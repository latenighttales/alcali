<template>
  <v-container fluid>
    <v-card>
      <v-card-title>{{ $t('components.KeysStatusCard.keys') }}</v-card-title>
      <v-simple-table>
        <tbody>
        <tr v-for="(count, status) in keys_status" :key="status">
          <td class="pr-0">
            <v-icon>{{statusIcon(status)}}</v-icon>
          </td>
          <td class="pl-0">{{ $t(`components.KeysStatusCard.${status}`) }}</td>
          <td class="text-right">{{ count }} / {{keys_total}}</td>
        </tr>
        </tbody>
      </v-simple-table>
    </v-card>
  </v-container>
</template>

<script>

  export default {
    name: "KeysStatusCard",
    data() {
      return {
        keys_status: {},
        keys_total: 0,
      }
    },
    mounted() {
      this.loadData()
    },
    methods: {
      loadData() {
        this.$http.get("api/keys/keys_status/").then(response => {
          this.keys_status = response.data
          this.keys_total = Object.values(response.data).reduce((acc, cur)=> acc + cur)
        })
      },
      statusIcon(status) {
        switch (status) {
          case "accepted":
            return "check"
          case "rejected":
            return "first_page"
          case "denied":
            return "close"
          case "unaccepted":
            return "refresh"
        }
      },
    },
  }
</script>

<style scoped>

</style>