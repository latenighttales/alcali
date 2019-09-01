import Vue from 'vue'
import App from './App.vue'
import vuetify from './plugins/vuetify';
import router from './router'
import axios from "axios";
import store from './store'


Vue.config.productionTip = false;

Vue.prototype.$http = axios;
Vue.prototype.$http.defaults.xsrfCookieName = 'csrftoken'
Vue.prototype.$http.defaults.xsrfHeaderName = 'X-CSRFToken'
Vue.prototype.$http.defaults.headers.common['Content-Type'] = 'application/json'

const accessToken = localStorage.getItem('token')
if (accessToken) {
  Vue.prototype.$http.defaults.headers.common.Authorization = `Bearer ${accessToken}`
  Vue.prototype.$http.defaults.withCredentials = true
}

/// for multiple parallel requests
let isRefreshing = false;
let failedQueue = [];

const processQueue = (error, token = null) => {
  failedQueue.forEach(prom => {
    if (error) {
      prom.reject(error);
    } else {
      prom.resolve(token);
    }
  })

  failedQueue = [];
}

Vue.prototype.$http.interceptors.response.use(function (response) {
  return response;
}, function (error) {

  const originalRequest = error.config;

  if (error.response.status === 401 && !originalRequest._retry) {

    if (isRefreshing) {
      return new Promise(function (resolve, reject) {
        failedQueue.push({resolve, reject})
      }).then(token => {
        originalRequest.headers['Authorization'] = 'Bearer ' + token;
        return Vue.prototype.$http(originalRequest);
      }).catch(err => {
        return err
      })
    }

    originalRequest._retry = true;
    isRefreshing = true;

    const refreshToken = window.localStorage.getItem('refresh');
    return new Promise(function (resolve, reject) {
      Vue.prototype.$http.post('/api/token/refresh/', {refresh: refreshToken})
        .then(({data}) => {
          window.localStorage.setItem('access', data.access);
          Vue.prototype.$http.defaults.headers.common['Authorization'] = 'Bearer ' + data.access;
          originalRequest.headers['Authorization'] = 'Bearer ' + data.access;
          processQueue(null, data.access);
          resolve(Vue.prototype.$http(originalRequest));
        })
        .catch((err) => {
          processQueue(err, null);
          reject(err);
        })
        .then(() => {
          isRefreshing = false
        })
    })
  }

  return Promise.reject(error).then(() => {
    router.push("/login")
  });
});


new Vue({
  vuetify,
  router,
  store,
  render: h => h(App)
}).$mount('#app');
