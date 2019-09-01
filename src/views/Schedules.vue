<template>
  <v-container>
    <ScheduleTable :key="refreshKey"></ScheduleTable>
    <Fab v-if="fabs" :fabs="fabs" v-on:fab_action="fabAction"></Fab>
  </v-container>
</template>

<script>
  import ScheduleTable from "../components/ScheduleTable"
  import Fab from "../components/core/Fab"

  export default {
    name: "Schedules",
    components: { Fab, ScheduleTable },
    data: () => ({
      fabs: [
        {
          color: "pink",
          action: "refreshSchedules",
          icon: "refresh",
          tooltip: "Refresh schedules",
        },
      ],
      refreshKey: 0,
    }),
    methods: {
      fabAction(action) {
        this[action]()
      },
      refreshSchedules() {
        this.$toast("refreshing schedules")
        this.$http.post("/api/schedules/refresh/").then(() => {
          this.refreshKey += 1
          this.$toast("schedules refreshed")
        }).catch(function(error) {
          alert(error)
        })

      },
    },
  }
</script>

<style scoped>

</style>