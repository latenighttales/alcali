<template>
  <v-container fluid>
    <v-row>
      <v-col sm="12" lg="7">
        <ConformityChart :key="master"></ConformityChart>
      </v-col>
      <v-col sm="6" lg="2">
        <KeysStatusCard :key="master"></KeysStatusCard>
      </v-col>
      <v-col sm="6" lg="3">
        <AlcaliStatusCard :key="master"></AlcaliStatusCard>
      </v-col>
    </v-row>
    <v-row>
      <v-col lg="12">
        <JobsChartCard :key="master"></JobsChartCard>
      </v-col>
    </v-row>
    <v-row>
      <v-col lg="12">
        <JobsTable :key="master" :filter="{limit: 10}"></JobsTable>
      </v-col>
    </v-row>

  </v-container>
</template>

<script>
  // @ is an alias to /src

  import KeysStatusCard from "../components/KeysStatusCard"
  import JobsChartCard from "../components/JobsChartCard"
  import AlcaliStatusCard from "../components/AlcaliStatusCard"
  import ConformityChart from "../components/ConformityChart"
  import JobsTable from "../components/JobsTable"

  export default {
    name: "home",
    props: {
      master: Number,
    },
    components: {
      JobsTable,
      ConformityChart,
      AlcaliStatusCard,
      KeysStatusCard,
      JobsChartCard,
    },
  }
</script>
