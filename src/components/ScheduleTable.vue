<template>
  <v-container fluid>
    <v-card>
      <v-card-title>
        Schedules
        <v-spacer></v-spacer>
        <v-text-field
            class="search"
            v-model="search"
            append-icon="search"
            label="Search"
            single-line
            hide-details
        ></v-text-field>
      </v-card-title>
      <v-data-table
          :sort-by.sync="settings.ScheduleTable.table.sortBy"
          @update:sort-by="updateSettings"
          :sort-desc.sync="settings.ScheduleTable.table.sortDesc"
          @update:sort-desc="updateSettings"
          :items-per-page.sync="settings.ScheduleTable.table.itemsPerPage"
          @update:items-per-page="updateSettings"
          :headers="headers"
          :items="schedules"
          :search="search"
          class="elevation-1"
          :loading="loading"
      >
        <template v-slot:item.enabled="{ item }">
          <v-chip :color="boolRepr(item.enabled)" dark>{{ item.enabled }}</v-chip>
        </template>
        <template v-slot:item.action="{ item }">
          <div class="text-center">
            <v-btn
                small
                :color="item.enabled ? 'orange': 'green'"
                tile
                class="ma-2"
                dark
                @click="manageSchedule(item.enabled ? 'disable_job': 'enable_job', item.name, item.minion)"
            >
              {{ item.enabled ? "disable" : "enable" }}
            </v-btn>
            <v-btn
                small
                color="red"
                tile
                class="ma-2"
                dark
                @click="manageSchedule('delete', item.name, item.minion)"
            >
              delete
            </v-btn>
          </div>
        </template>
      </v-data-table>
    </v-card>
  </v-container>
</template>

<script>
import { mapState } from "vuex"

export default {
  name: "ScheduleTable",
  data() {
    return {
      search: "",
      headers: [],
      schedules: [],
      loading: true,
    }
  },
  methods: {
    updateSettings() {
      this.$store.commit("updateSettings")
    },
    loadData() {
      this.loading = false
      this.$http.get("api/schedules/").then(response => {
        this.schedules = response.data
        if (this.schedules.length > 0) {
          // Custom headers ordering
          let headers = new Set(["minion", "name", "function"])
          // Add all needed header
          this.schedules.forEach(schedule => {
            Object.keys(schedule).forEach(key => {
              headers.add(key)
            })
          })
          headers.delete("id")
          headers.forEach(header => {
            this.headers.push({ text: header, value: header })
          })
          this.headers.push({ text: "action", value: "action" })
        }
      })
    },
    manageSchedule(action, name, minion) {
      this.$toast(`${action} on ${minion} for job ${name}`)
      let formData = new FormData
      formData.set("action", action)
      formData.set("name", name)
      formData.set("minion", minion)
      this.$http.post("api/schedules/manage/", formData).then(() => {
        this.$toast(`${action} on ${minion} for job ${name}: done`)
      }).then(() => {
        this.headers = []
        this.schedules = []
        this.loadData()
      }).catch((error) => {
        this.$toast.error(error.response.data)
      })
    },
    boolRepr(bool) {
      if (bool === true) {
        return "green"
      } else if (bool === false) {
        return "red"
      } else return "primary"
    },
  },
  mounted() {
    this.loadData()
  },
  computed: {
    ...mapState({
      settings: state => state.settings,
    }),
  },
}
</script>

<style scoped>

</style>