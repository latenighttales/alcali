<template>
  <v-container fluid>
    <v-row>
      <v-col sm="12">
        <KeysTable :key="refreshKey"></KeysTable>
      </v-col>
    </v-row>
    <Fab v-if="fabs" :fabs="fabs" v-on:fab_action="fabAction"></Fab>
  </v-container>
</template>

<script>

  import KeysTable from "../components/KeysTable"
  import Fab from "../components/core/Fab"

  export default {
    name: "Keys",
    components: { Fab, KeysTable },
    data() {
      return {
        fabs: [
          {
            color: "pink",
            action: "refreshKeys",
            icon: "refresh",
            tooltip: this.$i18n.t("components.Keys.Refresh"),
          },
          {
            color: "orange",
            action: "rejectAll",
            icon: "close",
            tooltip: this.$i18n.t("components.Keys.RejectAll"),
          },
          {
            color: "green",
            action: "acceptAll",
            icon: "done",
            tooltip: this.$i18n.t("components.Keys.AcceptAll"),
          }
        ],
        refreshKey: 0,
      }
    },
    methods: {
      fabAction(action) {
        this[action]()
      },
      refreshKeys() {
        this.$toast(this.$i18n.t("components.Keys.RefreshingKeys"))
        this.$http.post("/api/keys/refresh/").then((response) => {
          this.$toast(this.$i18n.t("components.Keys.KeysRefreshed"))
        }).then(() => {
          this.refreshKey += 1
        }).catch((error) => {
          this.$toast.error(error.response.data)
        })

      },
      acceptAll() {
        let formData = new FormData
        formData.set("action", "accept")
        formData.set("target", "*")
        this.$http.post("api/keys/manage_keys/", formData).then(response => {
          this.$toast(response.data.result)
        }).then(() => {
          this.refreshKey += 1
        }).catch((error) => {
          this.$toast.error(error.response.data)
        })
      },
      rejectAll() {
        let formData = new FormData
        formData.set("action", "reject")
        formData.set("target", "*")
        this.$http.post("api/keys/manage_keys/", formData).then(response => {
          this.$toast(response.data.result)
        }).then(() => {
          this.refreshKey += 1
        }).catch((error) => {
          this.$toast.error(error.response.data)
        })
      },
    },
  }
</script>

<style scoped>

</style>