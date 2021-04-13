<template>
  <v-app>
    <v-navigation-drawer
        v-model="settings.Layout.drawer"
        :mini-variant="settings.Layout.mini"
        app
        clipped
    >
      <v-list
          dense
          nav
          dark
          color="#212121"
          class="py-0"
      >
        <v-list-item two-line :class="settings.Layout.mini && 'px-0'">
          <v-list-item-avatar>
            <v-icon large>person</v-icon>
          </v-list-item-avatar>
          <v-list-item-content>
            <v-list-item-title>{{ username }}</v-list-item-title>
            <v-list-item-subtitle>{{ email }}</v-list-item-subtitle>
          </v-list-item-content>
        </v-list-item>
      </v-list>
      <v-divider></v-divider>
      <v-list dense>
        <v-list-item v-for="route in routes" :key="route.name" :to="`${route.path}`">
          <v-list-item-action v-if="settings.Layout.mini">
            <v-tooltip right>
              <template v-slot:activator="{ on }">
                <v-icon v-on="on">{{ route.icon }}</v-icon>
              </template>
              <span>{{ route.name }}</span>
            </v-tooltip>
          </v-list-item-action>
          <v-list-item-action v-else>
            <v-icon>{{ route.icon }}</v-icon>
          </v-list-item-action>
          <v-list-item-content>
            <v-list-item-title>{{ route.name }}</v-list-item-title>
          </v-list-item-content>
        </v-list-item>
      </v-list>
      <v-divider></v-divider>
      <v-list dense>
        <v-list-item to="/users">
          <v-list-item-action v-if="settings.Layout.mini">
            <v-tooltip right>
              <template v-slot:activator="{ on }">
                <v-icon v-on="on">group</v-icon>
              </template>
              <span>Users</span>
            </v-tooltip>
          </v-list-item-action>
          <v-list-item-action v-else>
            <v-icon>group</v-icon>
          </v-list-item-action>
          <v-list-item-content>
            <v-list-item-title>Users</v-list-item-title>
          </v-list-item-content>
        </v-list-item>
        <v-list-item to="/settings">
          <v-list-item-action v-if="settings.Layout.mini">
            <v-tooltip right>
              <template v-slot:activator="{ on }">
                <v-icon v-on="on">settings</v-icon>
              </template>
              <span>Settings</span>
            </v-tooltip>
          </v-list-item-action>
          <v-list-item-action v-else>
            <v-icon>settings</v-icon>
          </v-list-item-action>
          <v-list-item-content>
            <v-list-item-title>Settings</v-list-item-title>
          </v-list-item-content>
        </v-list-item>
      </v-list>
      <template v-slot:append>
        <v-list-item @click.stop="updateDomAndSettings('mini')" class="elevation-24">
          <v-list-item-action>
            <v-icon v-if="settings.Layout.mini">arrow_forward</v-icon>
            <v-icon v-else>arrow_back</v-icon>
          </v-list-item-action>
          <v-list-item-content>
            <v-list-item-title>COLLAPSE</v-list-item-title>
          </v-list-item-content>
        </v-list-item>
      </template>
    </v-navigation-drawer>
    <v-app-bar
        color="black"
        dark
        app
        clipped-left
    >
      <v-app-bar-nav-icon @click.stop="updateDomAndSettings('drawer')"></v-app-bar-nav-icon>
      <v-toolbar-title class="font-weight-bold">ALCALI</v-toolbar-title>
      <v-spacer></v-spacer>
      <v-expand-transition>
        <v-text-field
            v-show="expand_search"
            class="mx-auto search"
            flat
            hide-details
            label="Search jids, minions, states..."
            solo-inverted
            v-model="searchInput"
            @keyup.native.enter="searchBar"
        ></v-text-field>
      </v-expand-transition>
      <v-btn icon @click="expand_search = !expand_search" class="mr-2">
        <v-icon>search</v-icon>
      </v-btn>
      <v-menu
          v-model="notif_menu"
          bottom
          left
          offset-y
          offset-x
      >
        <template v-slot:activator="{ on }">
          <v-badge
              :color="notif_nb > 0 ? 'primary': 'transparent'"
              overlap
          >
            <template v-slot:badge>
              <span v-if="notif_nb > 0">{{ notif_nb }}</span>
            </template>
            <v-icon v-on="on" @click="notif_nb = 0">notifications</v-icon>
          </v-badge>
        </template>
        <v-card min-width="500px" max-width="500px">
          <v-list max-height="700px">
            <v-list-item v-if="messages.length === 0">
              <v-list-item-content>
                <v-list-item-subtitle>No new notifications</v-list-item-subtitle>
              </v-list-item-content>
            </v-list-item>
            <v-list-item
                v-for="(item, i) in messages"
                :key="i"
                :to="item.link"
            >
              <v-list-item-avatar>
                <v-icon dark :color="item.color" size="62">{{ item.icon }}</v-icon>
              </v-list-item-avatar>

              <v-list-item-content>
                <v-list-item-title>{{ item.text }}</v-list-item-title>
                <v-list-item-subtitle>{{ item.tag }}</v-list-item-subtitle>
              </v-list-item-content>
            </v-list-item>
          </v-list>
          <v-card-actions v-show="messages.length > 0">
            <v-spacer></v-spacer>
            <v-btn text @click="messages = []">Clear</v-btn>
          </v-card-actions>
        </v-card>
      </v-menu>
      <v-menu bottom left offset-y offset-x close-on-click>
        <template v-slot:activator="{ on }">
          <v-btn v-on="on" icon>
            <v-icon>more_vert</v-icon>
          </v-btn>
        </template>
        <v-list>
          <v-list-item
              @click="updateDomAndSettings('dark')"
          >
            <v-list-item-title>Toggle Theme</v-list-item-title>
          </v-list-item>
          <v-divider></v-divider>
          <v-list-item
              @click="logout"
          >
            <v-list-item-title>Logout</v-list-item-title>
          </v-list-item>
        </v-list>
      </v-menu>
    </v-app-bar>
    <v-main>
      <v-fade-transition mode="out-in">
        <router-view :key="$route.fullPath"></router-view>
      </v-fade-transition>
    </v-main>
  </v-app>
