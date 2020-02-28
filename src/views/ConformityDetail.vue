<template>
  <v-container fluid>
    <v-row>
      <v-col sm="12" lg="4">
        <ConformityCard :minion_id="minion_id" :conformity="conformity"
                        :custom_conformity="custom_conformity"></ConformityCard>
      </v-col>
      <v-col sm="12" lg="8">
        <ConformityDetailCard
            :succeeded="succeeded"
            :unchanged="unchanged"
            :failed="failed"
        ></ConformityDetailCard>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
  import ConformityDetailCard from "../components/ConformityDetailCard"
  import ConformityCard from "../components/ConformityCard"

  export default {
    name: "ConformityDetail",
    props: ["minion_id"],
    components: { ConformityCard, ConformityDetailCard },
    data() {
      return {
        conformity: "",
        succeeded: {},
        unchanged: {},
        failed: {},
        custom_conformity: [],
      }
    },
    mounted() {
      this.loadConformity()
    },
    methods: {
      loadConformity() {
        this.$http.get("api/minions/" + this.minion_id + "/conformity_detail/").then(response => {
          this.conformity = response.data.conformity
          this.custom_conformity = response.data.custom_conformity
          this.succeeded = response.data.succeeded
          this.unchanged = response.data.unchanged
          this.failed = response.data.failed
        })
      },
    },
  }
</script>

<style scoped>

</style>