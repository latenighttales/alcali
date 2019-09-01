<template>
    <v-container fluid grid-list-lg>
    <v-layout row wrap>
      <v-flex lg12>
      <EventsTable></EventsTable>
      </v-flex>
    </v-layout>
  </v-container>
</template>

<script>
  import EventsTable from "../components/EventsTable";
  export default {
    name: "Events",
    components: {EventsTable}
  }
</script>

<style scoped>

</style>