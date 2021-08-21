<template>
  <v-container fluid>
    <v-row>
      <v-col sm="12">
        <ScheduleTable :key="refreshKey"></ScheduleTable>
        <Fab v-if="fabs" :fabs="fabs" v-on:fab_action="fabAction"></Fab>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
  import ScheduleTable from "../components/ScheduleTable"
  import Fab from "../components/core/Fab"

  export default {
    name: "Schedules",
    components: { Fab, ScheduleTable },
    data() {
      return {
        fabs: [
          {
            color: "pink",
            action: "refreshSchedules",
            icon: "refresh",
            tooltip: this.$i18n.t("components.Schedules.Refresh"),
          },
        ],
        refreshKey: 0,
      }
    },
    methods: {
      fabAction(action) {
        this[action]()
      },
      refreshSchedules() {
        this.$toast(this.$i18n.t("components.Schedules.Refreshing"))
        this.$http.post("/api/schedules/refresh/").then(() => {
          this.refreshKey += 1
          this.$toast(this.$i18n.t("components.Schedules.Refreshed"))
        }).catch((error) => {
          this.$toast.error(error.response.data)
        })

      },
    },
  }
</script>

<style scoped>

</style>