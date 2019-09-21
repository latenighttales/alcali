import Vue from "vue"
import Vuex from "vuex"
import axios from "axios"

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    username: localStorage.getItem("username") || "",
    email: localStorage.getItem("email") || "",
    id: localStorage.getItem("id") || "",
    access: localStorage.getItem("access") || "",
    refresh: localStorage.getItem("refresh") || "",
    ws_status: false,
    theme: localStorage.getItem("theme") || false,
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
    toggleTheme(state) {
      state.theme = !state.theme
      localStorage.setItem('theme', JSON.stringify(state.theme))
    },
  },
  getters: {
    isLoggedIn: state => !!state.access,
    theme: state => state.theme,
    user_id: state => state.id,
  },
  actions: {
    updateWs({ commit }) {
      commit("updateWs")
    },
    toggleTheme({ commit }) {
      commit("toggleTheme")
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
