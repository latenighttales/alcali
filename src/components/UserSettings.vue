<template>
  <v-container fluid>
    <v-card>
      <v-card-title>{{$t('components.UserSettings.UserSettings')}}</v-card-title>
      <v-card-text>
        <v-container fluid>
          <v-row>
            <v-col lg="2">
              <span>{{$t('components.UserSettings.JobsNotifications')}}</span>
              <div v-for="(val, name) in notifs" :key="name">
                <v-switch v-model="notifs[name]" :label="$t(`components.UserSettings.${name}`)" color="primary" hide-details></v-switch>
              </div>
            </v-col>
            <v-col lg="2">
              <span>{{$t('components.UserSettings.MaxNotifications')}}</span>
              <v-text-field v-model="max_notifs" type="number"></v-text-field>
            </v-col>
          </v-row>
        </v-container>
      </v-card-text>
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn color="primary" @click="updateUserSettings">{{$t('components.UserSettings.Submit')}}</v-btn>
      </v-card-actions>
    </v-card>
  </v-container>
</template>

<script>
  export default {
    name: "UserSettings",
    data() {
      return {
        switch1: true,
        switch2: false,
        notifs: { created: false, published: true, returned: false, event: false },
        settings: null,
        max_notifs: null,
      }
    },
    methods: {
      loadData() {
        this.$http.get(`api/userssettings/${this.$store.getters.user_id}/`).then(response => {
          this.settings = response.data
          this.max_notifs = response.data.max_notifs
          Object.keys(this.notifs).forEach(notif => {
            this.notifs[notif] = this.settings["notifs_" + notif]
          })
        })
      },
      updateUserSettings() {
        let params = { max_notifs: this.max_notifs }
        Object.keys(this.notifs).forEach(notif => {
          params["notifs_" + notif] = this.notifs[notif]
        })
        this.$http.patch(`api/userssettings/${this.$store.getters.user_id}/`, params).then(response => {
          this.$toast(this.$i18n.t("components.UserSettings.UserSettingsUpdated"))
        })
      },
    },
    mounted() {
      this.loadData()
    },
  }
</script>

<style scoped>

</style>