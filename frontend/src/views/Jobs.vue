<template>
  <v-container>
    <v-row>
      <v-col sm="12">
        <JobsTable></JobsTable>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
  import JobsTable from "../components/JobsTable";

  export default {
    name: "Jobs",
    components: {
      JobsTable
    }
  }

</script>

<style scoped>

</style>