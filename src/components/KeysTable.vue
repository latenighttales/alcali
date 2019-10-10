<template>
  <v-container>
    <v-card>
      <v-card-title>
        Keys
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
          sort-by="minion_id"
          :headers="headers"
          :items="keys"
          :search="search"
          class="elevation-1"
          :loading="loading"
      >
        <template v-slot:item.minion_id="{ item }">
          <template v-if="item.status === 'accepted'">
            <v-btn text small class="text-none" :to="'/minions/'+item.minion_id">{{ item.minion_id }}</v-btn>
          </template>
          <template v-else>
            {{item.minion_id}}
          </template>
        </template>
        <template v-slot:item.status="{ item }">
          <v-chip :color="keysRepr(item.status)" dark>{{ item.status }}</v-chip>
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
              {{ action }}
            </v-btn>
          </template>
        </template>
      </v-data-table>
    </v-card>
  </v-container>
</template>

<script>
  export default {
    name: "KeysTable",
    data() {
      return {
        search: "",
        headers: [
          { text: "Minion Id", value: "minion_id" },
          { text: "Status", value: "status" },
          { text: "Public Key", value: "pub" },
          { text: "Actions", value: "action", sortable: false },
        ],
        keys: [],
        loading: true,
      }
    },
    mounted() {
      this.loadData()
    },
    methods: {
      loadData() {
        this.$http.get("api/keys/").then(response => {
          this.keys = response.data
          this.loading = false
        })
      },
      sleep(milliseconds) {
        return new Promise(resolve => setTimeout(resolve, milliseconds))
      },
      keysRepr(status) {
        if (status.startsWith("accept")) {
          return "green"
        } else if (status.startsWith("reject")) {
          return "orange"
        } else if (status.startsWith("de")) {
          return "red"
        } else {
          return "grey"
        }
      },
      keyAction(status) {
        if (status === "accepted") {
          return ["reject", "delete"]
        } else if (status === "rejected") {
          return ["accept", "delete"]
        } else if (status === "denied") {
          return ["accept"]
        } else {
          return ["accept", "delete"]
        }
      },
      manageKey(action, key) {
        let formData = new FormData
        formData.set("action", action)
        formData.set("target", key)
        this.$http.post("api/keys/manage_keys/", formData).then(response => {
          this.$toast(response.data.result)
        })
        this.sleep(2000).then(() => {
          this.loadData()
        })

      },
    },
  }
</script>

<style scoped>

</style>