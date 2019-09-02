<template>
  <v-container>
    <v-row>
      <v-col sm="12" lg="3">
        <InfosCard v-if="minion !== null" :minion="minion"></InfosCard>
        <NetworkCard v-if="minion !== null" :minion="minion"></NetworkCard>
      </v-col>
      <v-col sm="12" lg="9">
        <MinionDetailCard v-if="minion !== null" :minion="minion"></MinionDetailCard>
      </v-col>
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

  export default {
    name: "MinionDetail",
    components: { MinionDetailCard, InfosCard, NetworkCard },
    data() {
      return {
        minion: null,
      }
    },
    mounted() {
      this.loadData()
    },
    methods: {
      loadData() {
        this.$http.get("api/minions/" + this.minion_id + "/").then(response => this.minion = addedGrains(response.data))
      },
    },
    props: [
      "minion_id",
    ],
  }
</script>

<style scoped>

</style>