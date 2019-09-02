<template>

</template>

<script>
  export default {
    name: "Search",
    data() {
      return {
        query: null,

      }
    },
    created() {
      this.query = this.$route.query.q
    },
    mounted() {
      this.searchBar()
    },
    methods: {
      searchBar() {
        this.$http.get("api/search/?q=" + this.query).then(response => {
          console.log(response.data)
        })
      },
    },
  }
</script>

<style scoped>

</style>