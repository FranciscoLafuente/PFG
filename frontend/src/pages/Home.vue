<template>
  <v-container>
    <Search class="bar-search"></Search>
    <div v-if="isAuthenticated">
      <v-btn class="folder-button" color="primary" dark fab>
        <router-link to="/myproject">
          <v-icon>folder_open</v-icon>
        </router-link>
      </v-btn>
    </div>
  </v-container>
</template>

<script>
import Search from "../components/SearchBar";
import { mapGetters } from "vuex";

export default {
  components: {
    Search
  },
  computed: {
    ...mapGetters(["isAuthenticated"])
  }
};
</script>

<style scoped>
.container {
  height: 100%;
  width: 60%;
  justify-content: center;
  display: flex;
  align-items: center;
}
.folder-button {
  bottom: 15%;
  right: 10%;
  position: absolute;
}

.v-application a {
  text-decoration: none;
  color: white;
}

.v-btn--icon.v-size--default .v-icon,
.v-btn--fab.v-size--default .v-icon {
  font-size: 40px;
}
</style>
