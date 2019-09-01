<template>
  <v-app>
    <app-layout v-if="!layout"></app-layout>
    <simple-layout v-else></simple-layout>
  </v-app>
</template>
<script>

  import Layout from "./components/core/Layout";
  import SimpleLayout from "./components/core/SimpleLayout";

  export default {
    computed: {
      layout() {
        return this.$route.meta.plainLayout
      }
    },
    components: {
      'app-layout': Layout,
      'simple-layout': SimpleLayout
    }
  }
</script>
<style>
  html {
    overflow-y: auto !important
  }
</style>
