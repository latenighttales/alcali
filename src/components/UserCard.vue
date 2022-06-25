<template>
  <v-container fluid>
    <v-row>
      <v-col sm="12">
        <v-card>
          <v-data-table
              :sort-by.sync="settings.UserCard.table.sortBy"
              @update:sort-by="updateSettings"
              :sort-desc.sync="settings.UserCard.table.sortDesc"
              @update:sort-desc="updateSettings"
              :items-per-page.sync="settings.UserCard.table.itemsPerPage"
              @update:items-per-page="updateSettings"
              :headers="headers"
              :items="users"
              class="elevation-1"
          >
            <template v-slot:top>
              <v-toolbar flat>
                <v-toolbar-title class="headline">{{$t('components.mixins.UserCard.Users')}}</v-toolbar-title>
                <div class="flex-grow-1"></div>
                <v-dialog v-model="dialog" max-width="500px">
                  <template v-slot:activator="{ on }">
                    <v-btn color="primary" dark class="mb-2" v-on="on" @click="user = {}" :disabled="!isStaff">{{$t('components.mixins.UserCard.Create')}}</v-btn>
                  </template>
                  <v-card>
                    <v-card-title>{{ editing === true ? `${$t('components.mixins.UserCard.UpdateUser')}` : `${$t('components.mixins.UserCard.CreateUser')}` }}</v-card-title>
                    <v-card-text>
                      <v-container fluid>
                        <v-row>
                          <v-col lg="6">
                            <v-text-field v-model="user.username" :label="$t('components.mixins.UserCard.Username')" :rules="userRules"
                                          required></v-text-field>
                          </v-col>
                          <v-col lg="6">
                            <v-text-field v-model="user.email" :label="$t('components.mixins.UserCard.Email')" :rules="emailRules"
                                          required></v-text-field>
                          </v-col>
                        </v-row>
                        <v-row>
                          <v-col lg="6">
                            <v-text-field v-model="user.first_name" :label="$t('components.mixins.UserCard.FirstName')"></v-text-field>
                          </v-col>
                          <v-col lg="6">
                            <v-text-field v-model="user.last_name" :label="$t('components.mixins.UserCard.LastName')"></v-text-field>
                          </v-col>
                        </v-row>
                        <v-row>
                          <v-col lg="6">
                            <v-text-field
                                v-model="user.password"
                                :append-icon="show ? 'visibility' : 'visibility_off'"
                                :type="show ? 'text' : 'password'"
                                name="input-10-1"
                                :label="$t('components.mixins.UserCard.Password')"
                                counter
                                @click:append="show = !show"
                            ></v-text-field>
                          </v-col>
                          <v-col lg="6">
                            <v-checkbox
                                v-model="user.is_staff"
                                :label="$t('components.mixins.UserCard.StaffUser')"
                                :disabled="!isStaff"
                            ></v-checkbox>
                          </v-col>
                        </v-row>
                      </v-container>

                    </v-card-text>
                    <v-card-actions>
                      <v-spacer></v-spacer>
                      <v-btn color="primary" v-if="editing" @click="resetUser">{{$t('components.mixins.UserCard.Discard')}}</v-btn>
                      <v-btn color="warning" v-if="editing" @click="updateUser">{{$t('components.mixins.UserCard.Update')}}</v-btn>
                      <v-btn color="warning" v-if="!editing" :disabled="user.username == null || user.email == ''"
                             @click="createUser">{{$t('components.mixins.UserCard.Create')}}
                      </v-btn>
                    </v-card-actions>
                  </v-card>

                </v-dialog>
              </v-toolbar>
            </template>

            <template v-slot:item.is_staff="{ item }">
              <v-chip color="primary" v-if="item.is_staff" dark>{{ item.is_staff }}</v-chip>
            </template>
            <template v-slot:item.token="{ item }">
              <div class="text-center">
                <v-btn
                    small
                    class="ma-2"
                    color="primary"
                    tile
                    dark
                    @click="showToken(item)"
                >
                  {{$t('components.mixins.UserCard.View')}}
                </v-btn>
                <v-btn
                    small
                    class="ma-2"
                    color="orange"
                    tile
                    dark
                    @click="manageToken('renew', item)"
                >
                  {{$t('components.mixins.UserCard.Renew')}}
                </v-btn>
                <v-btn
                    small
                    color="red"
                    tile
                    dark
                    :disabled="String(item.id) === currentUserId"
                    @click="manageToken('revoke', item)"
                >
                  {{$t('components.mixins.UserCard.Revoke')}}
                </v-btn>
              </div>
            </template>
            <template v-slot:item.date_joined="{ item }">
              {{new Date(item.date_joined).toLocaleString("en-GB")}}
            </template>
            <template v-slot:item.action="{ item }">
              <div class="text-center">
                <v-btn
                    small
                    class="ma-2"
                    color="orange"
                    tile
                    dark
                    @click="editUser(item)"
                >
                  {{$t('components.mixins.UserCard.Update')}}
                </v-btn>
                <v-btn
                    small
                    color="red"
                    tile
                    dark
                    :disabled="String(item.id) === currentUserId"
                    @click="confirmDelete(item)"
                >
                  {{$t('components.mixins.UserCard.Delete')}}
                </v-btn>
              </div>
            </template>
          </v-data-table>
        </v-card>
      </v-col>
    </v-row>
    <div class="text-center">
      <v-dialog
          v-model="dialogDelete"
          width="500"
      >
        <v-card>
          <v-card-title
              class="headline red"
              primary-title
          >
            {{$t('components.mixins.UserCard.Delete')}} {{ user.username }} ?
          </v-card-title>

          <v-card-text>
            <br>
            {{$t('components.mixins.UserCard.ActionMsg')}}
          </v-card-text>

          <v-divider></v-divider>

          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn
                color="primary"
                text
                @click="dialogDelete = false"
            >
              {{$t('components.mixins.UserCard.Close')}}
            </v-btn>
            <v-btn
                color="red"
                text
                @click="deleteUser(user.id)"
            >
              {{$t('components.mixins.UserCard.Delete')}}
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>
    </div>
    <div class="text-center">
      <v-dialog
          v-model="dialogToken"
          width="500"
      >
        <v-card>
          <v-card-title
              class="headline primary"
              primary-title
          >
            {{ user.username }} {{$t('components.mixins.UserCard.Token')}}
          </v-card-title>

          <v-card-text v-if="user.user_settings">
            <br>
            {{user.user_settings.token}}
          </v-card-text>

          <v-divider></v-divider>

          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn
                color="primary"
                text
                @click="dialogToken = false"
            >
              {{$t('components.mixins.UserCard.Close')}}
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>
    </div>
  </v-container>
