<template>
  <v-app id="inspire">
    <v-content>
      <v-container
          class="fill-height"
          fluid
      >
        <v-row
            align="center"
            justify="center"
        >
          <v-col
              cols="12"
              sm="8"
              md="4"
          >
            <h1 class="text-center font-weight-bold display-4 mb-8">ALCALI</h1>
            <v-card class="elevation-12">
              <v-toolbar
                  color="black"
                  dark
                  flat
              >
                <v-toolbar-title>Login</v-toolbar-title>
                <v-spacer></v-spacer>
              </v-toolbar>
              <v-form @keyup.native.enter="authenticate">
                <v-card-text>
                  <v-text-field
                      label="Login"
                      name="login"
                      v-model="username"
                      prepend-icon="person"
                      type="text"
                  ></v-text-field>

                  <v-text-field
                      label="Password"
                      v-model="password"
                      name="password"
                      prepend-icon="lock"
                      type="password"
                  ></v-text-field>
                </v-card-text>
                <v-card-actions>
                  <v-spacer></v-spacer>
                  <v-btn color="primary" dark @click.prevent="authenticate">Login</v-btn>
                </v-card-actions>
              </v-form>
            </v-card>
          </v-col>
        </v-row>
      </v-container>
    </v-content>
  </v-app>
</template>
<script>
  export default {
    name: "Login",
    data: () => ({
      username: null,
      password: null,
    }),
    methods: {
      authenticate() {
        let username = this.username
        let password = this.password

        this.$store.dispatch("login", { username, password })
          .then(() => this.$router.push("/"))
          .catch((err) => {
            this.$toast.error("Invalid Login / Password")
          })
      },
    },
  }
</script>
<style scoped>
  html {
    overflow-y: auto !important
  }

</style>
