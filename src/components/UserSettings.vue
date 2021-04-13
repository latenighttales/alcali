<template>
  <v-container fluid>
    <v-card>
      <v-card-title>User Settings</v-card-title>
      <v-card-text>
        <v-container fluid>
          <v-row>
            <v-col lg="2">
              <span>Jobs Notifications</span>
              <div v-for="(val, name) in settings.UserSettings.notifs" :key="name">
                <v-switch v-model="settings.UserSettings.notifs[name]" :label="name" color="primary"
                          hide-details></v-switch>
              </div>
            </v-col>
            <v-col lg="2">
              <span>Max Notifications</span>
              <v-text-field v-model="settings.UserSettings.max_notifs" type="number"></v-text-field>
            </v-col>
          </v-row>
        </v-container>
      </v-card-text>
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn color="primary" @click="updateSettings">Submit</v-btn>
      </v-card-actions>
    </v-card>
  </v-container>
</template>

<script>


import { mapState } from "vuex"

export default {
  name: "UserSettings",
  computed: {
    ...mapState({
      settings: state => state.settings,
    }),
  },
  methods: {
    updateSettings() {
      this.$store.commit("updateSettings")
    },
  },
}
</script>

<style scoped>

</style>