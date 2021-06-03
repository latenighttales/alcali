<template>
  <v-container fluid>
    <v-card>
      <v-card-title>{{ $t('components.AlcaliStatusCard.Status') }}</v-card-title>
      <v-simple-table>
        <tbody>
        <tr>
          <td>{{ $t('components.KeysStatusCard.saltWebsocket') }}</td>
          <td class="text-right">
            <v-chip
                :color="wsStatus ? 'green': 'red'"
                text-color="white"
            >
              {{ wsStatus ? $t("components.AlcaliStatusCard.OK") : $t("components.AlcaliStatusCard.NOT_OK") }}
            </v-chip>
          </td>
        </tr>
        <tr v-for="(count, status) in stats" :key="status">
          <td>{{ $t(`components.AlcaliStatusCard.${status}`) }}</td>
          <td class="text-right">{{ count }}</td>
        </tr>
        </tbody>
      </v-simple-table>
    </v-card>
  </v-container>
</template>

<script>
  import helpersMixin from "./mixins/helpersMixin"

  export default {
    name: "AlcaliStatusCard",
    mixins: [helpersMixin],
    data() {
      return {
        stats: {},
      }
    },
    mounted() {
      this.loadData()
    },
    computed: {
      wsStatus() {
        return this.$store.state.ws_status
      },
    },
    methods: {
      loadData() {
        this.$http.get("api/stats/").then(response => this.stats = response.data)
      },
    },
  }
</script>

<style scoped>

</style>