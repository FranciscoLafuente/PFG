<template>
  <v-app>
    <Navbar></Navbar>
    <div class="base">
      <router-view />
    </div>
    <v-container>
      <v-dialog v-model="dialog" persistent max-width="195px">
        <template v-slot:activator="{ on }">
          <v-btn color="primary" dark v-on="on">Open Dialog</v-btn>
        </template>
        <v-card>
          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn color="green darken-1" text @click="dialog = false">
              <v-icon>clear</v-icon>
            </v-btn>
          </v-card-actions>
          <v-card-title class="headline">Unauthorized</v-card-title>
          <v-card-text>The access token provided is expired. You need to login again</v-card-text>
        </v-card>
      </v-dialog>
    </v-container>
    <Footer></Footer>
  </v-app>
</template>

<script>
//import axios from "axios";
import Navbar from "./components/navbar-component";
import Footer from "./components/footer-component";

export default {
  name: "App",

  components: {
    Navbar,
    Footer
  },
  data: () => ({
    dialog: false
  }),

  created: function() {
    let msg = "Token has expired";
    this.$http.interceptors.response.use(
      response => {
        return response;
      },
      error => {
        if (error.response.status === 401 && error.response.data.msg === msg) {
          this.dialog = true;
          this.$store.dispatch("logout").then(() => this.$router.push("/"));
        }
        throw error;
      }
    );
  }
};
</script>

<style scoped>
.base {
  margin: 0 auto;
  width: 100%;
  height: 100%;
  /*background: url(/img/doraemon.5ec8c002.jpg) no-repeat center top;
    opacity: 0.1;*/
}
</style>
