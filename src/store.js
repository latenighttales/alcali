import Vue from "vue"
import Vuex from "vuex"
import createPersistedState from "vuex-persistedstate"
import axios from "axios"

Vue.use(Vuex)

export default new Vuex.Store({
  plugins: [createPersistedState()],
  state: {
    username: "",
    email: "",
    id: "",
    access: "",
    refresh: "",
    is_staff: false,
    ws_status: false,
    settings: {},
  },
  mutations: {
    auth_success(state, data) {
      Object.keys(data).forEach(key => {
        state[key] = data[key]
      })
    },
    logout(state) {
      state.access = ""
    },
    updateWs(state) {
      state.ws_status = true
    },
    setSettings(state, settings) {
      state.settings = settings
    },
    updateSettings(state) {
      axios.patch(`api/userssettings/${state.id}/`, { settings: state.settings }).then(() => {
      }).catch((err) => {
        console.log("update settings failed:", err)
      })
    },
  },
  getters: {
    isLoggedIn: state => !!state.access,
    user_id: state => state.id,
    isStaff: state => state.is_staff,
    settings: state => state.settings,
  },
  actions: {
    updateWs({ commit }) {
      commit("updateWs")
    },
    toggleTheme({ commit }) {
      commit("toggleTheme")
    },
    fetchSettings(context) {
      axios.get(`api/userssettings/${context.getters.user_id}/`).then(response => {
        context.commit("setSettings", response.data.settings)
      }).catch(err => {
        console.log(err)
      })
    },
    login({ commit }, user_data) {
      return new Promise((resolve, reject) => {
        axios({ url: "/api/token/", data: user_data, method: "POST" })
          .then(resp => {
            Object.keys(resp.data).forEach(key => {
              localStorage.setItem(key, resp.data[key])
            })
            axios.defaults.headers.common.Authorization = `Bearer ${resp.data.access}`
            commit("auth_success", resp.data)
            resolve(resp)
          })
          .catch(err => {
            localStorage.clear()
            reject(err)
          })
      })
    },
    oauthlogin({ commit }, user_data) {
      return new Promise((resolve, reject) => {
        axios({ url: "/api/social/login/", data: user_data, method: "POST" })
          .then(resp => {
            // rename token to access
            delete Object.assign(resp.data, { ["access"]: resp.data["token"] })["token"]
            Object.keys(resp.data).forEach(key => {
              localStorage.setItem(key, resp.data[key])
            })
            axios.defaults.headers.common.Authorization = `Bearer ${resp.data.access}`
            commit("auth_success", resp.data)
            resolve(resp)
          })
          .catch(err => {
            localStorage.clear()
            reject(err)
          })
      })
    },
    logout({ commit }) {
      return new Promise((resolve) => {
        commit("logout")
        localStorage.clear()
        delete axios.defaults.headers.common["Authorization"]
        resolve()
      })
    },

  },
})
