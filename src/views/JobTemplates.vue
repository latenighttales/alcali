<template>
  <v-container>
    <v-row>
      <v-col sm="12" cols="12">
        <JobTemplatesTable></JobTemplatesTable>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
  import JobTemplatesTable from "../components/JobTemplatesTable"

  export default {
    name: "JobTemplates",
    components: {
      JobTemplatesTable,
    },
  }

</script>

<style scoped>

</style>