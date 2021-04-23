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
                <v-toolbar-title class="headline">Users</v-toolbar-title>
                <div class="flex-grow-1"></div>
                <v-dialog v-model="dialog" max-width="500px">
                  <template v-slot:activator="{ on }">
                    <v-btn color="primary" dark class="mb-2" v-on="on" @click="user = {}" :disabled="!isStaff">Create
                    </v-btn>
                  </template>
                  <v-card>
                    <v-card-title>{{ editing === true ? "Update User" : "Create User" }}</v-card-title>
                    <v-card-text>
                      <v-container fluid>
                        <v-row>
                          <v-col lg="6">
                            <v-text-field v-model="user.username" label="Username" :rules="userRules"
                                          required></v-text-field>
                          </v-col>
                          <v-col lg="6">
                            <v-text-field v-model="user.email" label="Email" :rules="emailRules"
                                          required></v-text-field>
                          </v-col>
                        </v-row>
                        <v-row>
                          <v-col lg="6">
                            <v-text-field v-model="user.first_name" label="First Name"></v-text-field>
                          </v-col>
                          <v-col lg="6">
                            <v-text-field v-model="user.last_name" label="Last Name"></v-text-field>
                          </v-col>
                        </v-row>
                        <v-row>
                          <v-col lg="6">
                            <v-text-field
                                v-model="user.password"
                                :append-icon="show ? 'visibility' : 'visibility_off'"
                                :type="show ? 'text' : 'password'"
                                name="input-10-1"
                                label="Password"
                                counter
                                @click:append="show = !show"
                            ></v-text-field>
                          </v-col>
                          <v-col lg="6">
                            <v-checkbox
                                v-model="user.is_staff"
                                label="Staff User"
                                :disabled="!isStaff"
                            ></v-checkbox>
                          </v-col>
                        </v-row>
                      </v-container>

                    </v-card-text>
                    <v-card-actions>
                      <v-spacer></v-spacer>
                      <v-btn color="primary" v-if="editing" @click="resetUser">Discard</v-btn>
                      <v-btn color="warning" v-if="editing" @click="updateUser">Update</v-btn>
                      <v-btn color="warning" v-if="!editing" :disabled="user.username == null || user.email == ''"
                             @click="createUser">Create
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
                  view
                </v-btn>
                <v-btn
                    small
                    class="ma-2"
                    color="orange"
                    tile
                    dark
                    @click="manageToken('renew', item)"
                >
                  renew
                </v-btn>
                <v-btn
                    small
                    color="red"
                    tile
                    dark
                    :disabled="String(item.id) === currentUserId"
                    @click="manageToken('revoke', item)"
                >
                  revoke
                </v-btn>
              </div>
            </template>
            <template v-slot:item.date_joined="{ item }">
              {{ new Date(item.date_joined).toLocaleString("en-GB") }}
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
                  update
                </v-btn>
                <v-btn
                    small
                    color="red"
                    tile
                    dark
                    :disabled="String(item.id) === currentUserId"
                    @click="confirmDelete(item)"
                >
                  delete
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
            Delete {{ user.username }} ?
          </v-card-title>

          <v-card-text>
            <br>
            this action is irreversible.
          </v-card-text>

          <v-divider></v-divider>

          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn
                color="primary"
                text
                @click="dialogDelete = false"
            >
              close
            </v-btn>
            <v-btn
                color="red"
                text
                @click="deleteUser(user.id)"
            >
              delete
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
            {{ user.username }} Token
          </v-card-title>

          <v-card-text v-if="user.user_settings">
            <br>
            {{ user.user_settings.token }}
          </v-card-text>

          <v-divider></v-divider>

          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn
                color="primary"
                text
                @click="dialogToken = false"
            >
              close
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
        { text: "Username", value: "username" },
        { text: "First Name", value: "first_name" },
        { text: "Last Name", value: "last_name" },
        { text: "Email", value: "email" },
        { text: "Staff", value: "is_staff" },
        { text: "Token", value: "token", sortable: false },
        { text: "Date Joined", value: "date_joined" },
        { text: "Actions", value: "action", sortable: false },
      ],
      userRules: [
        v => !!v || "Username is required",
      ],
      emailRules: [
        v => !!v || "E-mail is required",
        v => /.+@.+/.test(v) || "E-mail must be valid",
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
        this.$toast("User created")
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
      formData.set("username", this.user.username || "")
      formData.set("email", this.user.email || "")
      formData.set("first_name", this.user.first_name || "")
      formData.set("last_name", this.user.last_name || "")
      formData.set("password", this.user.password || "")
      formData.set("is_staff", this.user.is_staff)
      this.$http.patch(`api/users/${this.user.id}/`, formData).then(() => {
        this.$toast("User updated")
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
        this.$toast("User deleted")
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