<template>
  <v-container fluid>
    <v-row>
      <v-col sm="12">
        <EventsTable :key="master"></EventsTable>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
  import EventsTable from "../components/EventsTable"

  export default {
    name: "Events",
    props: ["master"],
    components: { EventsTable },
  }
</script>

<style scoped>

</style>