</template>

<script>
import { mapState } from "vuex"

  export default {
    name: "UserCard",
    data() {
      return {
        search: "",
        headers: [
          { text: this.$t("components.mixins.UserCard.Username"), value: "username" },
          { text: this.$t("components.mixins.UserCard.FirstName"), value: "first_name" },
          { text: this.$t("components.mixins.UserCard.LastName"), value: "last_name" },
          { text: this.$t("components.mixins.UserCard.Email"), value: "email" },
          { text: this.$t("components.mixins.UserCard.StaffUser"), value: "is_staff" },
          { text: this.$t("components.mixins.UserCard.Token"), value: "token", sortable: false },
          { text: this.$t("components.mixins.UserCard.DateJoined"), value: "date_joined" },
          { text: this.$t("components.mixins.UserCard.Action"), value: "action", sortable: false },
        ],
        userRules: [
          v => !!v || this.$t("components.mixins.UserCard.UsernameRequired"),
        ],
        emailRules: [
          v => !!v || this.$t("components.mixins.UserCard.EmailRequired"),
          v => /.+@.+/.test(v) || this.$t("components.mixins.UserCard.EmailValid"),
        ],
        users: [],
        user: {},
        editing: false,
        show: false,
        dialog: false,
        dialogDelete: false,
        dialogToken: false,
      }
    },
    mounted() {
      this.getUsers()
    },
    computed: {
      currentUserId() {
        return this.$store.state.id
      },
      isStaff() {
        return JSON.parse(this.$store.getters.isStaff) || false
      },
      ...mapState({
        settings: state => state.settings,
      }),
    },
    methods: {
      updateSettings() {
        this.$store.commit("updateSettings")
      },
      getUsers() {
        this.$http.get("api/users/").then(response => {
          this.users = response.data
        }).catch((error) => {
          this.$toast.error(error.response.data)
        })
      },
      createUser() {
        let formData = new FormData
        Object.keys(this.user).forEach(key => formData.append(key, this.user[key]))
        this.$http.post("api/users/", formData).then(() => {
          this.$toast(this.$i18n.t("components.mixins.UserCard.UserCreated"))
          this.dialog = false
        }).then(() => {
          this.user = {}
          this.getUsers()
        }).catch((error) => {
          this.dialog = false
          this.user = {}
          this.$toast.error(error.response.data)
        })
      },
      updateUser() {
        this.editing = false
        let formData = new FormData
        formData.set("username", this.user.username||'')
        formData.set("email", this.user.email||'')
        formData.set("first_name", this.user.first_name||'')
        formData.set("last_name", this.user.last_name||'')
        formData.set("password", this.user.password||'')
        formData.set("is_staff", this.user.is_staff)
        this.$http.patch(`api/users/${this.user.id}/`, formData).then(() => {
          this.$toast(this.$i18n.t("components.mixins.UserCard.UserUpdated"))
          this.dialog = false
          this.user = {}
        }).then(() => {
          this.getUsers()
        }).catch((error) => {
          this.dialog = false
          this.user = {}
          this.$toast.error(error.response.data)
        })
      },
      showToken(user) {
        this.dialogToken = true
        this.user = user
      },
      manageToken(action, user) {
        let formData = new FormData
        formData.set("action", action)
        this.$http.post(`api/users/${user.id}/manage_token/`, formData).then((response) => {
          this.$toast(response.data.result)
        }).then(() => {
          this.getUsers()
        }).catch((error) => {
          this.$toast.error(error.response.data)
        })
      },
      confirmDelete(user) {
        this.dialogDelete = true
        this.user = user
      },
      deleteUser(id) {
        this.$http.delete("api/users/" + id).then(() => {
          this.dialogDelete = false
          this.$toast(this.$i18n.t("components.mixins.UserCard.UserDeleted"))
        }).then(() => {
          this.getUsers()
        }).catch((error) => {
          this.$toast.error(error.response.data)
        })
      },
      editUser(user) {
        this.dialog = true
        this.editing = true
        this.user = user
      },
      resetUser() {
        this.dialog = false
        this.editing = false
        this.user = {}
      },
    },
  }
</script>

<style scoped>

</style>