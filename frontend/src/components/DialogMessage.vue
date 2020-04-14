<template>
  <v-dialog v-model="dialogMsg" persistent max-width="260px">
    <v-card>
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn color="green darken-1" text @click="$emit('showMsg', false)">
          <v-icon>clear</v-icon>
        </v-btn>
      </v-card-actions>
      <v-icon class="icon-header" size="100"> {{ icon }} </v-icon>
      <v-card-title class="headline">
        <span class="title-dialog"> {{ title }} </span>
      </v-card-title>
      <v-card-text> {{ message }} </v-card-text>
    </v-card>
  </v-dialog>
</template>

<script>
export default {
  props: ["dialogMsg", "title", "message", "icon"]
};
</script>

<style scoped>
.v-card:not(.v-sheet--tile):not(.v-card--shaped) {
  text-align: center;
}

.title-dialog {
  margin: auto;
}
</style>
