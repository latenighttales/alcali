<template>
  <v-container fluid>
    <v-row>
      <v-col sm="12">
        <ConformityTable :key="master"></ConformityTable>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
  import ConformityTable from "../components/ConformityTable"

  export default {
    name: "Conformity",
    props: ["master"],
    components: { ConformityTable },
  }
</script>

<style scoped>

</style>