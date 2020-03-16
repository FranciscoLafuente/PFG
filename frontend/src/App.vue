<template>
  <v-app>
    <Navbar></Navbar>
    <div class="base">
      <router-view />
    </div>
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
