<template>
  <v-container>
    <v-row no-gutters>
      <v-col sm="12">
        <v-card class="mb-8">
          <v-card-title>Run</v-card-title>
          <v-tabs
              v-model="tab"
          >
            <v-tabs-slider></v-tabs-slider>

            <v-tab href="#formatted">
              Formatted
            </v-tab>
            <v-tab
                href="#cli"
            >
              Cli
            </v-tab>
          </v-tabs>
          <v-tabs-items v-model="tab">
            <v-tab-item id="formatted" eager>
              <v-card>
                <v-spacer></v-spacer>
                <v-card-text>
                  <v-container>
                    <v-row>
                      <v-col cols="12" sm="6" lg="1" align-self="center" class="text-right">
                        <span>Client Type:</span>
                      </v-col>
                      <v-col cols="12" sm="6" lg="2">
                        <v-select
                            :items="client"
                            v-model="selected_client"
                        ></v-select>
                      </v-col>
                    </v-row>
                    <v-row>
                      <v-col lg="1">
                        <v-select
                            :items="target_type"
                            label="Target Type"
                            v-model="selected_target_type"
                            v-if="selected_client === 'local'"
                            @change="target = null"
                        ></v-select>
                      </v-col>
                      <v-col lg="2">
                        <v-text-field
                            label="Target"
                            v-model="target"
                            v-if="selected_client === 'local' && selected_target_type=== 'custom'"
                        ></v-text-field>
                        <v-select
                            :items="minions"
                            v-model="target"
                            v-if="selected_client === 'local' && selected_target_type=== 'single'"
                        ></v-select>
                      </v-col>
                      <v-col lg="2">
                        <v-combobox
                            v-model="selectedFunction"
                            item-value="name"
                            item-text="name"
                            :items="filteredFunction"
                            label="Function"
                            return-object
                        >
                          <template v-slot:append-outer v-if="selectedFunction">
                            <v-menu offset-y>
                              <template v-slot:activator="{ on }">
                                <v-icon
                                    color="black"
                                    v-on="on"
                                >info
                                </v-icon>
                              </template>
                              <div class="desc">
                                <pre>{{ selectedFunction.description }}</pre>
                              </div>
                            </v-menu>
                          </template>
                        </v-combobox>
                      </v-col>
                      <v-col lg="2">
                        <v-text-field label="Arguments" v-model="args"></v-text-field>
                      </v-col>
                      <v-col lg="2">
                        <v-text-field label="Keyword"></v-text-field>
                      </v-col>
                      <v-col lg="2">
                        <v-text-field label="Argument"></v-text-field>
                      </v-col>
                    </v-row>
                    <v-row dense>
                      <v-col sm="12">
                        <v-switch v-model="scheduleSwitch" label="Schedule" color="primary"
                                  v-show="selected_client === 'local'"></v-switch>
                        <div v-show="scheduleSwitch">
                          <v-text-field label="Schedule name" v-model="scheduleName" style="width: 350px;"></v-text-field>
                          <v-radio-group v-model="scheduleType" class="mt-0">
                            <v-radio value="once" color="primary">
                              <template v-slot:label>
                                <span><strong>Once:  </strong></span>
                                <v-row>
                                  <v-col sm="4" class="ml-2">
                                    <v-menu
                                        v-model="dateMenu"
                                        :close-on-content-click="false"
                                        transition="scale-transition"
                                        offset-y
                                        full-width
                                        min-width="290px"
                                    >
                                      <template v-slot:activator="{ on }">
                                        <v-text-field
                                            v-model="scheduleDate"
                                            readonly
                                            v-on="on"
                                        ></v-text-field>
                                      </template>
                                      <v-date-picker :min="scheduleDate" v-model="scheduleDate"
                                                     @input="dateMenu = false"></v-date-picker>
                                    </v-menu>
                                  </v-col>
                                  <v-col sm="4">
                                    <v-menu
                                        ref="menu"
                                        v-model="timeMenu"
                                        :close-on-content-click="false"
                                        :nudge-right="40"
                                        transition="scale-transition"
                                        offset-y
                                        full-width
                                        max-width="290px"
                                        min-width="290px"
                                    >
                                      <template v-slot:activator="{ on }">
                                        <v-text-field
                                            v-model="scheduleTime"
                                            readonly
                                            v-on="on"
                                        ></v-text-field>
                                      </template>
                                      <v-time-picker
                                          v-if="timeMenu"
                                          v-model="scheduleTime"
                                          full-width
                                      ></v-time-picker>
                                    </v-menu>
                                  </v-col>
                                </v-row>
                              </template>
                            </v-radio>
                            <v-radio value="recurring" color="primary">
                              <template v-slot:label>
                                <div><strong>Recurring: </strong> Every <span id="cron"></span></div>
                              </template>
                            </v-radio>
                          </v-radio-group>
                        </div>
                      </v-col>
                    </v-row>
                  </v-container>
                </v-card-text>
                <v-card-actions>
                  <v-spacer></v-spacer>
                  <v-btn color="orange" large dark @click="runJob(test=true)">Test</v-btn>
                  <v-btn color="info" large dark @click="runJob">Run</v-btn>
                </v-card-actions>
              </v-card>
            </v-tab-item>
            <v-tab-item id="cli">
              <TerminalCard v-if="functions !== null" :minions="minions" :functions="functions"></TerminalCard>
            </v-tab-item>
          </v-tabs-items>
        </v-card>

      </v-col>
    </v-row>
    <v-row>
      <v-col sm="12">
        <v-card v-if="results">
          <v-card-title>Results</v-card-title>
          <v-card-text v-html="results" class="ansiStyle"></v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>

  import TerminalCard from "./TerminalCard"
  import CronUI from "../assets/js/utils/cron-ui"

  export default {
    name: "RunCard",
    components: { TerminalCard },
    data() {
      return {
        scheduleSwitch: false,
        tab: null,
        client: [
          { text: "Local", value: "local" },
          { text: "Local Runner", value: "runner" },
          { text: "Wheel", value: "wheel" },
        ],
        selected_client: "local",
        minions: [],
        functions: null,
        selectedFunction: null,
        description: null,
        target_type: [
          { text: "Single", value: "single" },
          { text: "Group", value: "group" },
          { text: "Custom", value: "custom" },
        ],
        selected_target_type: "custom",
        target: "",
        args: "",
        kwargs: {},
        results: "",
        termKey: 0,
        cron: null,
        dateMenu: false,
        timeMenu: false,
        scheduleType: null,
        scheduleDate: new Date().toISOString().substr(0, 10),
        scheduleTime: new Date().toISOString().substr(11, 11).split(":").slice(0, -1).join(":"),
        scheduleName: null,
      }
    },
    methods: {
      loadData() {
        this.$http.get("api/functions/").then(response => {
          this.functions = response.data
        })
        this.$http.get("api/minions/").then(response => {
          response.data.forEach(item => this.minions.push(item.minion_id))
        })
      },
      runJob(test = false) {
        let formData = new FormData
        let action = "Running"
        formData.set("client", this.selected_client)
        if (this.selected_client === "local") formData.set("target", this.target)
        formData.set("function", this.selectedFunction.name || this.selectedFunction)
        if (test === true) this.kwargs.test = "True"
        if (Object.keys(this.kwargs).length !== 0 && this.kwargs.constructor === Object) {
          for (let key in this.kwargs) {
            formData.set(key, this.kwargs[key])
          }
        }
        if (this.args) formData.set("args", this.args)
        if (this.scheduleSwitch && this.scheduleType) {
          action = "Scheduling"
          formData.set("schedule_type", this.scheduleType)
          if (this.scheduleName) formData.set("schedule_name", this.scheduleName)
          if (this.scheduleType === "once") {
            formData.set("schedule", this.scheduleDate + " " + this.scheduleTime + ":00")
          } else {
            formData.set("cron", this.cron.currentValue)
          }
        }
        this.$toast(action + " " + this.selectedFunction.name || this.selectedFunction + " on " + this.target)
        this.$http.post("api/run/", formData).then(response => {
          this.results = response.data + this.results
        })
      },
    },
    computed: {
      filteredFunction: function() {
        if (this.functions === null) {
          return
        }
        return this.functions.filter((item) => {
          return item.type === this.selected_client
        })
      },
    },
    mounted() {
      this.cron = new CronUI("#cron", {
        initial: "* * * * *",
      })
      this.loadData()
      this.target = this.$route.query.target
      this.selectedFunction = this.$route.query.hasOwnProperty("function") === true ? { name: this.$route.query.function } : this.selectedFunction
      this.args = this.$route.query.args

    },

  }
</script>

<style scoped>


  .desc {
    background-color: rgba(138, 138, 138);
    border: 10px;
    border-right: 20px;
  }

  .ansiStyle {
    background-color: black;
    padding: 10px;
  }

</style>
