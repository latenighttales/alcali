<template>
  <v-container fluid>
    <UserCard></UserCard>
  </v-container>
</template>

<script>
  import UserCard from "../components/UserCard"

  export default {
    name: "Users",
    components: { UserCard },
  }
</script>

<style scoped>

</style>