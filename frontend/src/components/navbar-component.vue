<template>
    <div>
    <v-app-bar color="blue darken-1" dense dark>
      <v-toolbar-title>
        <router-link to="/">Shodita</router-link>
      </v-toolbar-title>

      <v-spacer></v-spacer>
      <v-container class="bar-buttons">
        <v-btn color="blue darken-1" text>
          <router-link to="/bots"> Bots</router-link>
        </v-btn>
        <v-btn color="blue darken-1" text>
          <router-link to="/signup">Sign up</router-link>
        </v-btn>

        <v-btn icon v-if="!isLogged">
          <router-link to="/login">
            <v-icon>perm_identity</v-icon>
          </router-link>
        </v-btn>
        <v-btn icon v-else><span>Logged</span></v-btn>
      </v-container>
    </v-app-bar>
  </div>
</template>

<script>
export default {
    props: ["isLogged"], 
}
</script>

<style scoped>
.bar-buttons {
  text-align: right;
}

a, a:visited {
  color: white;
  text-decoration: none;
}

.v-application a {
  color: white;
}
</style>