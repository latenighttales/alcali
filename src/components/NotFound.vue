<template>
  <v-container fluid>
    <v-row>
      <v-col cols="4" offset="4">
        <v-card>
          <v-card-title class="black white--text subheading" primary-title>
            <span class="title">{{$t('components.NotFound.Title')}}</span>
          </v-card-title>
          <v-card-text class="display-1 ma-7 text-center">
            {{$t('components.NotFound.404')}}
          </v-card-text>
          <v-card-actions>
            <v-btn text class="primary darken-3 white--text" to="/">
              <v-icon left>arrow_back</v-icon>
              {{$t('components.NotFound.Back')}}
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
  export default {
    name: "NotFound"
  }
</script>

<style scoped>

</style>

