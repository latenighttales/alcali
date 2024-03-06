<template>
  <v-container fluid>
    <v-row>
      <v-col sm="12">
        <UserSettings></UserSettings>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
  import UserSettings from "../components/UserSettings"

  export default {
    name: "Settings",
    components: { UserSettings },
  }
</script>

<style scoped>

</style>