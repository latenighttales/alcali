<template>
  <v-row v-resize="onResize">
    <v-col sm="12">
      <div class="console" id="terminal"></div>
    </v-col>
  </v-row>
</template>

<script>
  import { Terminal } from "xterm";
  import LocalEchoController from "local-echo";
  import "xterm/lib/xterm.css";
  import "xterm/dist/xterm.css";
  import * as fit from "xterm/lib/addons/fit/fit";

  export default {
    name: "TerminalCard",
    props: ["minions", "functions"],
    data() {
      return {
        term: null,
        functions_name: null
      };
    },
    methods: {
      initTerm() {
        let terminalContainer = document.getElementById("terminal");
        Terminal.applyAddon(fit);
        this.term = new Terminal({
          cursorBlink: true,
          fontSize: 20,
          fontFamily: "'Roboto Mono', monospace"

        });
        this.term.open(terminalContainer);
        // Create a local echo controller
        const localEcho = new LocalEchoController(this.term);
        // Create some auto-completion handlers
        localEcho.addAutocompleteHandler((index) => {
          if (index !== 0) return [];
          return ["salt", "clear"];
        });
        localEcho.addAutocompleteHandler((index) => {
          if (index !== 1) return [];
          return this.minions;
        });
        localEcho.addAutocompleteHandler((index) => {
          if (index !== 2) return [];
          return this.functions.map(item => item.name);
        });

        const help = "Usage: salt [options] '<target>' <function> [arguments]";
        // Infinite loop of reading lines
        const readLine = () => {
          localEcho.read(" ~$ ").then((input) => {
            // Print help
            if (input.split(" ").filter(item => {
              return item !== "";
            }).length < 1) {
              localEcho.println(help);
              readLine();
            } else if (input.split(" ").length === 1) {
              if (input === "clear") {
                this.term.clear();
              }
            } else if (input.split(" ").length >= 3) {
              let formData = new FormData;
              formData.set("raw", true);
              formData.set("command", input);
              this.$toast("Running " + input);
              this.$http.post("api/run/", formData).then(response => {
                localEcho.println(response.data.results);
              }).then(() => readLine());
            } else {
              localEcho.println(help);
              readLine();
            }
          });
        };
        readLine();
      },
      onResize() {
        if (this.term !== null) {
          this.term.fit();
        }
      }
    },
    mounted() {
      setTimeout(() => {
        this.initTerm();
      }, 100);
    },
    beforeDestroy() {
      if (this.term !== null) {
        this.term.destroy();
      }
    }
  };
</script>

<style scoped>

</style>