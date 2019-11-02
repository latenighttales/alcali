<template>
  <v-container>
    <v-row>
      <v-col sm="12" lg="4">
        <v-container>
          <v-card>
            <v-list-item two-line>
              <v-list-item-content>
                <v-list-item-title class="headline">{{ job.fun }}</v-list-item-title>
                <v-list-item-subtitle>Run on {{ formatDate(job.alter_time) }}</v-list-item-subtitle>
              </v-list-item-content>
            </v-list-item>
            <v-divider></v-divider>
            <v-simple-table>
              <tbody>
              <tr>
                <td>MINION ID:</td>
                <td class="text-right">
                  <v-btn text small class="pr-0 text-none" :to="'/minions/'+job.id">{{ job.id }}</v-btn>
                </td>
              </tr>
              <tr>
                <td>JOB ID:</td>
                <td class="text-right">
                  <v-btn text small class="pr-0" :to="'/jobs/'+job.jid">{{ job.jid }}</v-btn>
                </td>
              </tr>
              <tr>
                <td>FUNCTION:</td>
                <td class="text-right">{{ job.fun }}</td>
              </tr>
              <tr v-if="job.arguments">
                <td>ARGUMENTS:</td>
                <td class="text-right">{{ job.arguments }}</td>
              </tr>
              <tr v-if="job.keyword_arguments">
                <td>KEYWORD ARGUMENTS:</td>
                <td class="text-right">{{ job.keyword_arguments }}</td>
              </tr>
              <tr>
                <td>STATUS:</td>
                <td class="text-right">
                  <v-chip :color="boolRepr(job.success)" dark>{{ boolText(job.success) }}</v-chip>

                </td>
              </tr>
              <tr>
                <td>START TIME:</td>
                <td class="text-right">{{ new Date(job.alter_time).toLocaleString("en-GB") }}</td>
              </tr>
              </tbody>
            </v-simple-table>
          </v-card>
        </v-container>
      </v-col>
      <v-col sm="12" lg="8">
        <v-container>
          <v-card>
            <v-card-title>Results</v-card-title>
            <v-divider></v-divider>
            <div v-html="ansiResult" class="ansiStyle"></div>
          </v-card>
        </v-container>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
  export default {
    name: "JobDetail",
    props: ["jid", "minion_id"],
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
        if (bool === true) return "green"
        else return "red"
      },
      boolText(bool) {
        if (bool === true) return "success"
        else return "failed"
      },
      formatDate(date) {
        return new Date(date).toLocaleString("en-GB")
      },
    },
  }
</script>

<style scoped>
  .ansiStyle {
    background-color: black;
    padding: 10px;
  }
  .theme--light.v-btn--active:hover::before, .theme--light.v-btn--active::before {
    opacity: 0;
  }

</style>