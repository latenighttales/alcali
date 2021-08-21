<template>
  <v-container fluid>
    <v-card>
      <v-tabs
          v-model="settings.MinionDetail.MinionDetailCard.tab"
          @change="updateSettings"
      >
      <v-tabs-slider></v-tabs-slider>

        <v-tab href="#grain">
          {{ $t("components.MinionDetailCard.Grains") }}
        </v-tab>

        <v-tab href="#pillar">
          {{ $t("components.MinionDetailCard.Pillar") }}
        </v-tab>
        <v-tab href="#history">
          {{ $t("components.MinionDetailCard.History") }}
        </v-tab>
        <v-tab href="#graph">
          {{ $t("components.MinionDetailCard.Graph") }}
        </v-tab>
        <v-tab v-for="field in minion.custom_fields" v-bind:key="field.name">
          {{ field.name }}
        </v-tab>
      </v-tabs>
      <v-tabs-items v-model="settings.MinionDetail.MinionDetailCard.tab">
        <v-tab-item id="grain">
          <div class="text-right">
            <v-btn @click="fold('grainCm')" class="overlayedBtn">{{
              grainCmFolded ? $t("components.MinionDetailCard.Unfold") : $t("components.MinionDetailCard.Fold")
            }}</v-btn>
          </div>
          <codemirror v-model="code" ref="grainCm" :options="cmOptions"></codemirror>
        </v-tab-item>
        <v-tab-item id="pillar">
          <div class="text-right">
            <v-btn @click="fold('pillarCm')" class="overlayedBtn">{{
              pillarCmFolded ? $t("components.MinionDetailCard.Unfold") : $t("components.MinionDetailCard.Fold")
            }}</v-btn>
          </div>
          <codemirror v-model="codepillar" ref="pillarCm" :options="cmOptions"></codemirror>
        </v-tab-item>
        <v-tab-item id="history">
          <JobsTable :filter="{ 'target[]': minion.minion_id }"></JobsTable>
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
import CodeMirror from "codemirror";
import { codemirror } from "vue-codemirror";
import { mapState } from "vuex"

import "codemirror/addon/display/autorefresh.js";
import "codemirror/addon/fold/foldcode.js";
import "codemirror/addon/fold/brace-fold.js";
import "codemirror/addon/fold/foldgutter.js";
import "codemirror/addon/fold/indent-fold.js";
import "codemirror/mode/javascript/javascript.js";

// require styles
import "codemirror/lib/codemirror.css";
// language js
import "codemirror/mode/yaml/yaml.js";
// theme css
import "../assets/css/made-of-code.css";

import yaml from "js-yaml";
import JobsChartCard from "./JobsChartCard";
import JobsTable from "./JobsTable";

export default {
  name: "MinionDetailCard",
  components: {
    JobsTable,
    JobsChartCard,
    codemirror,
  },
  data() {
    return {
      code: yaml.safeDump(JSON.parse(this.minion.grain)),
      codepillar: yaml.safeDump(JSON.parse(this.minion.pillar)),
      grainCmFolded: false,
      pillarCmFolded: false,
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
    };
  },
  methods: {
    updateSettings() {
      this.$store.commit("updateSettings")
    },
    yamlRepr(data) {
      return yaml.safeDump(JSON.parse(data));
    },
    fold(ref) {
      if (this[ref + "Folded"] === true) {
        CodeMirror.commands.unfoldAll(this.$refs[ref].codemirror);
        this[ref + "Folded"] = false;
      } else {
        CodeMirror.commands.foldAll(this.$refs[ref].codemirror);
        this[ref + "Folded"] = true;
      }
    },
  },
  computed: {
    ...mapState({
      settings: state => state.settings,
    }),
  },
  props: ["minion"],
};
</script>

<style scoped>
.overlayedBtn {
  position: absolute;
  right: 0;
  z-index: 1;
}
</style>
