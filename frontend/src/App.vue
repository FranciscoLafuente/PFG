<template>
  <v-app>
    <Navbar :isLogged="isLogged"></Navbar>
    <div class="base">
      <router-view />
      </div>  
    <Footer></Footer>
  </v-app>
</template>

<script>
import axios from 'axios'
import Navbar from "./components/navbar-component";
import Footer from "./components/footer-component";



export default {
  name: 'App',

  components: {
    Navbar,
    Footer,
  },

  data: () => ({
    isLogged: false
  }),

  updated() {
    let token = this.getToken()

    axios
      .get("http://localhost:5000/myprofile", token)
      .then(r => { 
        console.log(r);
        this.isLogged = true
      })
      .catch(e => {
        console.log(e.response)
        });
  },

  methods: {
    getToken() {
      let user = localStorage.getItem("token");
      let token = {
        headers: {
          Authorization: "Bearer " + user
        }
      };
      return token;
    }
  },
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