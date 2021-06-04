<template>
  <v-container fluid>
    <v-row>
      <v-col sm="12" lg="3">
        <InfosCard v-if="minion !== null" :minion="minion"></InfosCard>
        <NetworkCard v-if="minion !== null" :minion="minion"></NetworkCard>
      </v-col>
      <v-col sm="12" lg="9">
        <MinionDetailCard v-if="minion !== null" :minion="minion"></MinionDetailCard>
      </v-col>
      <Fab v-if="fabs" :fabs="fabs" v-on:fab_action="fabAction"></Fab>
    </v-row>
  </v-container>
</template>

<script>
  import InfosCard from "../components/InfosCard"

  function addedGrains(data) {
    let grain = JSON.parse(data.grain)
    for (let key in grain) {
      data[key] = grain[key]
    }
    return data
  }

  import NetworkCard from "../components/NetworkCard"
  import MinionDetailCard from "../components/MinionDetailCard"
  import Fab from "../components/core/Fab"

  export default {
    name: "MinionDetail",
    components: { Fab, MinionDetailCard, InfosCard, NetworkCard },
    data() {
      return {
        minion: null,
        fabs: [
          {
            color: "blue",
            action: "refreshMinion",
            icon: "refresh",
            tooltip: this.$i18n.t("components.MinionDetails.RefreshMinion") + this.minion_id,
          },
          {
            color: "purple",
            action: "runMinion",
            icon: "play_arrow",
            tooltip: this.$i18n.t("components.MinionDetails.JobMinion") + this.minion_id,
          },
          {
            color: "orange",
            action: "highstateMinion",
            icon: "all_inclusive",
            tooltip: this.$i18n.t("components.MinionDetails.HighstateMinion") + this.minion_id,
          },
        ],
      }
    },
    mounted() {
      this.loadData()
    },
    methods: {
      loadData() {
        this.$http.get(`api/minions/${this.minion_id}/`).then(response => this.minion = addedGrains(response.data)).catch((error) => {
          this.$toast.error(this.$i18n.t("components.MinionDetail.MissingMinion", [this.minion_id]))
          this.$router.push("/minions")
        })
      },
      fabAction(action) {
        this[action]()
      },
      refreshMinion() {
        this.$toast(this.$i18n.t("components.MinionDetail.Refreshing", [this.minion_id]))
        let formData = new FormData
        formData.set('minion_id', this.minion_id)
        this.$http.post("/api/minions/refresh_minions/", formData).then(() => {
          this.$toast(this.$i18n.t("components.MinionDetail.MinionRefreshed"))
        }).catch((error) => {
          this.$toast.error(error.response.data)
        })
      },
      runMinion() {
        this.$router.push("/run?tgt=" + this.minion_id)
      },
      highstateMinion() {
        this.$router.push("/run?tgt=" + this.minion_id + "&fun=state.apply")
      },
    },
    props: [
      "minion_id",
    ],
  }
</script>

<style scoped>

</style>