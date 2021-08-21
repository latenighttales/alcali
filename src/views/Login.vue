<template>
  <v-app id="inspire">
    <v-main>
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
              lg="4"
          >
            <v-img
                class="elevation-0"
                :src="require('../assets/img/logo.png')"
                width="100"
                aspect-ratio="1"
                style="float: right"
            ></v-img>
            <h2 class="text-center font-weight-black display-4 mb-8">ALCALI</h2>
            <v-card class="elevation-12">
              <v-toolbar
                  color="black"
                  dark
                  flat
              >
                <v-toolbar-title>{{ $t('views.Login.LoginTitle') }}</v-toolbar-title>
                <v-spacer></v-spacer>
              </v-toolbar>
              <v-form @keyup.native.enter="authenticate">
                <v-card-text>
                  <v-text-field
                      :label="$t('views.Login.Login')"
                      name="login"
                      v-model="username"
                      prepend-icon="person"
                      type="text"
                  ></v-text-field>

                  <v-text-field
                      :label="$t('views.Login.Password')"
                      v-model="password"
                      name="password"
                      prepend-icon="lock"
                      type="password"
                  ></v-text-field>
                </v-card-text>
                <v-card-actions>
                  <v-spacer></v-spacer>
                  <v-btn color="primary" dark @click.prevent="authenticate">{{ $t('views.Login.SignIn') }}</v-btn>
                </v-card-actions>
              </v-form>
            </v-card>
          </v-col>
          <v-col sm="12" align="center">
            <v-btn @click="handleClickGetAuth" :disabled="!isInit">{{ $t('views.Login.SignIn') }}
              <span class="ml-2"><GoogleLogo></GoogleLogo></span>
            </v-btn>

          </v-col>
        </v-row>
      </v-container>
    </v-main>
  </v-app>
</template>
<script>
  import GoogleLogo from "../components/GoogleLogo"
  import Vue from "vue"
  import GAuth from "vue-google-oauth2"

  export default {
    name: "Login",
    components: { GoogleLogo },
    data: () => ({
      username: null,
      password: null,
      isInit: false,
      isSignIn: false,
      provider: null,
      clientId: null,
      redirectUri: null,
    }),
    methods: {
      authenticate() {
        let username = this.username
        let password = this.password

        this.$store.dispatch("login", { username, password })
          .then(() => this.$router.push("/"))
          .catch(() => {
            this.$toast.error(this.$t("views.Login.InvalidCredentials"))
          })
      },
      handleClickGetAuth() {
        this.$gAuth.getAuthCode()
          .then(authCode => {
            // On success
            let formData = new FormData()
            formData.set("provider", this.provider)
            formData.set("code", authCode)
            formData.set("redirect_uri", this.redirectUri)
            this.$store.dispatch("oauthlogin", formData)
              .then(() => this.$router.push("/"))
              .catch(() => {
                this.$toast.error(this.$t("views.Login.Unauthorized"))
              })
          })
          .catch(() => {
            this.$toast.error(this.$t("views.Login.Unauthorized"))
          })
      },
    },
    mounted() {
      this.$http.get("api/social/").then(response => {
        this.provider = response.data.provider
        this.clientId = response.data.client_id
        this.redirectUri = response.data.redirect_uri
        const gauthOption = {
          clientId: this.clientId,
          scope: "profile email",
          prompt: "select_account",
        }
        Vue.use(GAuth, gauthOption)
        let checkGauthLoad = setInterval(() => {
          this.isInit = this.$gAuth.isInit
          this.isSignIn = this.$gAuth.isAuthorized
          if (this.isInit) clearInterval(checkGauthLoad)
        }, 1000)
      })
    },
  }
</script>
<style scoped>
  html {
    overflow-y: auto !important
  }

</style>
