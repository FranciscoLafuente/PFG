<template>
  <v-container>{{ id_bot }}</v-container>
</template>

<script>
export default {
  data: () => ({
    id_bot: Number
  }),
  created() {
    this.getId();
  },
  methods: {
    getId() {
      this.id_bot = this.$route.params.id.toString();
    }
  }
};
</script>