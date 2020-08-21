import 'material-design-icons-iconfont/dist/material-design-icons.css'
import 'typeface-roboto/index.css'
import Vue from "vue"
import Vuetify, { VSnackbar, VBtn, VIcon } from "vuetify/lib"

import VuetifyToast from "vuetify-toast-snackbar-ng"

Vue.use(Vuetify, {
  components: {
    VSnackbar,
    VBtn,
    VIcon,
  },
})

Vue.use(VuetifyToast, {
  x: "center", // default
  y: "bottom", // default
  color: "black", // default
  icon: "info",
  iconColor: "", // default
  classes: [
    "body-2",
  ],
  timeout: 3000, // default
  dismissable: true, // default
  multiLine: false, // default
  vertical: false, // default
  queueable: false, // default
  showClose: true, // default
  closeText: "", // default
  closeColor: "", // default
  shorts: {
    custom: {
      color: "purple",
    },
  },
  property: "$toast", // default
})

export default new Vuetify({
  icons: {
    iconfont: "md",
  },
  theme: {
    themes: {
      light: {
        primary: "#6200EE",
        secondary: "#03DAC6",
      },
      dark: {
        secondary: "#BB86FC",
        primary: "#03DAC6",
      },
    },
  },
})
