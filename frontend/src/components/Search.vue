<template>
  <div class="container">
    <v-toolbar dense :elevation="9">
      <v-text-field
        hide-details
        v-model="lookFor"
        prepend-icon="search"
        single-line
        placeholder="Search"
        @keypress.enter="search"
      ></v-text-field>
    </v-toolbar>
  </div>
</template>

<script>
export default {
  data: () => ({
    lookFor: ""
  }),

  methods: {
    search() {
      console.log(this.lookFor);
    }
  }
};
</script>