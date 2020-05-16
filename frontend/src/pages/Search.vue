<template>
  <v-container>
    <div class="text-center pt-2">
      <v-pagination
        v-model="page"
        :length="pageCount"
        @next="getFromApiNext"
        @previous="getFromapiPrev"
      ></v-pagination>
    </div>
    <div class="content">
      <div v-if="data.length !== 0">
        <v-card v-for="(s, i) in data" :key="i" class="my-1" min-width="400">
          <v-card-text>
            <div class="item-ip" @click="redirect(s)">{{ s.ip }}</div>
            <div class="item-org">{{ s.organization }}</div>
            <div class="item-domain">{{ s.domain }}</div>
            <div class="item-country">{{ s.country }}</div>
          </v-card-text>
        </v-card>
      </div>
      <div v-else>
        <v-card>
          <v-card-title>No items were found with the search performed</v-card-title>
        </v-card>
      </div>
    </div>
  </v-container>
</template>

<script>
import { SEARCH_SCAN, SEARCH_ITEMS_SCAN } from "../store/actions.type";
import { mapGetters } from "vuex";

export default {
  data: () => ({
    options: {},
    text: "",
    page: 1,
    pageCount: 10,
    itemsPerPage: 4,
    start: 0,
    end: 4
  }),

  created() {
    this.text = this.$route.params.searchText.toString();
    this.$store.dispatch(`scans/${SEARCH_ITEMS_SCAN}`, this.text);
    let params = {
      text: this.text,
      page: this.start,
      size: this.end
    };
    this.$store.dispatch(`scans/${SEARCH_SCAN}`, params);
    // Get total pages
    this.pageCount = Math.ceil(this.items / this.itemsPerPage);
  },

  computed: {
    ...mapGetters({ data: "scans/getSearch", items: "scans/getItems" })
  },

  methods: {
    getFromApiNext() {
      this.start = this.start + this.itemsPerPage;
      this.end = this.start + this.itemsPerPage;

      let params = {
        text: this.text,
        page: this.start,
        size: this.end
      };
      this.$store.dispatch(`scans/${SEARCH_SCAN}`, params);
    },

    getFromapiPrev() {
      this.end = this.end - this.itemsPerPage;
      this.start = this.end - this.itemsPerPage;

      let params = {
        text: this.text,
        page: this.start,
        size: this.end
      };
      this.$store.dispatch(`scans/${SEARCH_SCAN}`, params);
    },

    redirect(item) {
      this.$router.push(`/scan=${item.scan_user}/host=${item.domain}/0`);
    }
  }
};
</script>

<style scoped>
.content {
  display: flex;
  justify-content: center;
}

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