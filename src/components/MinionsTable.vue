<template>
  <v-container>
    <v-card>
      <v-card-title>
        Minions
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
          :items="minions"
          :search="search"
          class="elevation-1"
          :loading="loading" loading-text="Loading... Please wait"
      >
        <template v-slot:item.minion_id="{ item }">
          <v-btn text small class="text-none" :to="'/minions/'+item.minion_id">{{ item.minion_id }}</v-btn>
        </template>
        <template v-slot:item.conformity="{ item }">
          <v-chip :color="boolRepr(item.conformity)" dark>{{ item.conformity }}
          </v-chip>
        </template>
        <template v-slot:item.last_job="{ item }">
          {{item.last_job === null ? "": new Date(item.last_job).toLocaleString("en-GB")}}
        </template>
        <template v-slot:item.last_highstate="{ item }">
          {{item.last_highstate === null ? "": new Date(item.last_highstate).toLocaleString("en-GB")}}
        </template>
        <template v-slot:item.action="{ item }">
          <div class="text-center">
            <v-btn
                small
                class="ma-2"
                color="blue"
                tile
                dark
                @click="refreshMinion(item.minion_id)"
            >
              refresh
            </v-btn>
            <v-btn
                small
                class="ma-2"
                color="blue-grey"
                tile
                dark
                :to="'/run?tgt='+item.minion_id"
            >
              run job
            </v-btn>
            <v-btn
                small
                class="ma-2"
                color="red"
                tile
                dark
                @click.stop="showDialog(item.minion_id)"
            >
              delete
            </v-btn>
          </div>
        </template>
      </v-data-table>
    </v-card>
    <div class="text-center">
      <v-dialog
          v-model="dialog"
          width="500"
      >
        <v-card>
          <v-card-title
              class="headline red"
              primary-title
          >
            Delete {{ target }} ?
          </v-card-title>

          <v-card-text>
            <br>
            If you delete {{ target }} from the database, you will need to refresh all minions.
          </v-card-text>

          <v-divider></v-divider>

          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn
                color="primary"
                text
                @click="dialog = false"
            >
              close
            </v-btn>
            <v-btn
                color="red"
                text
                @click="deleteMinion(target)"
            >
              delete
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>
    </div>
  </v-container>
</template>

<script>

  export default {
    name: "MinionsTable",
    data() {
      return {
        search: "",
        dialog: false,
        headers: [
          { text: "Minion Id", value: "minion_id" },
          { text: "Highstate Conformity", value: "conformity" },
          { text: "F.Q.D.N", value: "fqdn" },
          { text: "O.S", value: "os" },
          { text: "O.S Version", value: "oscodename" },
          { text: "Kernel", value: "kernelrelease" },
          { text: "Last Job", value: "last_job" },
          { text: "Last Highstate", value: "last_highstate" },
          { text: "Actions", value: "action", sortable: false },
        ],
        minions: [],
        target: null,
        loading: true,
      }
    },
    mounted() {
      this.loadData()
    },
    methods: {
      loadData() {
        this.$http.get("api/minions/").then(response => {
          function addedGrains(data) {
            data.forEach(min => {
              let grain = JSON.parse(min.grain)
              for (let key in grain) {
                min[key] = grain[key]
              }
            })
            return data
          }

          this.minions = addedGrains(response.data)
          this.loading = false
        })
      },
      boolRepr(bool) {
        if (bool === "True") {
          return "green"
        } else if (bool === "False") {
          return "red"
        } else return "primary"
      },
      refreshMinion(minion_id) {
        this.$toast("refreshing " + minion_id)
        let formData = new FormData
        formData.set("minion_id", minion_id)
        this.$http.post("/api/minions/refresh_minions/", formData).then(response => {
          this.$toast(response.data.result)
        }).catch((error) => {
          this.$toast.error(error.response.data)
        })
      },
      deleteMinion(minion_id) {
        this.dialog = false
        this.$http.delete("/api/minions/" + minion_id).then(() => {
          this.minions.splice(this.minions.indexOf(minion_id), 1)
          this.$toast(minion_id + " deleted")
        }).catch((error) => {
          this.$toast.error(error.response.data)
        })
      },
      showDialog(minion_id) {
        this.target = minion_id
        this.dialog = true
      },
    },
  }
</script>

<style scoped>

</style>