</template>

<script>
import { mapState } from "vuex"
import { EventSourcePolyfill } from "event-source-polyfill"
import helpersMixin from "../mixins/helpersMixin"

export default {
  name: "Layout",
  props: {
    source: String,
  },
  data: () => ({
    expand_search: false,
    notif_menu: false,
    searchInput: "",
    messages: [],
    notif_nb: 0,
    routes: [
      {
        name: "Overview",
        path: "/",
        icon: "dashboard",
      },
      {
        name: "Minions",
        path: "/minions",
        icon: "device_hub",
      },
      {
        name: "Jobs",
        path: "/jobs",
        icon: "playlist_play",
      },
      {
        name: "Run",
        path: "/run",
        icon: "play_arrow",
      },
      {
        name: "Job Templates",
        path: "/job_templates",
        icon: "playlist_add_check",
      },
      {
        name: "Schedules",
        path: "/schedules",
        icon: "schedule",
      },
      {
        name: "Conformity",
        path: "/conformity",
        icon: "done_all",
      },
      {
        name: "Keys",
        path: "/keys",
        icon: "compare_arrows",
      },
      {
        name: "Events",
        path: "/events",
        icon: "playlist_add",
      },
    ],
  }),
  methods: {
    updateDomAndSettings(val) {
      this.settings.Layout[val] = !this.settings.Layout[val]
      if (val === 'dark') {
        this.$vuetify.theme.dark = this.settings.Layout[val]
      }
      this.$store.commit("updateSettings")
    },
    logout: function() {
      this.$store.dispatch("logout").then(() => {
        this.$router.push("/login")
      })
    },
    searchBar() {
      if (this.searchInput !== "") {
        this.$router.push({ name: "search", query: { q: this.searchInput } })
      }
    },
    getPrefs() {
      this.$store.dispatch("fetchSettings")
    },
    saltStatus() {
      // Various Salt event tag matchers.
      let isJobEvent = helpersMixin.methods.fnmatch("salt/job/*")
      let isJobNew = helpersMixin.methods.fnmatch("salt/job/*/new")
      let isJobReturn = helpersMixin.methods.fnmatch("salt/job/*/ret/*")
      const accessToken = localStorage.getItem("access")
      let es = new EventSourcePolyfill("/api/event_stream/", {
        headers: {
          "Authorization": `Bearer ${accessToken}`,
        },
      })
      es.addEventListener("open", () => {
        this.$store.dispatch("updateWs")
      })
      es.addEventListener("message", event => {
        let data = JSON.parse(event.data)
        // Display only activated notifs.
        if (isJobNew(data.tag) && this.settings.UserSettings.notifs.published === true) {
          if (data.data.fun !== "saltutil.find_job") {
            data.type = "new"
            data.color = "green"
            data.icon = "keyboard_tab"
            data.link = ""
            let target = ""
            if (data.data.hasOwnProperty("tgt")) {
              target = data.data.tgt
            } else {
              target = data.data.minions.length + " minion(s)"
            }
            data.text = "Job " + data.data.fun + " published for " + target
            this.messages.unshift(data)
            if (this.messages.length > this.settings.UserSettings.max_notifs) {
              this.messages.pop()
            }
            this.notif_nb += 1
          } else {
            let findJobJid = data.data.jid
            this.messages.forEach((message, index) => {
              if (message.tag === findJobJid) {
                this.messages.splice(index, 1)
                this.notif_nb -= 1
              }
            })
          }
        } else if (isJobReturn(data.tag) && this.settings.UserSettings.notifs.returned === true) {
          if (data.data.fun !== "saltutil.find_job") {
            data.type = "return"
            data.color = "primary"
            data.icon = "subdirectory_arrow_left"
            data.text = "Job " + data.data.fun + " returned for " + data.data.id
            data.link = "/jobs/" + data.data.jid + "/" + data.data.id
            this.messages.unshift(data)
            if (this.messages.length > this.max_notifs) {
              this.messages.pop()
            }
            this.notif_nb += 1
          }
        } else if (isJobEvent(data.tag) && this.settings.UserSettings.notifs.event === true) {
          data.type = "event"
          data.color = "orange"
          data.icon = "more_horiz"
          data.text = "Job Event"
          data.link = ""
          this.messages.unshift(data)
          if (this.messages.length > this.max_notifs) {
            this.messages.pop()
          }
          this.notif_nb += 1
        } else if (/^\w{20}$/.test(data.tag) && this.settings.UserSettings.notifs.created === true) {
          data.type = "created"
          data.color = "secondary"
          data.icon = "add"
          data.text = "New Job Created"
          data.link = ""
          this.messages.unshift(data)
          if (this.messages.length > this.settings.UserSettings.max_notifs) {
            this.messages.pop()
          }
          this.notif_nb += 1
        }
      }, false)
    },
  },
  created() {
    this.getPrefs()
    this.saltStatus()
    this.$vuetify.theme.dark = this.settings.Layout.dark
  },
  computed: {
    ...mapState({
      username: state => state.username,
      email: state => state.email,
      settings: state => state.settings,
    }),
  },
}
</script>

<style>
::-webkit-scrollbar-track {
  -webkit-box-shadow: inset 0 0 6px rgba(0, 0, 0, 0.3);
  border-radius: 10px;
  background-color: #F5F5F5;
}

::-webkit-scrollbar {
  width: 10px;
  background-color: #F5F5F5;
}

::-webkit-scrollbar-thumb {
  border-radius: 10px;
  -webkit-box-shadow: inset 0 0 6px rgba(0, 0, 0, .3);
  background-color: #555;
}

span .v-chip__content {
  white-space: nowrap;
}

.v-list {
  border-radius: 0px !important;
}

.search {
  max-width: 300px !important;
}


</style>