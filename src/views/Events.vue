<template>
  <v-container fluid>
    <v-row>
      <v-col sm="12">
        <EventsTable></EventsTable>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
  import EventsTable from "../components/EventsTable"

  export default {
    name: "Events",
    components: { EventsTable },
  }
</script>

<style scoped>

</style>