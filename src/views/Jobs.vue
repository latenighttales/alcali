<template>
  <v-container fluid>
    <v-row>
      <v-col sm="12" cols="12">
        <JobsTable :key="master" :jid="jid"></JobsTable>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
  import JobsTable from "../components/JobsTable"

  export default {
    name: "Jobs",
    props: ["jid", "master"],
    components: {
      JobsTable,
    },
  }

</script>

<style scoped>

</style>