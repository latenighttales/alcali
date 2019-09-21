<template>
  <v-container>
    <v-card>
      <v-card-title>
        Events
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
          sort-by="alter_time"
          sort-desc
          :headers="headers"
          :items="events"
          :search="search"
          class="elevation-1"
          show-expand
          :loading="loading"
      >
        <template v-slot:item.alter_time="{ item }">
          {{new Date(item.alter_time).toLocaleString("en-GB")}}
        </template>
        <template v-slot:expanded-item="{ headers,item }">
          <td :colspan="headers.length">
            <pre>{{JSON.stringify(JSON.parse(item.data), null, 2)}}</pre>
          </td>
        </template>
      </v-data-table>
    </v-card>
  </v-container>
</template>

<script>
  function addedData(data) {
    data.forEach(event => {
      let grain = JSON.parse(event.data)
      for (let key in grain) {
        if (key === "id") {
          event["minion_id"] = grain[key]
        } else {
          event[key] = grain[key]
        }
      }
    })
    return data
  }

  export default {
    name: "EventsTable",
    data() {
      return {
        search: "",
        headers: [
          { text: "Tag", value: "tag" },
          { text: "Jid", value: "jid" },
          { text: "Target", value: "minion_id" },
          { text: "Function", value: "fun" },
          { text: "Arguments", value: "fun_args" },
          { text: "Date", value: "alter_time" },
        ],
        events: [],
        loading: true,
      }
    },
    mounted() {
      this.loadData()
    },
    methods: {
      loadData() {
        this.$http.get("api/events/").then(response => {
          this.events = addedData(response.data)
          this.loading = false
        })
      },
    },
  }
</script>

<style scoped>

</style>