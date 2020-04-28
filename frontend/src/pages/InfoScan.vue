<template>
  <v-row class="container">
    <v-col class="col-table" cols="7">
      <v-simple-table>
        <template v-slot:default>
          <thead>
            <h2 class="text-left">Scans:</h2>
          </thead>
          <tbody>
            <tr v-for="(s, index) in scans" :key="index">
              <td class="table-item">
                <div class="item-ip" @click="redirectUser(index, s.domain)">{{ s.ip }}</div>
                <div class="item-org">{{ s.organization }}</div>
                <div class="item-domain">{{ s.domain }}</div>
                <div class="item-country">{{ s.country }}</div>
              </td>
              <td>
                <v-btn icon large color="blue darken-1" @click="toTimeLine(index, s.domain)">
                  <v-icon>event</v-icon>
                </v-btn>
              </td>
            </tr>
          </tbody>
        </template>
      </v-simple-table>
    </v-col>
  </v-row>
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
    ...mapGetters({ scans: "scans/geoInfo" })
  },

  methods: {
    redirectUser(i, domain) {
      this.$router.push(
        `/myproject=${this.id_project}/scan=${this.id_scan}/host=${domain}/${i}`
      );
    },

    toTimeLine(i, domain) {
      this.$router.push(
        `/myproject=${this.id_project}/scan=${this.id_scan}/timeline/host=${domain}`
      );
    }
  }
};
</script>

<style scoped>
h2,
h3 {
  font-family: "Helvetica", sans-serif;
}

.container {
  padding: 2em;
}

.col-map {
  padding: 1em;
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
