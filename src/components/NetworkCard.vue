<template>
  <v-container fluid>
    <v-card>
      <v-card-title>Network</v-card-title>
      <v-tabs
          v-model="tab"
      >
        <v-tabs-slider></v-tabs-slider>

        <v-tab href="#interface">
          Interfaces
        </v-tab>

        <v-tab href="#mac">
          Mac
        </v-tab>

        <v-tab href="#dns">
          Dns
        </v-tab>
      </v-tabs>
      <v-tabs-items v-model="tab">
        <v-tab-item id="interface">
          <v-simple-table>
            <tbody>
            <tr v-for="(val, key) in minion.ip_interfaces" :key="key">
              <td>{{key}}</td>
              <td class="text-right" v-for="iface in val">{{ iface }}</td>
            </tr>
            <tr>
              <td>IPv4 GATEWAY</td>
              <td class="text-right">{{ minion.ip4_gw }}</td>
            </tr>
            <tr>
              <td>IPv6 GATEWAY</td>
              <td class="text-right">{{ minion.ip6_gw }}</td>
            </tr>
            </tbody>
          </v-simple-table>
        </v-tab-item>
        <v-tab-item id="mac">
          <v-simple-table>
            <tbody>
            <tr v-for="(val, key) in minion.hwaddr_interfaces" :key="key">
              <td>{{key}}</td>
              <td class="text-right">{{ val }}</td>
            </tr>
            </tbody>
          </v-simple-table>
        </v-tab-item>
        <v-tab-item id="dns">
          <v-simple-table>
            <tbody>
            <tr v-for="(val, key) in minion.dns" :key="key">
              <td>{{key}}</td>
              <td class="text-right">{{ val.length >= 1 ? val: "" }}</td>
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
    name: "NetworkCard",
    data() {
      return {
        tab: null,
        tabs: 3,
      }
    },
    props: ["minion"],
  }
</script>

<style scoped>

</style>