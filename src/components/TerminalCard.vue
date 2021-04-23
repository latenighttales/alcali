<template>
  <v-row v-resize="onResize">
    <v-col sm="12">
      <div class="console" id="terminal"></div>
    </v-col>
  </v-row>
</template>

<script>
  import { Terminal } from "xterm"
  import { FitAddon } from "xterm-addon-fit"
  import "xterm/css/xterm.css"
  import LocalEchoController from "../assets/js/local-echo/LocalEchoController"

  export default {
    name: "TerminalCard",
    props: ["minions", "functions"],
    data() {
      return {
        term: null,
        fitter: null,
        functions_name: null,
      }
    },
    methods: {
      initTerm() {
        let terminalContainer = document.getElementById("terminal")
        this.term = new Terminal({
          cursorBlink: true,
          fontSize: 20,
          fontFamily: "'Roboto Mono', monospace",

        })
        const fitAddon = new FitAddon()
        this.term.loadAddon(fitAddon)
        this.term.open(terminalContainer)
        fitAddon.fit()
        this.fitter = fitAddon
        // Create a local echo controller
        const localEcho = new LocalEchoController(this.term)
        // Create some auto-completion handlers
        localEcho.addAutocompleteHandler((index) => {
          if (index !== 0) return []
          return ["salt", "clear"]
        })
        localEcho.addAutocompleteHandler((index) => {
          if (index !== 1) return []
          return this.minions
        })
        localEcho.addAutocompleteHandler((index) => {
          if (index !== 2) return []
          return this.functions.map(item => item.name)
        })

        const help = "Usage: salt [options] '<target>' <function> [arguments]"
        // Infinite loop of reading lines
        const readLine = () => {
          localEcho.read(" ~$ ").then((input) => {
            let filteredInput = input.split(" ").filter(item => {
              return item !== ""
            })
            if (filteredInput.length === 0) { // just "enter"
              readLine()
            } else if (filteredInput.length === 1 && filteredInput[0] === "clear") {
              this.term.clear()
              readLine()
            } else if (filteredInput.length <= 2) {
              localEcho.println(help)
              readLine()
            } else if (input.split(" ").length >= 3 && filteredInput[0] === "salt") {
              let formData = new FormData
              formData.set("raw", true)
              formData.set("cli", true)
              formData.set("command", input)
              this.$toast("Running " + input)
              this.$http.post("api/run/", formData).then(response => {
                localEcho.println(response.data.results)
              }).catch((error) => {
                this.$toast.error(error.response.data)
              }).then(() => readLine())
            } else {
              localEcho.println(help)
              readLine()
            }
          })
        }
        readLine()
      },
      onResize() {
        if (this.term !== null) {
          this.fitter.fit()
        }
      },
    },
    mounted() {
      setTimeout(() => {
        this.initTerm()
      }, 100)
    },
    beforeDestroy() {
      if (this.term !== null) {
        this.term.dispose()
      }
    },
  }
</script>

<style scoped>

</style>