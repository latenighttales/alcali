<template>
  <v-container fluid>
    <v-card>
      <v-card-title>{{$t('components.CommonSettings.Title')}}</v-card-title>
      <v-card-text>
        <v-container fluid>
          <v-row>
            <v-col sm="4" lg="2" align-self="center">
              {{$t('components.CommonSettings.Parse')}}
            </v-col>
            <v-col sm="4" lg="2">
              <v-select
                  :items="minions"
                  item-text="minion_id"
                  item-value="minion_id"
                  v-model="target"
                  :label="$t('components.CommonSettings.Target')"
              ></v-select>
            </v-col>
            <v-col align-self="center">
              <v-btn :disabled="target == null" @click="parseModules" color="primary">{{$t('components.CommonSettings.Submit')}}</v-btn>
            </v-col>
            <v-col sm="4" lg="1" align-self="center">
              Alcali Version:
            </v-col>
            <v-col sm="4" lg="2" align-self="center">
              <span>{{version}}</span>
            </v-col>
          </v-row>
          <v-row>
            <v-col sm="12" lg="6">
              <v-row>{{$t('components.CommonSettings.Fields')}}</v-row>
              <v-row v-for="item in uniqueMinionField" :key="item.name">
                <v-col lg="4"><b>{{item.name}}</b></v-col>
                <v-col lg="4">{{item["function"]}}</v-col>
                <v-col align-self="center">
                  <v-btn color="red" dark @click="deleteMinionsFields(item.name)">{{$t('components.CommonSettings.Delete')}}</v-btn>
                </v-col>
              </v-row>
              <v-row>
                <v-col lg="4">
                  <v-text-field
                      :label="$t('components.CommonSettings.Name')"
                      single-line
                      v-model="minionsfields_name"
                  ></v-text-field>

                </v-col>
                <v-col lg="4">
                  <v-combobox
                      :items="functions"
                      item-value="name"
                      item-text="name"
                      :label="$t('components.CommonSettings.Functions')"
                      v-model="minionsfields_value"
                  ></v-combobox>
                </v-col>
                <v-col align-self="center">
                  <v-btn :disabled="minionsfields_name == null || minionsfields_value == null" color="primary"
                         @click="createMinionsFields">{{$t('components.CommonSettings.Create')}}
                  </v-btn>
                </v-col>
              </v-row>

            </v-col>
            <v-col sm="12" lg="6">
              <v-row>{{$t('components.CommonSettings.Conformity')}}</v-row>
              <v-row v-for="item in conformity" v-bind:key="item.id">
                <v-col lg="4"><b>{{item.name}}</b></v-col>
                <v-col lg="4">{{item.function}}</v-col>
                <v-col align-self="center">
                  <v-btn color="red" @click="deleteConformity(item.id)" dark>{{$t('components.CommonSettings.Delete')}}</v-btn>
                </v-col>
              </v-row>
              <v-row>
                <v-col lg="4">
                  <v-text-field
                      :label="$t('components.CommonSettings.Name')"
                      single-line
                      v-model="conformity_name"
                  ></v-text-field>
                </v-col>
                <v-col lg="4">
                  <v-text-field
                      :label="$t('components.CommonSettings.Function')"
                      single-line
                      v-model="conformity_value"
                  ></v-text-field>
                </v-col>
                <v-col align-self="center">
                  <v-btn :disabled="conformity_name == null || conformity_value === null" color="primary"
                         @click="createConformity">{{$t('components.CommonSettings.Create')}}
                  </v-btn>
                </v-col>
              </v-row>
            </v-col>
          </v-row>
        </v-container>
      </v-card-text>
    </v-card>
  </v-container>
</template>

<script>
  export default {
    name: "CommonSettings",
    data() {
      return {
        version: "unknown",
        minions: [],
        target: null,
        functions: [],
        minionsfields: [],
        minionsfields_name: null,
        minionsfields_value: null,
        conformity: [],
        conformity_name: null,
        conformity_value: null,
      }
    },
    mounted() {
      this.loadData()
    },
    computed: {
      uniqueMinionField() {
        if (this.minionsfields === null) return
        return this.minionsfields.filter((field, index, self) =>
          index === self.findIndex((t) => (
            t["function"] === field["function"] && t.name === field.name
          )),
        )
      },
    },
    methods: {
      loadData() {
        this.$http.get("api/keys/").then(response => {
          this.minions = response.data.filter(key => key.status === "accepted")
        })
        this.$http.get("api/functions/").then(response => {
          this.functions = response.data.filter(item => item.type === "local")
        })
        this.$http.get("api/conformity/").then(response => {
          this.conformity = response.data
        })
        this.$http.get("api/minionsfields/").then(response => {
          this.minionsfields = response.data
        })
        this.$http.get("api/version/").then(response => {
          this.version = response.data.version
        })
      },
      parseModules() {
        this.$toast(this.$i18n.t("components.CommonSettings.ParseModulesStart"))
        let formData = new FormData()
        formData.set("target", this.target)
        this.$http.post("api/settings/initdb", formData).then(response => {
          this.$toast(response.data.result)
        }).then(() => {
          this.loadData()
        }).catch((error) => {
          this.$toast.error(error.response.data)
        })
      },
      deleteConformity(id) {
        let formData = new FormData
        formData.set("id", id)
        this.$http.delete("/api/conformity/" + id).then(() => {
          this.$toast(this.$i18n.t("components.CommonSettings.ConformityDeleted"))
          this.conformity.splice(this.conformity.indexOf(id), 1)
        })
      },
      createConformity() {
        let formData = new FormData
        formData.set("name", this.conformity_name)
        formData.set("function", this.conformity_value)
        this.$http.post("/api/conformity/", formData).then(() => {
          this.conformity.push({
            "name": this.conformity_name,
            "function": this.conformity_value,
            "id": this.conformity.length + 2,
          })
          this.$toast(this.$i18n.t("components.CommonSettings.ConformityCreated"))
          this.conformity_name = null
          this.conformity_value = null
        })
      },
      createMinionsFields() {
        let formData = new FormData
        formData.set("name", this.minionsfields_name)
        formData.set("function", this.minionsfields_value.name)
        formData.set("value", "{}")
        this.$http.post("/api/minionsfields/", formData).then(() => {
          this.minionsfields.push({ "name": this.minionsfields_name, "function": this.minionsfields_value.name })
          this.$toast(this.$i18n.t("components.CommonSettings.MinionsFieldsCreated"))
          this.minionsfields_name = null
          this.minionsfields_value = null
        })
      },
      deleteMinionsFields(name) {
        let formData = new FormData
        formData.set("name", name)
        this.$http.post("/api/minionsfields/delete_field/", formData).then(response => {
          this.$toast(response.data.result)
          this.minionsfields = this.minionsfields.filter(field => field.name !== name)
        })

      },
    },
  }
</script>

<style scoped>

</style>