<template>
  <v-container>
    <v-row>
      <v-col sm="12">
        <v-card>
          <v-card-title>{{ editing === true ? 'Update User' : 'Create User'}}</v-card-title>
          <v-card-text>
            <v-container>
              <v-row>
                <v-col lg="6">
                  <v-text-field v-model="user.username" label="Username" :rules="userRules" required></v-text-field>
                </v-col>
                <v-col lg="6">
                  <v-text-field v-model="user.email" label="Email" :rules="emailRules" required></v-text-field>
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
      </v-col>
    </v-row>
    <v-row>
      <v-col sm="12">
        <v-card>
          <v-card-title>
            Users
            <v-spacer></v-spacer>
            <v-text-field
                v-model="search"
                append-icon="search"
                label="Search"
                single-line
                hide-details
            ></v-text-field>
          </v-card-title>
          <v-data-table
              sort-by="username"
              :headers="headers"
              :items="users"
              :search="search"
              class="elevation-1"
          >
            <template v-slot:item.is_staff="{ item }">
              <v-chip color="primary" v-if="item.is_staff" dark>{{ item.is_staff }}</v-chip>
            </template>
            <template v-slot:item.date_joined="{ item }">
              {{new Date(item.date_joined).toLocaleString('en-GB')}}
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
                    @click="deleteUser(item.id)"
                >
                  delete
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
  export default {
    name: "UserCard",
    data() {
      return {
        search: '',
        headers: [
          {text: 'Username', value: 'username'},
          {text: 'First Name', value: 'first_name'},
          {text: 'Last Name', value: 'last_name'},
          {text: 'Email', value: 'email'},
          {text: 'Staff', value: 'is_staff'},
          {text: 'Date Joined', value: 'date_joined'},
          {text: 'Actions', value: 'action', sortable: false},
        ],
        userRules: [
          v => !!v || 'Username is required',
        ],
        emailRules: [
          v => !!v || 'E-mail is required',
          v => /.+@.+/.test(v) || 'E-mail must be valid',
        ],
        users: [],
        user: {},
        editing: false,
        show: false,
      }
    },
    mounted() {
      this.getUsers()
    },
    methods: {
      getUsers() {
        this.$http.get("api/users/").then(response => {
          this.users = response.data
        })
      },
      createUser() {
        let formData = new FormData
        Object.keys(this.user).forEach(key => formData.append(key, this.user[key]))
        this.$http.post("api/users/", formData).then(() => {
          this.$toast("User created")
        }).then(() => {
          this.user = {}
          this.getUsers()
        })
      },
      updateUser() {
        this.editing = false
        let formData = new FormData
        formData.set('username', this.user.username)
        formData.set('email', this.user.email)
        formData.set('first_name', this.user.first_name)
        formData.set('last_name', this.user.last_name)
        formData.set('password', this.user.password)
        formData.set('is_staff', this.user.is_staff)
        this.$http.patch("api/users/" + this.user.id + "/", formData).then(() => {
          this.$toast("User updated")
          this.user = {}
        }).then(() => {
          this.getUsers()
        })
      },
      deleteUser(id) {
        this.$http.delete("api/users/" + id).then(() => {
          this.$toast("User deleted")
        }).then(() => this.getUsers())
      },
      editUser(user) {
        this.editing = true
        this.user = user
      },
      resetUser() {
        this.editing = false
        this.user = {}
      },
    },
  }
</script>

<style scoped>

</style>