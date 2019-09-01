<template>
  <v-container>
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
          color: "pink",
          action: "refreshKeys",
          icon: "refresh",
          tooltip: "Refresh keys",
        },
        {
          color: "green",
          action: "acceptAll",
          icon: "playlist_play",
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
        this.$http.post("/api/keys/refresh/").then(() => {
          this.$toast("keys refreshed")
        }).then(() => {
          this.refreshKey += 1
        }).catch(function(error) {
          alert(error)
        })

      },
    },
  }
</script>

<style scoped>

</style>