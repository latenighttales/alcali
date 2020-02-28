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
    data: () => ({
      fabs: [
        {
          color: "blue",
          action: "refreshKeys",
          icon: "compare_arrows",
          tooltip: "Refresh keys",
        },
        {
          color: "orange",
          action: "rejectAll",
          icon: "close",
          tooltip: "Reject all keys",
        },
        {
          color: "green",
          action: "acceptAll",
          icon: "done",
          tooltip: "Accept all keys",
        },
      ],
      refreshKey: 0,
    }),
    methods: {
      fabAction(action) {
        this[action]()
      },
      refreshKeys() {
        this.$toast("refreshing keys")
        this.$http.post("/api/keys/refresh/").then((response) => {
          this.$toast("keys refreshed")
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