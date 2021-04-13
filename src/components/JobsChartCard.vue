<template>
  <v-container fluid>
    <v-card :elevation="minion == null ? 2 : 0">
      <v-list-item three-line dense>
        <v-list-item-content>
          <v-list-item-title class="headline mb-1">Jobs Stats</v-list-item-title>
        </v-list-item-content>
        <v-spacer></v-spacer>
        <v-list-item-content class="mr-6">
          <v-select
              :items="filters"
              label="Filter"
              v-model="settings.Home.JobsChartCard.filter"
              @change="updateSettings"
          ></v-select>
        </v-list-item-content>
        <v-list-item-content>
          <v-select
              :items="periods"
              label="Period"
              v-model="settings.Home.JobsChartCard.period"
              @change="updateSettings"
          ></v-select>
        </v-list-item-content>

      </v-list-item>
      <canvas ref="chart"></canvas>
    </v-card>
  </v-container>
</template>

<script>
import Chart from "chart.js"
import gradientLinePlugin from "../assets/js/utils/chart-line-gradient"
import { mapState } from "vuex"

export default {
  name: "JobsChartCard",
  props: ["minion"],
  data() {
    return {
      filters: [{ text: "All", value: "all" }, { text: "Highstate", value: "highstate" }, {
        text: "Other",
        value: "other",
      }],
      periods: [{ text: "Week", value: 7 }, { text: "Two Weeks", value: 14 }, { text: "Month", value: 30 }, {
        text: "Year",
        value: 365,
      }],
      jobchart: null,
      labels: null,
      chart_data: [],
    }
  },
  computed: {
    ...mapState({
      settings: state => state.settings,
    }),
  },
  mounted() {
    this.createChart()
  },
  methods: {
    updateSettings() {
      this.$store.commit("updateSettings")
      this.loadData()
    },
    loadData() {
      let params = { params: { fun: this.settings.Home.JobsChartCard.filter, period: this.settings.Home.JobsChartCard.period } }
      if (this.minion) {
        params.params.id = this.minion
      }
      this.$http.get("api/jobs/graph", params).then(response => {
        this.jobchart.data.labels = response.data.labels
        this.jobchart.data.datasets[0].data = response.data.series[0]
        this.jobchart.data.datasets[1].data = response.data.series[1]
        this.jobchart.update()
      })
    },
    createChart() {
      let params = { params: { fun: this.settings.Home.JobsChartCard.filter, period: this.settings.Home.JobsChartCard.period } }
      if (this.minion) {
        params.params.id = this.minion
      }
      if (this.jobchart != null) {
        this.jobchart.destroy()
      }
      this.$http.get("api/jobs/graph", params).then(response => {
        this.labels = response.data.labels
        this.chart_data[0] = response.data.series[0]
        this.chart_data[1] = response.data.series[1]
        this.$refs.chart.height = 60
        this.jobchart = new Chart(this.$refs.chart, {
          type: "line",
          data: {
            labels: this.labels,
            datasets: [{
              lineTension: 0.1,
              pointRadius: 1,
              data: this.chart_data[0], // fake data before update(needed for plugin).
              fill: false,
              colorStart: "rgba(0, 173, 238, 1.0)",
              colorEnd: "rgba(231, 18, 143, 1.0)",
            }, {
              lineTension: 0.1,
              pointRadius: 1,
              data: this.chart_data[1],
              fill: false,
              colorStart: "rgba(255, 255, 255, 1.0)",
              colorEnd: "rgba(255, 0, 0, 1.0)",
            }],
          },
          options: {
            linearGradientLine: true,
            legend: {
              display: false,
            },
            scales: {
              xAxes: [{
                gridLines: {
                  display: true,
                },
              }],
              yAxes: [{
                gridLines: {
                  display: true,
                },
                ticks: {
                  autoSkip: true,
                  beginAtZero: true,
                  maxTicksLimit: 6,
                },
              }],
            },
            responsive: true,
          },
          plugins: [gradientLinePlugin],
        })
      })
    },
  },
}
</script>

<style scoped>

</style>