<template>
  <v-container>
    <v-row no-gutters v-if="filter == null">
      <v-col sm="12">
        <v-card class="mb-8">
          <v-row>
            <v-col lg="2">
              <v-card-title>Search Jobs</v-card-title>
            </v-col>
            <v-divider></v-divider>
            <v-col lg="2" align-self="center">
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
                      label="Select date(s)"
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
                  <v-btn text color="primary" @click="menu = false">Cancel</v-btn>
                  <v-btn text color="primary" @click="$refs.menu.save(selectedDate)">OK</v-btn>
                </v-date-picker>
              </v-menu>
            </v-col>
            <v-col lg="2">
              <v-autocomplete
                  :items="users"
                  v-model="selectedUsers"
                  label="User(s)"
                  multiple
                  single-line
              >
                <template v-slot:selection="{ item, index }">
                  <span v-if="index === 0">{{ item }}</span>
                  <span
                      v-if="index === 1"
                      class="grey--text caption"
                  > (+{{ selectedUsers.length - 1 }} others)</span>
                </template>
              </v-autocomplete>
            </v-col>
            <v-col lg="2">
              <v-autocomplete
                  :items="minions"
                  v-model="selectedTarget"
                  label="Target(s)"
                  multiple
                  single-line
              >
                <template v-slot:selection="{ item, index }">
                  <span v-if="index === 0">{{ item }}</span>
                  <span
                      v-if="index === 1"
                      class="grey--text caption"
                  > (+{{ selectedTarget.length - 1 }} others)</span>
                </template>
              </v-autocomplete>
            </v-col>
            <v-col lg="1">
              <v-select
                  :items="limit"
                  v-model="selectedLimit"
                  label="Limit"
                  single-line
              >
              </v-select>
            </v-col>
            <v-col lg="1" align-self="center">
              <div class="text-center">
                <v-btn
                    color="primary"
                    @click="filterJobs"
                >Search
                </v-btn>
              </div>
            </v-col>
          </v-row>
        </v-card>
      </v-col>
    </v-row>
    <v-row no-gutters>
      <v-col sm="12">
        <v-card :elevation="filter == null ? 2 : 0">
          <v-card-title>
            Jobs
            <v-spacer></v-spacer>
            <v-text-field
                v-model="search"
                append-icon="search"
                label="Search"
                single-line
                hide-details
            ></v-text-field>
          </v-card-title>
          <v-data-table
              sort-by="jid"
              sort-desc
              item-key="uniqueid"
              :headers="filteredHeaders"
              :items="indexedItems"
              :search="search"
              class="elevation-1"
              :loading="loading"
          >
            <template v-slot:item.jid="{ item }">
              <v-btn text small class="text-none" :to="'/jobs/'+item.jid+'/'+item.id">{{ item.jid }}</v-btn>
            </template>
            <template v-slot:item.id="{ item }">
              {{ filter ? "" :item.id }}
            </template>
            <template v-slot:item.arguments="{ item }">
              {{ item.arguments.length > 20 ? item.arguments.slice(0, 20)+"...": item.arguments }}
            </template>
            <template v-slot:item.success="{ item }">
              <v-chip :color="boolRepr(item.success)" dark>{{ boolText(item.success) }}</v-chip>
            </template>
            <template v-slot:item.alter_time="{ item }">
              {{new Date(item.alter_time).toLocaleString("en-GB")}}
            </template>
            <template v-slot:item.action="{ item }">
              <div class="text-center">
                <v-btn
                    small
                    class="ma-2"
                    color="blue"
                    tile
                    dark
                    :to="'/jobs/'+item.jid+'/'+item.id"
                >
                  detail
                </v-btn>
                <v-btn
                    small
                    class="ma-2"
                    color="blue-grey"
                    tile
                    dark
                    :to="'/run/?target='+item.id+'&function='+item.fun+'&args='+item.arguments"
                >
                  rerun
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

  export default {
    name: "JobsTable",
    props: ["filter"],
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
          { text: "Jid", value: "jid" },
          { text: "Target", value: "id" },
          { text: "Function", value: "fun" },
          { text: "Arguments", value: "arguments" },
          { text: "User", value: "user" },
          { text: "Status", value: "success" },
          { text: "Date", value: "alter_time" },
          { text: "Actions", value: "action", sortable: false },
        ],
        jobs: [],
        loading: true,
      }
    },
    computed: {
      indexedItems() {
        return this.jobs.map((item, index) => ({
          uniqueid: index,
          ...item,
        }))
      },
      dateRangeText() {
        return this.selectedDate.join(" ~ ")
      },
      filteredHeaders() {
        if (this.filter && this.filter.hasOwnProperty('target[]')) {
          this.headers.splice(1, 1)
        }
        return this.headers
      },
    },
    mounted() {
      this.loadData()
    },
    methods: {
      loadData() {
        this.$http.get("api/jobs/filters/").then(response => {
          this.minions = response.data.minions
          this.users = response.data.users
        })
        this.$http.get("api/jobs/", { params: this.filter }).then(response => {
          this.jobs = response.data
          this.loading = false
        })
      },
      filterJobs() {
        this.loading = true
        let params = {
          limit: this.selectedLimit,
          target: this.selectedTarget,
          users: this.selectedUsers,
        }
        if (this.selectedDate.length > 0) {
          params.start = this.selectedDate[0]
          params.end = this.selectedDate[1] || this.selectedDate[0]
        }
        this.$http.get("api/jobs/", {
          params: params,
        }).then(response => {
          this.jobs = response.data
          this.loading = false
          this.selectedUsers = this.selectedTarget = this.selectedLimit = this.selectedDate = null
          this.selectedDate = []
        })
      },
      boolRepr(bool) {
        if (bool === true) return "green"
        else return "red"
      },
      boolText(bool) {
        if (bool === true) return "success"
        else return "failed"
      },
    },
  }
</script>

<style scoped>

</style>