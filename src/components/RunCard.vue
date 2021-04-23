<template>
  <v-container fluid>
    <v-row no-gutters>
      <v-col sm="12">
        <v-card class="mb-8">
          <v-card-title>Run</v-card-title>
          <v-tabs
              v-model="settings.RunCard.tab"
              @change="updateSettings"
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
          <v-tabs-items v-model="settings.RunCard.tab">
            <v-tab-item id="formatted" eager>
              <v-card>
                <v-spacer></v-spacer>
                <v-card-text>
                  <v-container fluid>
                    <v-row>
                      <v-col sm="3" lg="1" align-self="center" class="text-right">
                        <span>Client Type:</span>
                      </v-col>
                      <v-col sm="3" lg="1">
                        <v-select
                            :items="client"
                            v-model="selected_client"
                        ></v-select>
                      </v-col>
                      <v-col sm="3" lg="1" offset-lg="1" v-if="!client_batch && !scheduleSwitch">
                        <v-checkbox v-model="client_async" label="Async" color="primary"></v-checkbox>
                      </v-col>
                      <v-col sm="3" lg="1" :offset-lg="client_batch ? 3: 1"
                             v-if="selected_client === 'local' && !scheduleSwitch">
                        <v-checkbox v-model="client_batch" label="Batch" color="primary"></v-checkbox>
                      </v-col>
                      <v-col sm="3" lg="1" v-if="selected_client === 'local' && client_batch && !scheduleSwitch">
                        <v-text-field label="Batch" v-model="batch"></v-text-field>
                      </v-col>
                      <v-col sm="3" lg="1" :offset-lg="client_batch ? 0: 1"
                             v-if="selected_client === 'local' && !scheduleSwitch">
                        <v-text-field label="Timeout" v-model="timeout" type="number"></v-text-field>
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
                            v-if="selected_client === 'local'"
                        ></v-text-field>
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
                      <v-col lg="3">
                        <v-text-field label="Arguments" v-model="arg"></v-text-field>
                      </v-col>
                      <v-col lg="4">
                        <v-text-field label="Keyword Arguments" v-model="kwarg"></v-text-field>
                      </v-col>
                    </v-row>
                    <v-row dense>
                      <v-col sm=12 lg="3">
                        <v-row dense>
                          <v-col sm="12">
                            <v-switch v-model="scheduleSwitch" label="Schedule" color="primary"
                                      v-show="selected_client === 'local'"></v-switch>
                          </v-col>
                          <v-col sm="12" v-show="scheduleSwitch">
                            <v-text-field label="Schedule Name" v-model="scheduleName"
                                          style="width: 350px;"></v-text-field>
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
                          </v-col>
                        </v-row>
                      </v-col>
                      <v-col sm=12 lg="6">
                        <v-row dense>
                          <v-col sm="12">
                            <v-switch v-model="pillarSwitch" label="Pillar" color="primary"
                                      v-show="selected_client === 'local'"></v-switch>
                          </v-col>
                          <v-col sm="12" v-show="pillarSwitch">
                            <codemirror v-model="code" :options="cmOptions"></codemirror>
                          </v-col>
                          <v-col sm="12" v-show="pillarSwitch">
                            <span v-html="pillarRendered"></span>
                          </v-col>
                        </v-row>
                      </v-col>
                      <v-col sm=12 lg="3">
                        <v-row dense>
                          <v-col sm="12">
                            <v-switch v-model="saveJobSwitch" label="Save as template" color="primary"></v-switch>
                          </v-col>
                          <v-col sm="12" v-show="saveJobSwitch">
                            <v-text-field label="Job Template Name" v-model="jobTemplateName"
                                          style="width: 350px;"></v-text-field>
                          </v-col>
                        </v-row>
                      </v-col>
                    </v-row>
                  </v-container>
                </v-card-text>
                <v-card-actions>
                  <v-spacer></v-spacer>
                  <v-btn color="orange" large dark @click="runJob(test=true)" v-show="!saveJobSwitch">Test</v-btn>
                  <v-btn color="info" large dark @click="runJob" v-show="!saveJobSwitch">Run</v-btn>
                  <v-btn color="green" large dark @click="saveJob" v-show="saveJobSwitch">Save</v-btn>
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
// require component
import { codemirror } from "vue-codemirror"

import "codemirror/addon/display/autorefresh.js"
import "codemirror/addon/fold/foldcode.js"
import "codemirror/addon/fold/brace-fold.js"
import "codemirror/addon/fold/foldgutter.js"
import "codemirror/addon/fold/indent-fold.js"
import "codemirror/mode/javascript/javascript.js"

// require styles
import "codemirror/lib/codemirror.css"
// language js
import "codemirror/mode/yaml/yaml.js"
// theme css
import "../assets/css/made-of-code.css"

import yaml from "js-yaml"
import { mapState } from "vuex"

