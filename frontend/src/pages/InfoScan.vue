<template>
  <v-row class="container">
    <v-col class="col-map" cols="5">
      <WorldMap :visitedCountries="visitedCountries"></WorldMap>
    </v-col>
    <v-col class="col-table" cols="7">
      <v-simple-table>
        <template v-slot:default>
          <thead>
            <h2 class="text-left">Scans:</h2>
          </thead>
          <tbody>
            <tr v-for="(s, index) in scans" :key="index">
              <td class="table-item">
                <div class="item-ip" @click="redirectUser(index, s.domain)">
                  {{ s.ip }}
                </div>
                <div class="item-org">{{ s.org }}</div>
                <div class="item-domain">{{ s.domain }}</div>
                <div class="item-country">{{ s.country }}</div>
              </td>
            </tr>
          </tbody>
        </template>
      </v-simple-table>
    </v-col>
  </v-row>
</template>

<script>
import WorldMap from "../components/Map";
import Countries from "../common/countries";
import { mapGetters } from "vuex";
import { FETCH_INFO } from "../store/actions.type";

export default {
  components: {
    WorldMap
  },
  data: () => ({
    id_scan: "",
    countries: Countries,
    visitedCountries: {},
    scanInfo: []
  }),

  created() {
    this.id_scan = this.$route.params.id_scan.toString();
    this.$store.dispatch(`scans/${FETCH_INFO}`, this.id_scan);
    // TODO: no carga la informacion en el mapa
  },

  computed: {
    ...mapGetters({ scans: "scans/geoInfo" }),

    // Add visited countries to the map
    addToVisited: function(name) {
      name.scans.forEach(e => {
        let code = this.getCode(e.country);
        let country = {
          name: name,
          code: code
        };
        this.$set(this.visitedCountries, country.code, 500);
      });
      return true;
    }
  },

  methods: {
    getCode(country) {
      let code = "";
      this.countries.forEach(e => {
        if (e.name === country) {
          code = e.code;
        }
      });
      return code;
    },

    redirectUser(i, domain) {
      this.$router.push(`/scan=${this.id_scan}_scan/host=${domain}/${i}`);
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
