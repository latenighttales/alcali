<template>
  <v-container>
    <v-row>
      <v-col sm="12" lg="4">
        <v-card>
          <v-list-item two-line>
            <v-list-item-content>
              <v-list-item-title class="headline">{{ job.fun }}</v-list-item-title>
              <v-list-item-subtitle>Run {{ formatDate(job.alter_time) }}</v-list-item-subtitle>
            </v-list-item-content>
          </v-list-item>
          <v-divider></v-divider>
          <v-simple-table>
            <tbody>
            <tr>
              <td>FUNCTION:</td>
              <td class="text-right">{{ job.fun }}</td>
            </tr>
            <tr>
              <td>JID:</td>
              <td class="text-right">{{ job.jid }}</td>
            </tr>
            <tr v-if="job.arguments.length > 0">
              <td>ARGUMENTS:</td>
              <td class="text-right"><span v-for="arg in job.arguments">{{ arg }}</span></td>
            </tr>
            <tr>
              <td>MINION ID:</td>
              <td class="text-right">{{ job.id }}</td>
            </tr>
            <tr>
              <td>STATUS:</td>
              <td class="text-right">
                <v-chip :color="boolRepr(job.success)" dark>{{ boolText(job.success) }}</v-chip>

              </td>
            </tr>
            <tr>
              <td>START TIME:</td>
              <td class="text-right">{{ new Date(job.alter_time).toLocaleString('en-GB') }}</td>
            </tr>
            </tbody>
          </v-simple-table>
        </v-card>
      </v-col>
      <v-col sm="12" lg="8">
        <v-card>
          <v-card-title>Results</v-card-title>
          <v-divider></v-divider>
          <div v-html="ansiResult" class="ansiStyle"></div>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
  export default {
    name: "JobDetail",
    props: ['jid', 'minion_id'],
    data() {
      return {
        job: {},
        ansiResult: null,
      }
    },
    mounted() {
      this.loadData()
      this.loadRenderedJob()
    },
    methods: {
      loadData() {
        this.$http.get(`api/jobs/${this.jid}/${this.minion_id}/`).then(response => this.job = response.data)
      },
      loadRenderedJob() {
        this.$http.get(`api/jobs/${this.jid}/${this.minion_id}/rendered_state/`).then(response => this.ansiResult = response.data)
      },
      boolRepr(bool) {
        if (bool === true) return 'green'
        else return 'red'
      },
      boolText(bool) {
        if (bool === true) return 'success'
        else return 'failed'
      },
      formatDate(date) {
        return new Date(date).toLocaleString('en-GB')
      }
    }
  }
</script>

<style scoped>
  .ansiStyle {
    background-color: black;
    padding: 10px;
  }

</style>