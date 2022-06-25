<template>
  <v-container fluid>
    <v-card>
      <v-card-title>
        {{ $t("components.EventsTable.Events") }}
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
        :sort-by.sync="settings.EventsTable.table.sortBy"
        @update:sort-by="updateSettings"
        :sort-desc.sync="settings.EventsTable.table.sortDesc"
        @update:sort-desc="updateSettings"
        :items-per-page.sync="settings.EventsTable.table.itemsPerPage"
        @update:items-per-page="updateSettings"
        :headers="headers"
        :items="events"
        :search="search"
        class="elevation-1"
        show-expand
        :loading="loading"
      >
        <template v-slot:item.alter_time="{ item }">
          {{ new Date(item.alter_time).toLocaleString("en-GB") }}
        </template>
        <template v-slot:expanded-item="{ headers, item }">
          <td :colspan="headers.length">
            <pre>{{ JSON.stringify(safeParse(item.data), null, 2) }}</pre>
          </td>
        </template>
      </v-data-table>
    </v-card>
  </v-container>
</template>

<script>
import { mapState } from "vuex"

function addedData(data) {
  data.forEach((event) => {
    let grain = JSON.parse(event.data);
    for (let key in grain) {
      if (key === "id") {
        event["minion_id"] = grain[key];
      } else {
        event[key] = grain[key];
      }
    }
  });
  return data;
}

export default {
  name: "EventsTable",
  data() {
    return {
      search: "",
      headers: [
        { text: this.$i18n.t("components.EventsTable.Tag"), value: "tag" },
        { text: this.$i18n.t("components.EventsTable.Jid"), value: "jid" },
        {
          text: this.$i18n.t("components.EventsTable.Target"),
          value: "minion_id",
        },
        { text: this.$i18n.t("components.EventsTable.Function"), value: "fun" },
        {
          text: this.$i18n.t("components.EventsTable.Arguments"),
          value: "fun_args",
        },
        {
          text: this.$i18n.t("components.EventsTable.Date"),
          value: "alter_time",
        },
      ],
      events: [],
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
      this.$http.get("api/events/").then((response) => {
        this.events = addedData(response.data);
        this.loading = false;
      });
    },
    safeParse(json) {
      let parsed;
      try {
        parsed = JSON.parse(json);
      } catch (e) {
        return {};
      }
      return parsed;
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