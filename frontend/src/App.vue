<template>
  <v-app>
    <Navbar></Navbar>
    <div class="base">
      <router-view />
    </div>
    <v-container class="container">
      <dialogMessage
        :dialogMsg="dialogMsg"
        :title="msg_title"
        :icon="msg_icon"
        :message="msg_text"
        @showMsg="dialogMsg = $event"
      ></dialogMessage>
    </v-container>
    <Footer></Footer>
  </v-app>
</template>

<script>
//import axios from "axios";
import Navbar from "./components/Navbar";
import Footer from "./components/Footer";
import dialogMessage from "./components/DialogMessage";
import { UN_TITLE, UN_ICON, UN_TEXT } from "./common/dialogMsg";

export default {
  name: "App",

  components: {
    Navbar,
    Footer,
    dialogMessage
  },
  data: () => ({
    dialogMsg: false,
    msg_title: UN_TITLE,
    msg_icon: UN_ICON,
    msg_text: UN_TEXT
  }),

  created: function() {
    let msg = "Token has expired";
    this.$http.interceptors.response.use(
      response => {
        return response;
      },
      error => {
        if (error.response.status === 401 && error.response.data.msg === msg) {
          this.dialogMsg = true;
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
  height: 87%;
}

.v-card:not(.v-sheet--tile):not(.v-card--shaped) {
  text-align: center;
}

.icon-error {
  font-size: 60px;
}
</style>
