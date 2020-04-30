<template>
  <div>
    <v-app-bar color="blue darken-1" dense dark>
      <v-toolbar-title>
        <router-link to="/">Shodita</router-link>
      </v-toolbar-title>

      <v-spacer></v-spacer>
      <v-toolbar-items>
        <v-btn color="blue darken-1" text>
          <router-link to="/myproject">My Projects</router-link>
        </v-btn>
        <v-btn color="blue darken-1" text>
          <router-link to="/bots">My Bots</router-link>
        </v-btn>
        <v-btn icon>
          <router-link to="/uploadBot">
            <v-icon>adb</v-icon>
          </router-link>
        </v-btn>
        <v-btn color="blue darken-1" text>
          <router-link to="/signup">Sign up</router-link>
        </v-btn>

        <v-btn icon @click="logout()">
          <v-icon v-if="!isAuthenticated">perm_identity</v-icon>
          <v-icon v-else>power_off</v-icon>
        </v-btn>
      </v-toolbar-items>
    </v-app-bar>
  </div>
</template>

<script>
import { mapGetters } from "vuex";
import { LOGOUT } from "../store/actions.type";

export default {
  computed: {
    ...mapGetters(["isAuthenticated"])
  },
  methods: {
    logout: function() {
      this.$store.dispatch(LOGOUT).then(() => {
        this.$router.push({ name: "login" });
      });
    }
  }
};
</script>

<style scoped>
.v-toolbar__title {
  min-width: max-content;
}

a,
a:visited {
  color: white;
  text-decoration: none;
}

.v-application a {
  color: white;
}
</style>
