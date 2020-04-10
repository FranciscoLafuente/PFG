<template>
  <v-row class="container">
    <v-col class="col-map" cols="4">
      <WorldMap :visitedCountries="visitedCountries"></WorldMap>
    </v-col>
    <v-col class="col-table" cols="8">
      <v-simple-table>
        <template v-slot:default>
          <thead>
            <h2 class="text-left">Scans:</h2>
          </thead>
          <tbody>
            <tr v-for="s in scan" :key="s.ip">
              <td class="table-item">
                <a>
                  <div class="item-ip">{{ s.ip }}</div>
                </a>
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
import axios from "axios";
import constants from "../constants";
import WorldMap from "../components/map-component";
import Countries from "./countries.js";

export default {
  components: {
    WorldMap,
  },
  data: () => ({
    scan: [],
    id_scan: "",
    countries: Countries,
    visitedCountries: {},
  }),

  created() {
    this.initialize();
  },

  methods: {
    initialize() {
      this.id_scan = this.$route.params.id_scan.toString();
      let token = this.getToken();
      axios
        .get(constants.END_POINT_LOCAL + "/scan/" + this.id_scan, token)
        .then((r) => {
          r.data.forEach((e) => {
            e.forEach((element) => {
              if (element.type === "geo") {
                this.scan.push(element.data);
                // Add to map
                this.addToVisited(element.data.country);
              }
            });
          });
        })
        .catch((error) => {
          console.log(error.response);
        });
    },

    getToken() {
      let token = {
        headers: {
          Authorization: "Bearer " + this.$store.state.token,
        },
      };
      return token;
    },

    addToVisited(name) {
      let code = this.getCode(name);

      let country = {
        name: name,
        code: code,
      };
      this.$set(this.visitedCountries, country.code, 500);
    },

    getCode(country) {
      let code = "";
      this.countries.forEach((e) => {
        if (e.name === country) {
          code = e.code;
        }
      });
      return code;
    },
  },
};
</script>

<style scoped>
a:hover {
  text-decoration: underline solid #444;
}

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
