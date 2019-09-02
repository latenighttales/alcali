<template>
  <v-container>
    <v-card>
      <v-tabs
          v-model="tab"
      >
        <v-tabs-slider></v-tabs-slider>

        <v-tab href="#grain">
          Grains
        </v-tab>

        <v-tab href="#pillar">
          Pillar
        </v-tab>
        <v-tab href="#history">
          History
        </v-tab>
        <v-tab href="#graph">
          Graph
        </v-tab>
        <v-tab v-for="field in minion.custom_fields" v-bind:key="field.name">
          {{field.name}}
        </v-tab>
      </v-tabs>
      <v-tabs-items v-model="tab">
        <v-tab-item id="grain">
          <codemirror v-model="code" :options="cmOptions"></codemirror>
        </v-tab-item>
        <v-tab-item id="pillar">
          <codemirror v-model="codepillar" :options="cmOptions"></codemirror>
        </v-tab-item>
        <v-tab-item id="history">
          <JobsTable :filter="{'target[]': minion.minion_id}"></JobsTable>
        </v-tab-item>
        <v-tab-item id="graph" eager>
          <JobsChartCard v-if="minion" :minion="minion.minion_id"></JobsChartCard>
        </v-tab-item>
        <v-tab-item v-for="field in minion.custom_fields" v-bind:key="field.name">
          <codemirror :options="cmOptions" :value="yamlRepr(field.value)"></codemirror>
        </v-tab-item>
      </v-tabs-items>
    </v-card>
  </v-container>
</template>

<script>

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
  import JobsChartCard from "./JobsChartCard"
  import JobsTable from "./JobsTable"

  export default {
    name: "MinionDetailCard",
    components: {
      JobsTable,
      JobsChartCard,
      codemirror,
    },
    data() {
      return {
        tab: null,
        code: yaml.safeDump(JSON.parse(this.minion.grain)),
        codepillar: yaml.safeDump(JSON.parse(this.minion.pillar)),
        cmOptions: {
          tabSize: 4,
          mode: "yaml",
          theme: "made-of-code",
          line: true,
          autoRefresh: true,
          lineNumbers: false,
          readOnly: true,
          cursorBlinkRate: 0,
          //viewportMargin: Infinity,
          foldGutter: true,
          gutters: ["CodeMirror-foldgutter"],
        },
      }
    },
    methods: {
      yamlRepr(data) {
        return yaml.safeDump(JSON.parse(data))
      },
    },
    props: ["minion"],
  }
</script>

<style scoped>

</style>