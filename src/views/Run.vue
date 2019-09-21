<template>
  <v-container>
    <v-row>
      <v-col sm="12">
        <RunCard></RunCard>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
  import RunCard from "../components/RunCard";

  export default {
    name: "Run",
    components: {RunCard}
  }
</script>

<style scoped>

</style>