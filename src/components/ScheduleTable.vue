<template>
  <v-container>
    <v-card>
      <v-card-title>
        Schedules
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
          sort-by="minion"
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
                color="red"
                tile
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
  export default {
    name: "ScheduleTable",
    data() {
      return {
        search: '',
        headers: [],
        schedules: [],
        loading: true,
      }
    },
    methods: {
      loadData() {
        this.loading = false
        this.$http.get("api/schedules/").then(response => {
          this.schedules = response.data
          if (this.schedules.length > 0) {
            Object.keys(response.data[0]).forEach(key => {
              if (key !== "id") {
                this.headers.push({text: key, value: key})
              }
            })
            this.headers.push({text: "action", value: "action"})
          }
        })
      },
      manageSchedule(action, name, minion) {
        let formData = new FormData
        formData.set('action', action)
        formData.set('name', name)
        formData.set('minion', minion)
        this.$toast("performing " + action + " schedule " + name + " on " + minion)
        this.$http.post("api/schedules/manage/", formData).then(response => {
          this.$toast(response.data.result)
        })
      },
      boolRepr(bool) {
        if (bool === true) {
          return 'green'
        } else if (bool === false) {
          return 'red'
        } else return 'primary'
      },
    },
    mounted() {
      this.loadData()
    },
  }
</script>

<style scoped>

</style>