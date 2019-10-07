<template>
  <v-container>
    <UserCard></UserCard>
  </v-container>
</template>

<script>
  import UserCard from "../components/mixins/UserCard"

  export default {
    name: "Users",
    components: { UserCard },
  }
</script>

<style scoped>

</style>