<template>
  <v-app>
    <v-navigation-drawer
        v-model="drawer"
        :mini-variant="mini"
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
        <v-list-item two-line>
          <v-list-item-avatar>
            <v-icon large>person</v-icon>
          </v-list-item-avatar>
          <v-list-item-content>
            <v-list-item-title>{{username}}</v-list-item-title>
            <v-list-item-subtitle>{{email}}</v-list-item-subtitle>
          </v-list-item-content>
        </v-list-item>
      </v-list>
      <v-divider></v-divider>
      <v-list dense>
        <v-list-item v-for="route in routes" :key="route.name" :to="`${route.path}`">
          <v-list-item-action v-if="mini">
            <v-tooltip right>
              <template v-slot:activator="{ on }">
                <v-icon v-on="on">{{ route.icon }}</v-icon>
              </template>
              <span>{{route.name}}</span>
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
          <v-list-item-action v-if="mini">
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
          <v-list-item-action v-if="mini">
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
        <v-list-item @click.stop="mini = !mini" class="elevation-24">
          <v-list-item-action>
            <v-icon v-if="mini">arrow_forward</v-icon>
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
      <v-app-bar-nav-icon @click.stop="drawer = !drawer"></v-app-bar-nav-icon>
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
                <v-icon dark :color="item.color" size="62">{{item.icon}}</v-icon>
              </v-list-item-avatar>

