<template>
  <v-container>
    <v-card>
      <v-card-title>{{minion_id}}</v-card-title>
      <v-simple-table>
        <tbody>
        <tr>
          <td>Highstate</td>
          <td class="text-right">
            <v-chip :color="boolRepr(conformity)" dark>{{ valRepr(conformity) }}</v-chip>
          </td>
        </tr>
        </tbody>
        <tbody v-for="conf in custom_conformity" :key="conf.key">
        <tr v-for="(val, key) in conf" :key="key">
          <td>{{ key }}</td>
          <td class="text-right">
            <v-chip
                v-if="isBool(val)"
                :color="boolRepr(conformity)"
                dark
            >{{ valRepr(conformity) }}</v-chip>
            <span v-else>{{ valRepr(val) }}</span>
          </td>
        </tr>
        </tbody>
      </v-simple-table>
    </v-card>
  </v-container>
</template>

<script>
  export default {
    name: "ConformityCard",
    props: ["minion_id", "conformity", "custom_conformity"],
    data() {
      return {}
    },
    methods: {
      boolRepr(bool) {
        if (bool === true) {
          return "green"
        } else if (bool === false) {
          return "red"
        } else {
          return "primary"
        }
      },
      isBool(val) {
        return typeof val === 'boolean'
      },
      valRepr(val) {
        return val === null ? "unknown" : val
      },
    },
  }
</script>

<style scoped>

</style>