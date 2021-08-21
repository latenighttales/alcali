<template>
  <v-container fluid>
    <v-card>
      <v-card-title>
        {{ $t("components.KeysTable.Keys") }}
        <v-spacer></v-spacer>
        <v-text-field
          class="search"
          v-model="search"
          append-icon="search"
          :label="$t('common.Search')"
          single-line
          hide-details
        ></v-text-field>
      </v-card-title>
      <v-data-table
        :sort-by.sync="settings.KeysTable.table.sortBy"
        @update:sort-by="updateSettings"
        :sort-desc.sync="settings.KeysTable.table.sortDesc"
        @update:sort-desc="updateSettings"
        :items-per-page.sync="settings.KeysTable.table.itemsPerPage"
        @update:items-per-page="updateSettings"
        :headers="headers"
        :items="keys"
        :search="search"
        class="elevation-1"
        :loading="loading"
      >
        <template v-slot:item.minion_id="{ item }">
          <template v-if="item.status === 'accepted'">
            <v-btn
              text
              small
              class="text-none"
              :to="'/minions/' + item.minion_id"
              >{{ item.minion_id }}</v-btn
            >
          </template>
          <template v-else>
            {{ item.minion_id }}
          </template>
        </template>
        <template v-slot:item.status="{ item }">
          <v-chip :color="keysRepr(item.status)" dark>{{
            $t(`components.KeysTable.${item.status.toString()}`)
          }}</v-chip>
        </template>
        <template v-slot:item.action="{ item }">
          <template v-for="action in keyAction(item.status)">
            <v-btn
              small
              class="ma-2"
              dark
              v-bind:color="keysRepr(action)"
              @click="manageKey(action, item.minion_id)"
              :key="action"
            >
              {{ $t(`components.KeysTable.${action}`) }}
            </v-btn>
          </template>
        </template>
      </v-data-table>
    </v-card>
  </v-container>
</template>

<script>
import { mapState } from "vuex"

export default {
  name: "KeysTable",
  data() {
    return {
      search: "",
      headers: [
        { text: this.$t("components.KeysTable.MinionId"), value: "minion_id" },
        { text: this.$t("components.KeysTable.Status"), value: "status" },
        { text: this.$t("components.KeysTable.PublicKey"), value: "pub" },
        {
          text: this.$t("components.KeysTable.Actions"),
          value: "action",
          sortable: false,
        },
      ],
      keys: [],
      loading: true,
    };
  },
  mounted() {
    this.loadData();
  },
  methods: {
    updateSettings() {
      this.$store.commit("updateSettings")
    },
    loadData() {
      this.$http.get("api/keys/").then((response) => {
        this.keys = response.data;
        this.loading = false;
      });
    },
    sleep(milliseconds) {
      return new Promise((resolve) => setTimeout(resolve, milliseconds));
    },
    keysRepr(status) {
      if (status.startsWith("accept")) {
        return "green";
      } else if (status.startsWith("reject")) {
        return "orange";
      } else if (status.startsWith("de")) {
        return "red";
      } else {
        return "grey";
      }
    },
    keyAction(status) {
      if (status === "accepted") {
        return ["reject", "delete"];
      } else if (status === "rejected") {
        return ["accept", "delete"];
      } else if (status === "denied") {
        return ["accept"];
      } else {
        return ["accept", "delete"];
      }
    },
    manageKey(action, key) {
      let formData = new FormData();
      formData.set("action", action);
      formData.set("target", key);
      this.$http
        .post("api/keys/manage_keys/", formData)
        .then((response) => {
          this.$toast(response.data.result);
        })
        .catch((error) => {
          this.$toast.error(error.response.data);
        });
      this.sleep(2000).then(() => {
        this.loadData();
      });
    },
  },
  computed: {
    ...mapState({
      settings: state => state.settings,
    }),
  },
};
</script>

<style scoped>
</style>