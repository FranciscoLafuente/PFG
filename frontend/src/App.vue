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
  },

  created: function() {
    this.$http.interceptors.response.use(
      response => {
        return response;
      },
      function(error) {
        console.log("Esto es el error config", error);
        if (error.response.status === 401) {
          console.log("Esta dentro del error");
          let a = this.$router.push("/login");
          console.log("Esto es lo que devuelve el push", a);

          return Promise.reject(error);
        }
        console.log("Sale por aqui");

        // return Error object with Promise
        return Promise.reject(error);
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
