<template>
  <v-card>
    <v-card-title>Infos</v-card-title>
    <v-tabs
        v-model="tab"
    >
      <v-tabs-slider></v-tabs-slider>

      <v-tab href="#common">
        Common
      </v-tab>

      <v-tab href="#salt">
        Salt
      </v-tab>

      <v-tab href="#hardware">
        Hardware
      </v-tab>
    </v-tabs>
    <v-tabs-items v-model="tab">
      <v-tab-item id="common">
        <v-simple-table>
          <tbody>
          <tr v-for="item in common" :key="item.name">
            <td>{{ item.name }}</td>
            <td class="text-right">{{minion[item.grain]}}</td>
          </tr>
          </tbody>
        </v-simple-table>
      </v-tab-item>
      <v-tab-item id="salt">
        <v-simple-table>
          <tbody>
          <tr v-for="item in salt" :key="item.name">
            <td>{{ item.name }}</td>
            <td class="text-right">{{minion[item.grain]}}</td>
          </tr>
          </tbody>
        </v-simple-table>
      </v-tab-item>
      <v-tab-item id="hardware">
        <v-simple-table>
          <tbody>
          <tr v-for="item in hardware" :key="item.name">
            <td>{{ item.name }}</td>
            <td class="text-right">{{minion[item.grain]}}</td>
          </tr>
          </tbody>
        </v-simple-table>
      </v-tab-item>
    </v-tabs-items>
  </v-card>

</template>

<script>
  export default {
    name: "InfosCard",
    data() {
      return {
        tab: null,
        common: [
          {name: "F.Q.D.N", grain: "fqdn"},
          {name: "O.S", grain: "os"},
          {name: "O.S Version", grain: "oscodename"},
          {name: "Kernel", grain: "kernelrelease"},
          {name: "Last Job", grain: "last_job"},
          {name: "Last Highstate", grain: "last_highstate"},
          {name: "Conformity", grain: "conformity"},
        ],
        salt: [
          {name: "ID", grain: "id"},
          {name: "Master", grain: "master"},
          {name: "Salt Version", grain: "saltversion"},
          {name: "Salt Path", grain: "saltpath"},
          {name: "Python Version", grain: "pythonversion"},
        ],
        hardware: [
          {name: "C.P.U Model", grain: "cpu_model"},
          {name: "Number of C.P.U", grain: "num_cpus"},
          {name: "Total Memory", grain: "mem_total"},
          {name: "Total Swap", grain: "swap_total"},
          {name: "Virtual", grain: "virtual"},
        ]
      }
    },
    props: ['minion'],
  }
</script>

<style scoped>

</style>