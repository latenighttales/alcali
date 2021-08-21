<template>
  <v-container fluid>
    <v-row no-gutters v-if="filter == null">
      <v-col sm="12">
        <v-card class="mb-8">
          <v-row>
            <v-col lg="2">
              <v-card-title>{{
                $t("components.JobsTable.SearchJobs")
              }}</v-card-title>
            </v-col>
            <v-col lg="2" offset-lg="2">
              <v-menu
                ref="menu"
                v-model="menu"
                :close-on-content-click="false"
                :return-value.sync="selectedDate"
                transition="scale-transition"
                offset-y
                min-width="290px"
              >
                <template v-slot:activator="{ on }">
                  <v-text-field
                    v-model="dateRangeText"
                    :label="$t('components.JobsTable.SelectDate')"
                    readonly
                    v-on="on"
                  ></v-text-field>
                </template>
                <v-date-picker
                  :max="new Date().toISOString().split('T')[0]"
                  v-model="selectedDate"
                  reactive
                  no-title
                  range
                >
                  <div class="flex-grow-1"></div>
                  <v-btn text color="primary" @click="menu = false">{{
                    $t("components.JobsTable.Cancel")
                  }}</v-btn>
                  <v-btn
                    text
                    color="primary"
                    @click="$refs.menu.save(selectedDate)"
                    >OK</v-btn
                  >
                </v-date-picker>
              </v-menu>
            </v-col>
            <v-col lg="2">
              <v-autocomplete
                :items="users"
                v-model="selectedUsers"
                :label="$t('components.JobsTable.User')"
                multiple
                single-line
              >
                <template v-slot:selection="{ item, index }">
                  <span v-if="index === 0">{{ item }}</span>
                  <span v-if="index === 1" class="grey--text caption">
                    (+{{ selectedUsers.length - 1 }} others)</span
                  >
                </template>
              </v-autocomplete>
            </v-col>
            <v-col lg="2">
              <v-autocomplete
                :items="minions"
                v-model="selectedTarget"
                :label="$t('components.JobsTable.Target')"
                multiple
                single-line
              >
                <template v-slot:selection="{ item, index }">
                  <span v-if="index === 0">{{ item }}</span>
                  <span v-if="index === 1" class="grey--text caption">
                    (+{{ selectedTarget.length - 1 }} others)</span
                  >
                </template>
              </v-autocomplete>
            </v-col>
            <v-col lg="1">
              <v-select
                :items="limit"
                v-model="selectedLimit"
                :label="$t('components.JobsTable.Limit')"
                single-line
              >
              </v-select>
            </v-col>
            <v-col lg="1" align-self="center">
              <div class="text-center">
                <v-btn color="primary" @click="filterJobs"
                  >{{ $t("common.Search") }}
                </v-btn>
              </div>
            </v-col>
          </v-row>
        </v-card>
      </v-col>
    </v-row>
    <v-row no-gutters>
      <v-col sm="12">
        <v-card
          :elevation="filter == null || filter.hasOwnProperty('limit') ? 2 : 0"
        >
          <v-card-title>
            {{ $t("components.JobsTable.Job") }}
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
            :sort-by.sync="settings.JobsTable.table.sortBy"
            @update:sort-by="updateSettings"
            :sort-desc.sync="settings.JobsTable.table.sortDesc"
            @update:sort-desc="updateSettings"
            :items-per-page.sync="settings.JobsTable.table.itemsPerPage"
            @update:items-per-page="updateSettings"
            item-key="uniqueid"
            :headers="filteredHeaders"
            :items="indexedItems"
            :search="search"
            class="elevation-1"
            :loading="loading"
          >
            <template v-slot:item.jid="{ item }">
              <v-btn
                text
                small
                class="text-none"
                :to="'/jobs/' + item.jid + '/' + item.id"
                >{{ item.jid }}</v-btn
              >
            </template>
            <template v-slot:item.id="{ item }">
              <v-btn
                text
                small
                class="text-none"
                :to="'/minions/' + item.id"
                v-show="!filter || filter.hasOwnProperty('limit')"
                >{{ item.id }}</v-btn
              >
            </template>
            <template v-slot:item.arguments="{ item }">
              {{
                item.arguments.length > 20
                  ? item.arguments.slice(0, 20) + "..."
                  : item.arguments
              }}
            </template>
            <template v-slot:item.keyword_arguments="{ item }">
              {{
                item.keyword_arguments.length > 20
                  ? item.keyword_arguments.slice(0, 20) + "..."
                  : item.keyword_arguments
              }}
            </template>
            <template v-slot:item.success="{ item }">
              <v-chip :color="boolRepr(item.success)" dark>{{
                boolText(item.success)
              }}</v-chip>
            </template>
            <template v-slot:item.alter_time="{ item }">
              {{ new Date(item.alter_time).toLocaleString("en-GB") }}
            </template>
            <template v-slot:item.action="{ item }">
              <div class="text-center">
                <v-btn
                  small
                  class="ma-2"
                  color="blue"
                  tile
                  dark
                  :to="'/jobs/' + item.jid + '/' + item.id"
                >
                  {{$t("components.JobsTable.Detail")}}
                </v-btn>
                <v-btn
                  small
                  class="ma-2"
                  color="blue-grey"
                  tile
                  dark
                  :to="
                    '/run?tgt=' +
                    item.id +
                    '&fun=' +
                    item.fun +
                    '&arg=' +
                    item.arguments +
                    '&kwarg=' +
                    item.keyword_arguments
                  "
                >
                  {{$t("components.JobsTable.Rerun")}}
                </v-btn>
              </div>
            </template>
          </v-data-table>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import { mapState } from "vuex"

