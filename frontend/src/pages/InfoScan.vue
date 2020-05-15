<template>
  <v-container fluid>
    <v-row dense>
      <v-col cols="4">
        <v-card class="mx-auto" max-width="300">
          <v-card-title>Description</v-card-title>
          <v-card-text>This page shows the results of the scans performed. There are two links, the one with the calendar icon shows a timeline with all scans in chronological order. The other leads to the result of the last scan.</v-card-text>
        </v-card>
      </v-col>
      <v-col cols="8" class="scan-col">
        <div class="sub-container">
          <v-card v-for="(s, index) in scans" :key="index" class="mx-auto" min-width="400">
            <v-row dense>
              <v-col cols="9">
                <v-card-text>
                  <div class="item-ip" @click="redirectUser(index, s.domain)">{{ s.ip }}</div>
                  <div class="item-org">{{ s.organization }}</div>
                  <div class="item-domain">{{ s.domain }}</div>
                  <div class="item-country">{{ s.country }}</div>
                </v-card-text>
              </v-col>
              <v-col cols="3" class="second-col">
                <v-card-actions>
                  <v-btn icon large color="blue darken-1" @click="toTimeLine(index, s.domain)">
                    <v-icon>event</v-icon>
                  </v-btn>
                </v-card-actions>
              </v-col>
            </v-row>
          </v-card>
        </div>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import { mapGetters } from "vuex";
import { FETCH_INFO } from "../store/actions.type";

export default {
  data: () => ({
    id_scan: String,
    id_project: String,
    visitedCountries: Object,
    scanInfo: Array
  }),

  created() {
    this.id_scan = this.$route.params.id_scan.toString();
    this.id_project = this.$route.params.id.toString();
    this.$store.dispatch(`scans/${FETCH_INFO}`, this.id_scan);
  },

  computed: {
    ...mapGetters({ scans: "scans/fullScan" })
  },

  methods: {
    redirectUser(i, domain) {
      this.$router.push(`/scan=${this.id_scan}/host=${domain}/${i}`);
    },

    toTimeLine(i, domain) {
      this.$router.push(`/scan=${this.id_scan}/timeline/host=${domain}`);
    }
  }
};
</script>

<style scoped>
h2,
h3 {
  font-family: "Helvetica", sans-serif;
}

.sub-container {
  padding: 2em;
}

.scan-col {
  justify-content: start;
  text-align: start;
  display: flex;
}

.second-col {
  justify-content: center;
  text-align: center;
  display: flex;
}

.col-table {
  padding: 1em;
}

.text-left {
  color: #999;
  border-bottom: 1px dashed #aaa;
  display: inline;
  text-transform: uppercase;
}

.table-item {
  font-family: Arial;
  padding: 0.5em 0;
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
