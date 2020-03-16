<template>
  <v-container>
    <Search class="bar-search"></Search>
    <div>
      <div>
        <v-btn class="folder-button" color="primary" dark fab>
          <router-link to="/myproject">
            <v-icon>folder_open</v-icon>
          </router-link>
        </v-btn>
      </div>
    </div>
  </v-container>
</template>

<script>
import Search from "../components/search-component";

export default {
  components: {
    Search
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
  color: white;
}

.v-btn--icon.v-size--default .v-icon,
.v-btn--fab.v-size--default .v-icon {
  font-size: 40px;
}
</style>