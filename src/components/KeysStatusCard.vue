<template>
  <v-container>
    <v-card>
      <v-card-title>Keys</v-card-title>
      <v-simple-table>
        <tbody>
        <tr v-for="(count, status) in keys_status" :key="status">
          <td>{{ status }}</td>
          <td class="text-right">{{ count }}</td>
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
      }
    },
    mounted() {
      this.loadData();
    },
    methods: {
      loadData() {
        this.$http.get("api/keys/keys_status/").then(response => this.keys_status = response.data)
      },
    }
  }
</script>

<style scoped>

</style>