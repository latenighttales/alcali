<template>
  <v-container fluid>
    <v-row no-gutters>
      <v-col sm="12">
        <v-card>
          <v-card-title>
            {{ $t("components.JobTemplatesTable.JobTemplate") }}
            <v-spacer></v-spacer>
            <v-text-field
              class="search"
              v-model="search"
              append-icon="search"
              :label="$t('common.Search')"
              single-line
              hide-details
            ></v-text-field>
          </v-card-title>
          <v-data-table
            :sort-by.sync="settings.JobTemplatesTable.table.sortBy"
            @update:sort-by="updateSettings"
            :sort-desc.sync="settings.JobTemplatesTable.table.sortDesc"
            @update:sort-desc="updateSettings"
            :items-per-page.sync="settings.JobTemplatesTable.table.itemsPerPage"
            @update:items-per-page="updateSettings"
            :headers="headers"
            :items="job_templates"
            :search="search"
            class="elevation-1"
            :loading="loading"
          >
            <template v-slot:item.name="{ item }">
              <b>{{ item.name }}</b>
            </template>
            <template v-slot:item.action="{ item }">
              <div class="text-center">
                <v-btn
                  small
                  class="ma-2"
                  color="blue-grey"
                  tile
                  dark
                  :to="computeUrl(item, false)"
                >
                  {{ $t("components.JobTemplatesTable.Run") }}
                </v-btn>
                <v-btn
                  small
                  class="ma-2"
                  color="orange"
                  tile
                  dark
                  :to="computeUrl(item, true)"
                >
                  {{ $t("components.JobTemplatesTable.Edit") }}
                </v-btn>
                <v-btn
                  small
                  class="ma-2"
                  color="red"
                  tile
                  dark
                  @click="deleteTemplate(item.id)"
                >
                  {{ $t("components.JobTemplatesTable.Delete") }}
                </v-btn>
              </div>
            </template>
          </v-data-table>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import { mapState } from "vuex"

export default {
  name: "JobTemplatesTable",
  data() {
    return {
      search: "",
      headers: [
        { text: this.$t("components.JobTemplatesTable.Name"), value: "name" },
        {
          text: this.$t("components.JobTemplatesTable.Client"),
          value: "client",
        },
        {
          text: this.$t("components.JobTemplatesTable.TargetType"),
          value: "tgt_type",
        },
        { text: this.$t("components.JobTemplatesTable.Target"), value: "tgt" },
        {
          text: this.$t("components.JobTemplatesTable.Function"),
          value: "fun",
        },
        {
          text: this.$t("components.JobTemplatesTable.Arguments"),
          value: "arg",
        },
        {
          text: this.$t("components.JobTemplatesTable.KeywordArguments"),
          value: "kwarg",
        },
        { text: this.$t("components.JobTemplatesTable.Batch"), value: "batch" },
        {
          text: this.$t("components.JobTemplatesTable.Actions"),
          value: "action",
          sortable: false,
        },
      ],
      loading: true,
      job_templates: [],
    };
  },
  mounted() {
    this.loadData();
  },
  methods: {
    updateSettings() {
      this.$store.commit("updateSettings")
    },
    loadData() {
      this.$http.get("api/job_templates/").then((response) => {
        let templates = response.data;
        // Load the job as json and augment the template with its attrs.
        templates.forEach((template) => {
          let loadedJob = JSON.parse(template.job);
          // distinction between args and kwargs.
          Object.keys(loadedJob).forEach((key) => {
            if (key === "arg") {
              let args = loadedJob[key];
              let kwarg = args.filter((item) => {
                return item.includes("=");
              });
              args = args.filter((item) => {
                return !item.includes("=");
              });
              template[key] = args.join(" ");
              template["kwarg"] = kwarg.join(" ");
            } else {
              template[key] = loadedJob[key];
            }
          });
          delete template.job;
        });
        this.job_templates = templates;
        this.loading = false;
      });
    },
    deleteTemplate(id) {
      this.$http
        .delete(`api/job_templates/${id}/`)
        .then((response) => {
          this.$toast(
            this.$i18n.t("components.JobTemplatesTable.TemplateDeleted")
          );
        })
        .then(() => {
          this.loadData();
        });
    },
    computeUrl(item, edit = false) {
      let searchParams = new URLSearchParams(item);
      searchParams.delete("id");
      if (!edit) {
        searchParams.delete("name");
      }
      return "/run?" + searchParams.toString();
    },
  },
  computed: {
    ...mapState({
      settings: state => state.settings,
    }),
  },
};
</script>

<style scoped>
</style>