<template>
  <v-card>
    <v-card-title>
      Highstate Conformity
      <v-expand-transition>
        <v-text-field
            v-show="expand_search"
            class="mx-auto"
            hide-details
            label="Search"
            solo-inverted
        ></v-text-field>
      </v-expand-transition>
      <v-btn icon @click="expand_search = !expand_search">
        <v-icon>mdi-magnify</v-icon>
      </v-btn>
    </v-card-title>
    <v-expansion-panels>
      <v-expansion-panel
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
</template>

<script>
  export default {
    name: "ConformityDetailCard",
    props: ["succeeded", "unchanged", "failed"],
    data() {
      return {
        expand_search: false,
      }
    },
  }
</script>

<style scoped>
  .v-expansion-panel-content {
    background-color: black;
  }


</style>