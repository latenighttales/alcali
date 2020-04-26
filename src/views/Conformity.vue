<template>
  <v-container fluid>
    <v-row>
      <v-col sm="12">
        <ConformityTable></ConformityTable>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
  import ConformityTable from "../components/ConformityTable"

  export default {
    name: "Conformity",
    components: { ConformityTable },
  }
</script>

<style scoped>

</style>