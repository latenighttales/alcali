<template>
  <v-container fluid>
    <v-card>
      <v-card-title>
        Minions
        <v-spacer></v-spacer>
        <v-menu
            v-model="menu"
            :close-on-content-click="false"
            offset-y
            offset-x
            left
        >
          <template v-slot:activator="{ on }">
            <v-btn
                color="primary"
                dark
                v-on="on"
                class="mr-5"
            >
              Columns
            </v-btn>
          </template>

          <v-card flat max-width="700">
            <v-card-text>
              <v-container fluid>
                <v-row no-gutters>
                  <template v-for="(item, index) in available_headers">
                    <v-col :key="index" cols="4">
                      <v-checkbox :label="item" :value="item" v-model="settings.MinionsTable.table.columns" @change="updateSettings" hide-details></v-checkbox>
                    </v-col>
                  </template>
                </v-row>
              </v-container>
            </v-card-text>
          </v-card>
        </v-menu>
        <v-text-field
            v-model="search"
            append-icon="search"
            label="Search"
            single-line
            hide-details
            class="search"
        ></v-text-field>
      </v-card-title>
      <v-data-table
          :sort-by.sync="settings.MinionsTable.table.sortBy"
          @update:sort-by="updateSettings"
          :headers="customHeaders"
          :sort-desc.sync="settings.MinionsTable.table.sortDesc"
          @update:sort-desc="updateSettings"
          :items="minions"
          :items-per-page.sync="settings.MinionsTable.table.itemsPerPage"
          @update:items-per-page="updateSettings"
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

  import { mapState } from "vuex"

  export default {
    name: "MinionsTable",
    data() {
      return {
        search: "",
        dialog: false,
        default_headers: ["minion_id", "conformity", "fqdn", "os", "oscodename", "kernelrelease", "last_job", "last_highstate"],
        unwanted_headers: ["pillar", "grain", "id"],
        available_headers: [],
        minions: [],
        menu: false,
        target: null,
        loading: true,
      }
    },
    computed: {
      customHeaders() {
        let custom = []
        this.settings.MinionsTable.table.columns.forEach(header => {
          let titled = header.split("_").map(title => title.replace(/^\w/, c => c.toUpperCase())).join(" ")
          custom.push({ text: titled, value: header })
        })
        custom.push({ text: "Actions", value: "action", sortable: false })
        return custom
      },
      ...mapState({
        settings: state => state.settings
      })
    },
    mounted() {
      this.loadData()
    },
    methods: {
      updateSettings() {
        this.$store.commit('updateSettings')
      },
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
          // Compute available headers
          this.available_headers = this.available_headers.concat(this.default_headers)
          if (this.minions.length > 0) {
            Object.keys(this.minions[0]).forEach(key => {
              if (typeof this.minions[0][key] === "string" && !this.default_headers.includes(key) && !this.unwanted_headers.includes(key) && !key.startsWith("lsb")) {
                this.available_headers.push(key)
              }
            })
          }
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
        this.$http.delete(`/api/minions/${minion_id}/`).then(() => {
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