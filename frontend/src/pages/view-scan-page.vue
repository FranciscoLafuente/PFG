<template>
  <div class="container-map">
    <l-map class="map" :zoom="zoom" :center="center">
      <l-tile-layer :url="url"></l-tile-layer>
      <l-marker :lat-lng="markerLatLng"></l-marker>
    </l-map>
    <v-container>
      <div>
        <v-simple-table>
          <template v-slot:default>
            <thead>
              <tr>
                <th class="text-left">Nobita</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(item, index) in nobita" :key="index">
                <td>{{ index }}</td>
                <td>{{ item }}</td>
              </tr>
            </tbody>
          </template>
        </v-simple-table>
      </div>
    </v-container>
    <v-container>
      <div>
        <v-simple-table>
          <template v-slot:default>
            <thead>
              <tr>
                <th class="text-left">Shizuka</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(item, index) in shizuka" :key="index">
                <td>{{ index }}</td>
                <td>{{ item }}</td>
              </tr>
            </tbody>
          </template>
        </v-simple-table>
      </div>
    </v-container>
    <v-container>
      <div>
        <v-simple-table>
          <template v-slot:default>
            <thead>
              <tr>
                <th class="text-left">Sueno</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(item, index) in suneo" :key="index">
                <td>{{ index }}</td>
                <td>{{ item }}</td>
              </tr>
            </tbody>
          </template>
        </v-simple-table>
      </div>
    </v-container>
    <v-container>
      <div>
        <v-simple-table>
          <template v-slot:default>
            <thead>
              <tr>
                <th class="text-left">Gigante</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(item, index) in gigante" :key="index">
                <td>{{ index }}</td>
                <td>{{ item }}</td>
              </tr>
            </tbody>
          </template>
        </v-simple-table>
      </div>
    </v-container>
  </div>
</template>

<script>
import { LMap, LTileLayer, LMarker } from "vue2-leaflet";
import constants from "../constants";
import axios from "axios";

export default {
  components: {
    LMap,
    LTileLayer,
    LMarker,
  },
  data: () => ({
    url: "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
    zoom: 8,
    center: [40.4168, -3.70379],
    markerLatLng: [40.4168, -3.70379],
    nobita: {},
    shizuka: {},
    suneo: {},
    gigante: {},
  }),

  created() {
    this.initialize();
  },

  methods: {
    initialize() {
      let token = this.getToken();
      let id_scan = this.$route.params.id_scan.toString();

      axios
        .get(constants.END_POINT_LOCAL + "/scan/" + id_scan, token)
        .then((r) => {
          console.log(r.data);
          r.data.forEach((e) => {
            if (e.bot === "nobita") {
              this.nobita = e;
              this.loadLocation(e.latitud, e.longitud);
            }
            if (e.bot === "shizuka") {
              this.shizuka = e;
            }
            if (e.bot === "suneo") {
              this.suneo = e;
            }
            if (e.bot === "gigante") {
              this.gigante = e;
            }
          });
        })
        .catch((e) => {
          console.log(e.response);
        });
    },

    loadLocation(lat, long) {
      this.center = [lat, long];
      this.markerLatLng = [lat, long];
    },

    getToken() {
      let token = {
        headers: {
          Authorization: "Bearer " + this.$store.state.token,
        },
      };
      return token;
    },
  },
};
</script>

<style>
.container-map {
  height: 300px;
  width: 100%;
}

.map {
  height: 100%;
  width: 100%;
}
</style>
