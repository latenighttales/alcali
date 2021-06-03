<template>
  <v-container fluid>
    <v-card>
      <v-card-title>{{minion.id}}</v-card-title>
      <v-tabs
          v-model="tab"
      >
        <v-tabs-slider></v-tabs-slider>

        <v-tab href="#common">
          {{$t('components.InfosCard.Common')}}
        </v-tab>

        <v-tab href="#salt">
          {{$t('components.InfosCard.Salt')}}
        </v-tab>

        <v-tab href="#hardware">
          {{$t('components.InfosCard.Hardware')}}
        </v-tab>
      </v-tabs>
      <v-tabs-items v-model="tab">
        <v-tab-item id="common">
          <v-simple-table>
            <tbody>
            <tr v-for="item in common" :key="item.name">
              <td>{{ $t(item.name) }}</td>
              <td v-if="item.grain === 'last_job' || item.grain === 'last_highstate' && minion[item.grain] !== null"
                  class="text-right">{{ new Date(minion[item.grain]).toLocaleString("en-GB")}}
              </td>
              <td v-else-if="item.grain === 'conformity'" class="text-right"><v-chip :color="boolRepr(minion[item.grain])" dark>{{ minion[item.grain] == null ? "unknown": minion[item.grain] }}</v-chip></td>
              <td v-else class="text-right">{{minion[item.grain]}}</td>
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
  </v-container>
</template>

<script>
  export default {
    name: "InfosCard",
    data() {
      return {
        tab: null,
        common: [
          { name: 'components.InfosCard.FQDN', grain: "fqdn" },
          { name: 'components.InfosCard.OS', grain: "os" },
          { name: 'components.InfosCard.OSVersion', grain: "oscodename" },
          { name: 'components.InfosCard.Kernel', grain: "kernelrelease" },
          { name: 'components.InfosCard.LastJob', grain: "last_job" },
          { name: 'components.InfosCard.LastHighstate', grain: "last_highstate" },
          { name: 'components.InfosCard.HighstateConformity', grain: "conformity" },
        ],
        salt: [
          { name: "ID", grain: "id" },
          { name: 'components.InfosCard.Master', grain: "master" },
          { name: 'components.InfosCard.SaltVersion', grain: "saltversion" },
          { name: 'components.InfosCard.SaltPath', grain: "saltpath" },
          { name: 'components.InfosCard.PythonVersion', grain: "pythonversion" },
        ],
        hardware: [
          { name: 'components.InfosCard.CPUModel', grain: "cpu_model" },
          { name: 'components.InfosCard.CPUNumber', grain: "num_cpus" },
          { name: 'components.InfosCard.TotalMemory', grain: "mem_total" },
          { name: 'components.InfosCard.TotalSwap', grain: "swap_total" },
          { name: 'components.InfosCard.Virtual', grain: "virtual" },
        ],
      }
    },
    props: ["minion"],
    methods: {
      boolRepr(bool) {
        if (bool === "True") {
          return "green"
        } else if (bool === "False") {
          return "red"
        } else return "primary"
      },
    },
  }
</script>

<style scoped>

</style>