export default {
  name: "JobsTable",
  props: ["filter", "jid"],
  data() {
    return {
      menu: false,
      limit: [50, 100, 200, 500, 1000],
      selectedDate: [],
      selectedLimit: null,
      selectedUsers: null,
      selectedTarget: null,
      minions: [],
      users: [],
      search: "",
      headers: [
        { text: this.$t("components.JobsTable.JID"), value: "jid" },
        { text: this.$t("components.JobsTable.Target"), value: "id" },
        { text: this.$t("components.JobsTable.Function"), value: "fun" },
        { text: this.$t("components.JobsTable.Arguments"), value: "arguments" },
        {
          text: this.$t("components.JobsTable.KeywordArguments"),
          value: "keyword_arguments",
        },
        { text: this.$t("components.JobsTable.User"), value: "user" },
        { text: this.$t("components.JobsTable.Status"), value: "success" },
        { text: this.$t("components.JobsTable.Date"), value: "alter_time" },
        {
          text: this.$t("components.JobsTable.Action"),
          value: "action",
          sortable: false,
        },
      ],
      jobs: [],
      loading: true,
    };
  },
  computed: {
    indexedItems() {
      return this.jobs.map((item, index) => ({
        uniqueid: index,
        ...item,
      }));
    },
    dateRangeText() {
      return this.selectedDate.join(" ~ ");
    },
    filteredHeaders() {
      if (this.filter && this.filter.hasOwnProperty("target[]")) {
        let newHeaders = this.headers;
        newHeaders.splice(1, 1);
        return newHeaders;
      }
      return this.headers;
    },
    ...mapState({
      settings: state => state.settings,
    }),
  },
  mounted() {
    this.loadData();
  },
  methods: {
    updateSettings() {
      this.$store.commit("updateSettings")
    },
    loadData() {
      this.$http.get("api/jobs/filters/").then((response) => {
        this.minions = response.data.minions;
        this.users = response.data.users;
      });
      if (this.jid) {
        this.$http.get(`api/jobs/${this.jid}`).then((response) => {
          this.jobs = response.data;
          this.loading = false;
        });
      } else {
        this.$http
          .get("api/jobs/", { params: this.filter })
          .then((response) => {
            this.jobs = response.data;
            this.loading = false;
          });
      }
    },
    filterJobs() {
      this.loading = true;
      let params = {
        limit: this.selectedLimit,
        target: this.selectedTarget,
        users: this.selectedUsers,
      };
      if (this.selectedDate.length > 0) {
        params.start = this.selectedDate[0];
        params.end = this.selectedDate[1] || this.selectedDate[0];
      }
      this.$http
        .get("api/jobs/", {
          params: params,
        })
        .then((response) => {
          this.jobs = response.data;
          this.loading = false;
          this.selectedUsers = this.selectedTarget = this.selectedLimit = this.selectedDate = null;
          this.selectedDate = [];
        });
    },
    boolRepr(bool) {
      if (bool === true) return "green";
      else return "red";
    },
    boolText(bool) {
      if (bool === true) return this.$i18n.t("components.JobsTable.Success");
      else return this.$i18n.t("components.JobsTable.Failed");
    },
  },
};
</script>

<style scoped>
</style>