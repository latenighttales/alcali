<template>
  <v-container fluid>
    <v-card>
      <v-card-title>
        {{ $t('components.ConformityDetailCard.HighstateConformity') }}
        <v-spacer></v-spacer>
        <v-checkbox
            class="mb-0 mt-0"
            v-show="Object.keys(succeeded).length>0"
            color="green"
            v-model="succeeded_checkbox"
            :label="`${$t('components.ConformityTable.Succeeded')}: ${Object.keys(succeeded).length}`"
        ></v-checkbox>
        <v-checkbox
            v-show="Object.keys(unchanged).length>0"
            class="ml-3 mb-0 mt-0"
            color="orange"
            v-model="unchanged_checkbox"
            :label="`${$t('components.ConformityTable.Unchanged')}: ${Object.keys(unchanged).length}`"
        ></v-checkbox>
        <v-checkbox
            v-show="Object.keys(failed).length>0"
            class="ml-3 mb-0 mt-0"
            color="red"
            v-model="failed_checkbox"
            :label="`${$t('components.ConformityTable.Failed')}: ${Object.keys(failed).length}`"
        ></v-checkbox>
      </v-card-title>
      <v-expansion-panels>
        <v-expansion-panel
            v-if="succeeded_checkbox"
            v-for="(item,i) in succeeded"
            :key="i"
            dark
        >
          <v-expansion-panel-header>{{i}}
            <template v-slot:actions>
              <v-icon color="green">$vuetify.icons.expand</v-icon>
            </template>
          </v-expansion-panel-header>
          <v-expansion-panel-content v-html="item">
          </v-expansion-panel-content>
        </v-expansion-panel>
      </v-expansion-panels>

      <v-expansion-panels>
        <v-expansion-panel
            v-if="unchanged_checkbox"
            v-for="(item,i) in unchanged"
            :key="i"
        >
          <v-expansion-panel-header>{{i}}
            <template v-slot:actions>
              <v-icon color="orange">$vuetify.icons.expand</v-icon>
            </template>
          </v-expansion-panel-header>
          <v-expansion-panel-content v-html="item">
          </v-expansion-panel-content>
        </v-expansion-panel>
      </v-expansion-panels>

      <v-expansion-panels>
        <v-expansion-panel
            v-if="failed_checkbox"
            v-for="(item,i) in failed"
            :key="i"
        >
          <v-expansion-panel-header>{{i}}
            <template v-slot:actions>
              <v-icon color="red">$vuetify.icons.expand</v-icon>
            </template>
          </v-expansion-panel-header>
          <v-expansion-panel-content v-html="item">
          </v-expansion-panel-content>
        </v-expansion-panel>
      </v-expansion-panels>
    </v-card>
  </v-container>
</template>

<script>
  export default {
    name: "ConformityDetailCard",
    props: ["succeeded", "unchanged", "failed"],
    data() {
      return {
        expand_search: false,
        succeeded_checkbox: true,
        unchanged_checkbox: true,
        failed_checkbox: true,
      }
    },
  }
</script>

<style scoped>
  .v-expansion-panel-content {
    background-color: black;
  }


</style>