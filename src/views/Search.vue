<template>
  <v-container fluid>
    <v-row>
      <v-col sm="12" v-if="jobs.length === 0 && minions.length === 0">
        <v-container fluid>
          <p class="display-2 text-center">{{ $t("views.Search.NoResult") }}</p>
        </v-container>
      </v-col>
      <v-col sm="12" v-if="jobs.length > 0">
        <v-container fluid>
          <v-card>
            <v-card-title>
              {{ $t("views.Search.Jobs") }}
              <v-spacer></v-spacer>
              <v-text-field
                v-model="job_search"
                append-icon="search"
                :label="$t('common.Search')"
                single-line
                hide-details
              ></v-text-field>
            </v-card-title>
            <v-data-table
              sort-by="jid"
              sort-desc
              :headers="jobs_headers"
              :items="jobs"
              :search="search"
              :items-per-page="5"
              class="elevation-1"
            >
              <template v-slot:item.jid="{ item }">
                <v-btn
                  text
                  small
                  class="text-none"
                  :class="item.jid.includes(query) ? 'red' : ''"
                  :to="'/jobs/' + item.jid + '/' + item.id"
                  >{{ item.jid }}
                </v-btn>
              </template>
              <template v-slot:item.fun="{ item }">
                <span :class="item.fun.includes(query) ? 'red' : ''">{{
                  item.fun
                }}</span>
              </template>
              <template v-slot:item.arguments="{ item }">
                {{
                  item.arguments.length > 20
                    ? item.arguments.slice(0, 20) + "..."
                    : item.arguments
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
            </v-data-table>
          </v-card>
        </v-container>
      </v-col>
      <v-col sm="12" v-if="minions.length > 0">
        <v-container fluid>
          <v-card>
            <v-card-title>
              Minions
              <v-spacer></v-spacer>
              <v-text-field
                v-model="search"
                append-icon="search"
                :label="$t('common.Search')"
                single-line
                hide-details
              ></v-text-field>
            </v-card-title>
            <v-data-table
              :headers="minions_headers"
              :items="minions"
              :items-per-page="5"
              class="elevation-1"
            >
              <template v-slot:item.minion_id="{ item }">
                <v-btn
                  text
                  small
                  class="text-none"
                  :class="item.minion_id.includes(query) ? 'red' : ''"
                  :to="'/minions/' + item.minion_id"
                  >{{ item.minion_id }}
                </v-btn>
              </template>
              <template v-slot:item.conformity="{ item }">
                <v-chip :color="boolRepr(item.conformity)" dark
                  >{{ item.conformity == null ? "unknown" : item.conformity }}
                </v-chip>
              </template>
              <template v-slot:item.last_job="{ item }">
                {{
                  item.last_job === null
                    ? ""
                    : new Date(item.last_job).toLocaleString("en-GB")
                }}
              </template>
              <template v-slot:item.last_highstate="{ item }">
                {{
                  item.last_highstate === null
                    ? ""
                    : new Date(item.last_highstate).toLocaleString("en-GB")
                }}
              </template>
            </v-data-table>
          </v-card>
        </v-container>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
export default {
  name: "Search",
  data() {
    return {
      query: null,
      jobs: [],
      jobs_headers: [
        { text: "Jid", value: "jid" },
        { text: "Target", value: "id" },
        { text: "Function", value: "fun" },
        { text: "Arguments", value: "arguments" },
        { text: "User", value: "user" },
        { text: "Status", value: "success" },
        { text: "Date", value: "alter_time" },
      ],
      job_search: "",
      minions: [],
      minions_headers: [
        { text: "Minion Id", value: "minion_id" },
        { text: "Highstate Conformity", value: "conformity" },
        { text: "F.Q.D.N", value: "fqdn" },
        { text: "O.S", value: "os" },
        { text: "O.S Version", value: "oscodename" },
        { text: "Kernel", value: "kernelrelease" },
        { text: "Last Job", value: "last_job" },
        { text: "Last Highstate", value: "last_highstate" },
      ],
    };
  },
  created() {
    this.query = this.$route.query.q;
  },
  mounted() {
    this.searchBar();
  },
  methods: {
    searchBar() {
      this.$http.get("api/search/?q=" + this.query).then((response) => {
        function addedGrains(data) {
          data.forEach((min) => {
            let grain = JSON.parse(min.grain);
            for (let key in grain) {
              min[key] = grain[key];
            }
          });
          return data;
        }

        this.jobs = response.data.jobs;
        this.minions = addedGrains(response.data.minions);
      });
    },
    boolRepr(bool) {
      if (bool === true) return "green";
      else return "red";
    },
    boolText(bool) {
      if (bool === true) return this.$t("views.Search.Success");
      else return this.$t("views.Search.Failed");
    },
  },
};
</script>

<style scoped>
</style>