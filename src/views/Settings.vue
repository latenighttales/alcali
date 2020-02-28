<template>
  <v-container fluid>
    <v-row>
      <v-col sm="12">
        <CommonSettings></CommonSettings>
      </v-col>
    </v-row>
    <v-row>
      <v-col sm="12">
        <UserSettings></UserSettings>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
  import CommonSettings from "../components/CommonSettings"
  import UserSettings from "../components/UserSettings"

  export default {
    name: "Settings",
    components: { UserSettings, CommonSettings },
  }
</script>

<style scoped>

</style>