export default {
  name: "RunCard",
  components: { TerminalCard, codemirror },
  data() {
    return {
      scheduleSwitch: false,
      pillarSwitch: false,
      saveJobSwitch: false,
      jobTemplateName: "",
      code: "# Type valid yaml to override pillars\n\n\n",
      cmOptions: {
        tabSize: 4,
        mode: "yaml",
        theme: "made-of-code",
        line: true,
        autoRefresh: true,
        lineNumbers: false,
        foldGutter: true,
        gutters: ["CodeMirror-foldgutter"],
      },
      client: [
        { text: "Local", value: "local" },
        { text: "Runner", value: "runner" },
        { text: "Wheel", value: "wheel" },
      ],
      selected_client: "local",
      client_async: false,
      client_batch: false,
      minions: [],
      functions: null,
      selectedFunction: null,
      description: null,
      batch: null,
      timeout: null,
      target_type: [
        { text: "glob", value: "glob" },
        { text: "pcre", value: "--pcre" },
        { text: "list", value: "--list" },
        { text: "grain", value: "--grain" },
        { text: "grain_pcre", value: "--grain-pcre" },
        { text: "pillar", value: "--pillar" },
        { text: "pillar_pcre", value: "--pillar-pcre" },
        { text: "range", value: "--range" },
        { text: "compound", value: "--compound" },
        { text: "nodegroup", value: "--nodegroup" },
      ],
      selected_target_type: "glob",
      target: "",
      arg: "",
      kwarg: "",
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
    updateSettings() {
      this.$store.commit("updateSettings")
    },
    loadData() {
      this.$http.get("api/functions/").then(response => {
        this.functions = response.data
      })
      this.$http.get("api/minions/").then(response => {
        response.data.forEach(item => this.minions.push(item.minion_id))
      })
    },
    createCommand(test = false) {
      // Client, async options.
      let command = `salt --client=${this.client_batch ? "local_batch" : this.selected_client}${this.client_async && !this.client_batch ? "_async" : ""}`
      // Targeting.
      if (this.selected_client === "local") {
        if (this.selected_target_type !== "glob") command += " " + this.selected_target_type + " " + this.target
        else command += " " + this.target
      }
      // Functions.
      if (this.selectedFunction && this.selectedFunction.hasOwnProperty("name")) {
        command += ` ${this.selectedFunction.name}`
      } else {
        command += ` ${this.selectedFunction}`
      }
      // Args and Kwargs.
      command += `${this.arg ? ` ${this.arg}` : ""}${test === true ? " test=True" : ""}${this.kwarg ? ` ${this.kwarg}` : ""}`
      // Pillar override.
      command += `${this.pillarSwitch ? ` pillar='${this.pillarRendered}'` : ""}`
      // Batch and timeout options.
      command += `${this.client_batch && this.batch ? ` -b ${this.batch}` : ""}${this.timeout ? ` -t ${this.timeout}` : ""}`
      return command
    },
    saveJob() {
      let formData = new FormData
      let command = this.createCommand(false)
      formData.set("name", this.jobTemplateName)
      formData.set("job", command)
      this.$http.post("api/job_templates/", formData).then(response => {
        this.$toast("Template " + this.jobTemplateName + " saved")
      })
    },
    runJob(test = false) {
      let action = "Running"
      let formData = new FormData
      let command = this.createCommand(test)
      formData.set("raw", true)
      formData.set("command", command)
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
      this.$toast(action + " " + command)
      this.$http.post("api/run/", formData).then(response => {
        let result = response.data
        // If we're expecting an async result, display a link to the minion's result.
        if (this.client_async && this.selected_client === "local") {
          let parser = new DOMParser()
          let htmlRes = parser.parseFromString(result, "text/html")
          let resultChild = htmlRes.getElementsByClassName("ansi2html-content")[0].children
          let jid = resultChild[resultChild.length - 1].innerText
          // for all targeted minions.
          for (let i = 1; i < resultChild.length - 2; i++) {
            // create link and add it to html.
            let a = document.createElement("a")
            let linkText = document.createTextNode(resultChild[i].innerText)
            a.appendChild(linkText)
            a.title = `Async result to job for ${resultChild[i].innerText.replace("- ", "")}`
            a.href = `/#/jobs/${jid}/${resultChild[i].innerText.replace("- ", "")}`
            resultChild[i].innerHTML = ""
            resultChild[i].appendChild(a)
          }
          result = new XMLSerializer().serializeToString(htmlRes)
        }
        this.results = result + this.results
      }).catch((error) => {
        this.$toast.error(error.response.data)
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
    pillarRendered: function() {
      return `${JSON.stringify(yaml.safeLoad(this.code) === null ? {} : yaml.safeLoad(this.code))}`
    },
    ...mapState({
      settings: state => state.settings,
    }),
  },
  mounted() {
    this.cron = new CronUI("#cron", {
      initial: "* * * * *",
    })
    this.loadData()
    if (this.$route.query.client) {
      this.selected_client = this.$route.query.client.split("_")[0]
      if (this.$route.query.client.split("_").length > 1) {
        this["client_" + this.$route.query.client.split("_")[1]] = true
      }
    }
    if (this.$route.query.tgt_type) {
      this.target_type.forEach(tgt_type => {
        if (tgt_type.text === this.$route.query.tgt_type) {
          this.selected_target_type = tgt_type.value
        }
      })
    }
    this.batch = this.$route.query.batch ? this.$route.query.batch : null
    this.target = this.$route.query.tgt
    this.selectedFunction = this.$route.query.hasOwnProperty("fun") === true ? { name: this.$route.query.fun } : this.selectedFunction
    this.arg = this.$route.query.arg
    if (this.$route.query.kwarg) {
      let pillar = this.$route.query.kwarg.split(" ").filter(item => {
        return item.startsWith("pillar")
      }).join()
      if (pillar) {
        this.pillarSwitch = true
        this.code = yaml.dump(JSON.parse(pillar.split("=")[1]))
        this.kwarg = this.$route.query.kwarg.split(" ").filter(item => {
          return !item.startsWith("pillar")
        }).join(" ")
      } else {
        this.kwarg = this.$route.query.kwarg
      }
    }
    if (this.$route.query.name) {
      this.saveJobSwitch = true
      this.jobTemplateName = this.$route.query.name
    }
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
