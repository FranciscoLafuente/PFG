<template>
  <v-container>
    <v-card v-for="(s, i) in data" :key="i" class="my-1" max-width="400">
      <v-card-text>
        <div class="item-ip" @click="redirect(s)">{{ s.ip }}</div>
        <div class="item-org">{{ s.organization }}</div>
        <div class="item-domain">{{ s.domain }}</div>
        <div class="item-country">{{ s.country }}</div>
      </v-card-text>
    </v-card>
  </v-container>
</template>

<script>
import { SEARCH_SCAN } from "../store/actions.type";
import { mapGetters } from "vuex";

export default {
  data: () => ({
    text: ""
  }),

  created() {
    this.text = this.$route.params.searchText.toString();
    this.$store.dispatch(`scans/${SEARCH_SCAN}`, this.text);
  },

  computed: {
    ...mapGetters({ data: "scans/getSearch" })
  },

  methods: {
    redirect(item) {
      this.$router.push(`/scan=${item.scan_user}/host=${item.domain}/0`);
    }
  }
};
</script>

<style scoped>
.item-ip {
  color: #444;
  font-size: 18px;
  font-weight: 700;
  padding: 0 0 0.5em 0;
}

.item-ip:hover {
  cursor: pointer;
  text-decoration: underline solid #444;
}

.item-org {
  font-size: 10px;
  font-weight: 700;
}

.item-domain {
  color: #999;
}

.item-country {
  font-size: 10px;
  font-weight: 400;
}
</style>