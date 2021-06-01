<template>
  <v-container fluid>
    <v-card>
      <v-card-title>{{ $t('components.ConformityChart.conformity') }}</v-card-title>
      <v-card-text>
        <v-container fluid>
          <template v-for="name in conformitynames">
            <v-row no-gutters :key="name" align="center" justify="center">
              <v-col sm="2">{{name}}</v-col>
              <v-col sm="10">
                <v-menu open-on-hover max-width="250px">
                  <template v-slot:activator="{ on }">
                    <canvas :ref="name" height="15" v-on="on"></canvas>
                  </template>
                  <v-simple-table dense>
                    <thead>
                    <tr>
                      <th>{{name}}</th>
                    </tr>
                    </thead>
                    <tbody v-html="customTool">
                    </tbody>
                  </v-simple-table>
                </v-menu>
              </v-col>
            </v-row>
          </template>
        </v-container>
      </v-card-text>
    </v-card>
  </v-container>
</template>

<script>
  import Chart from "chart.js"
  import "chartjs-plugin-stacked100"

  import colors from "vuetify/lib/util/colors"

  export default {
    name: "ConformityChart",
    data() {
      return {
        conformitynames: null,
        confchart: null,
        conformity: null,
        customTool: "",
      }
    },
    created() {

    },
    mounted() {
      this.loadConformity()
    },
    methods: {
      loadConformity() {
        this.$http.get("api/minions/conformity/").then(response => {
          this.conformity = response.data.data
          this.conformitynames = response.data.name
        }).then(() => {
          this.conformity.forEach((conformity, idx) => {
            let chart_data = {
              labels: [this.conformitynames[idx]],
              datasets: [],
            }
            Object.keys(conformity).forEach((value) => {
              let color = ""
              if (["conflict", "false"].indexOf(value) >= 0) {
                color = "#F44336"
              } else if (["conform", "true"].indexOf(value) >= 0) {
                color = "#41f40e"
              } else if (["None", "unknown", "null"].indexOf(value) >= 0) {
                color = this.$vuetify.theme.themes.light.primary
              } else {
                let keys = Object.keys(colors)
                color = colors[keys[keys.length * Math.random() << 0]].darken2
              }
              chart_data.datasets.push({
                label: this.$i18n.t(`components.ConformityChart.${value}`),
                data: [conformity[value]],
                backgroundColor: color,
              })
            })
            new Chart(this.$refs[this.conformitynames[idx]], {
              type: "horizontalBar",
              data: chart_data,
              options: {
                animation: false,
                plugins: {
                  stacked100: { enable: true },
                },
                tooltips: {
                  enabled: false,
                  mode: "index",
                  intersect: false,
                  custom: (tooltip) => {
                    if (!tooltip) {
                      return
                    }
                    if (tooltip.body) {
                      let bodyLines = tooltip.body.map(lines => lines.lines)

                      let innerHtml = ""

                      bodyLines.forEach(function(body, i) {
                        let colors = tooltip.labelColors[i]
                        let style = "background:" + colors.backgroundColor
                        style += "; border-color:" + colors.borderColor
                        style += "; border-width: 2px"
                        let span = `<span class="chartjs-tooltip-key" style="${style}">__</span>`
                        innerHtml += "<tr><td>" + span + "  " + body + "</td></tr>"
                      })
                      this.customTool = innerHtml
                    }
                  },
                },
                legend: { display: false },
                scales: {
                  xAxes: [{
                    stacked: true,
                    display: false, //this will remove all the x-axis grid lines
                    gridLines: {
                      display: false,
                      drawTicks: false,
                      drawBorder: false,
                    },
                    ticks: {
                      display: false,
                      padding: -20,
                    },
                  }],
                  yAxes: [{
                    stacked: true,
                    display: false, //this will remove all the x-axis grid lines
                    ticks: {
                      display: false,
                      padding: -20,
                    },
                    gridLines: {
                      drawTicks: false,
                      display: false,
                      drawBorder: false,
                    },
                  }],
                },
              },
            })
          })
        })
      },
    },
  }
</script>

<style scoped>
  .v-menu--inline {
    display: block;
  }

  .chartjs-tooltip-key {
    display: inline-block;
    width: 10px;
    height: 10px;
    margin-right: 10px;
  }

</style>