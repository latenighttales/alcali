<template>
  <v-container fluid>
    <v-card>
      <v-card-title>{{
        $t("components.UserSettings.UserSettings")
      }}</v-card-title>
      <v-card-text>
        <v-container fluid>
          <v-row>
            <v-col lg="2">
              <span>{{ $t("components.UserSettings.JobsNotifications") }}</span>
              <div v-for="(val, name) in settings.UserSettings.notifs" :key="name">
                <v-switch
                  v-model="settings.UserSettings.notifs[name]"
                  :label="$t(`components.UserSettings.${name}`)"
                  color="primary"
                  hide-details
                ></v-switch>
              </div>
            </v-col>
            <v-col lg="2">
              <span>{{ $t("components.UserSettings.MaxNotifications") }}</span>
              <v-text-field v-model="settings.UserSettings.max_notifs" type="number"></v-text-field>
            </v-col>
            <v-col lg="2">
              <div class="locale-changer" style="margin-left: 20px">
                <span>{{ $t("components.UserSettings.Language") }}</span>
                <div>
                  <v-select :items="langs" v-model="$i18n.locale">
                    <template v-slot:selection="{ item }">
                      <img
                        :src="item.image"
                        style="width: 25px; height: 25px; margin-right: 5px"
                      />
                      {{ item.text }}
                    </template>
                    <template v-slot:item="{ item }">
                      <img
                        :src="item.image"
                        style="width: 25px; height: 25px; margin-right: 5px"
                      />
                      {{ item.text }}
                    </template>
                  </v-select>
                </div>
              </div>
            </v-col>
          </v-row>
        </v-container>
      </v-card-text>
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn color="primary" @click="updateSettings">{{
          $t("components.UserSettings.Submit")
        }}</v-btn>
      </v-card-actions>
    </v-card>
  </v-container>
</template>

<script>
import { mapState } from "vuex"

export default {
  name: "UserSettings",
  data() {
    return {
      langs: [
        {
          text: "english",
          value: "en",
          image: require("../assets/img/i18n/en.png"),
        },
        {
          text: "français",
          value: "fr",
          image: require("../assets/img/i18n/fr.png"),
        },
        {
          text: "chinese",
          value: "zh",
          image: require("../assets/img/i18n/zh.png"),
        },
      ],
    }
  },
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
};
</script>

<style scoped></style>
