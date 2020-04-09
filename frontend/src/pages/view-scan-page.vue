<template>
  <div class="container-map">
    <l-map class="map" :zoom="zoom" :center="center">
      <l-tile-layer :url="url"></l-tile-layer>
      <l-marker :lat-lng="markerLatLng"></l-marker>
    </l-map>
    <v-container class="container-tables">
      <v-container class="container-header">
        <h2>
          <v-icon>public</v-icon>
          <span class="title-ip">{{ ip }}</span>
          <small class="title-domain">{{ domain }}</small>
        </h2>
      </v-container>
      <v-container>
        <v-row>
          <v-col cols="6">
            <v-simple-table>
              <template v-slot:default>
                <thead>
                  <h3 class="text-left">Geo Location</h3>
                </thead>
                <tbody>
                  <tr>
                    <td>City</td>
                    <td v-if="geo.city">{{ geo.city }}</td>
                    <td v-else>--</td>
                  </tr>
                  <tr>
                    <td>Country</td>
                    <td v-if="geo.country">{{ geo.country }}</td>
                    <td v-else>--</td>
                  </tr>
                  <tr>
                    <td>Organization</td>
                    <td v-if="geo.org">{{ geo.org }}</td>
                    <td v-else>--</td>
                  </tr>
                  <tr>
                    <td>ISP</td>
                    <td v-if="geo.isp">{{ geo.isp }}</td>
                    <td v-else>--</td>
                  </tr>
                  <tr>
                    <td>Region Name</td>
                    <td v-if="geo.region_name">{{ geo.region_name }}</td>
                    <td v-else>--</td>
                  </tr>
                  <tr>
                    <td>ZIP</td>
                    <td v-if="geo.zip">{{ geo.zip }}</td>
                    <td v-else>--</td>
                  </tr>
                </tbody>
              </template>
            </v-simple-table>
          </v-col>
          <v-col cols="6">
            <v-simple-table>
              <template v-slot:default>
                <thead>
                  <h3 class="text-left">Nobita</h3>
                </thead>
                <tbody>
                  <tr v-for="(item, index) in nobita" :key="index">
                    <td>{{ item.port }}</td>
                    <td>{{ item.banner }}</td>
                  </tr>
                </tbody>
              </template>
            </v-simple-table>
          </v-col>
        </v-row>
        <v-row>
          <v-col cols="6">
            <v-simple-table>
              <template v-slot:default>
                <thead>
                  <h3 class="text-left">Suneo</h3>
                </thead>
                <div v-if="suneo">
                  <tbody>
                    <tr>
                      <td>CMS</td>
                      <td v-if="suneo.cms">{{ suneo.cms }}</td>
                      <td v-else>--</td>
                    </tr>
                  </tbody>
                  <h4>Technologies</h4>
                  <div class="suneo-tech" v-if="suneo.technologies">
                    <div
                      class="suneo-tech-item"
                      v-for="(tech, index) in suneo.technologies"
                      :key="index"
                    >{{ tech }}</div>
                  </div>
                  <div v-else>--</div>
                </div>
              </template>
            </v-simple-table>
          </v-col>
          <v-col cols="6">
            <v-simple-table>
              <template v-slot:default>
                <thead>
                  <h3 class="text-left">Shizuka</h3>
                </thead>
                <tbody>
                  <tr v-for="(item, index) in shizuka" :key="index">
                    <td>{{ item }}</td>
                  </tr>
                </tbody>
              </template>
            </v-simple-table>
          </v-col>
        </v-row>
      </v-container>
      <v-container>
        <v-simple-table>
          <template v-slot:default>
            <thead>
              <th class="text-left">Gigante</th>
            </thead>
            <tbody>
              <tr v-for="(item, index) in gigante" :key="index">
                <td>{{ index }}</td>
                <td>{{ item }}</td>
              </tr>
            </tbody>
          </template>
        </v-simple-table>
      </v-container>
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
    LMarker
  },
  data: () => ({
    url: "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
    zoom: 8,
    center: [40.4168, -3.70379],
    markerLatLng: [40.4168, -3.70379],
    domain: "",
    ip: "",
    nobita: [],
    shizuka: [],
    suneo: {},
    gigante: {},
    geo: {}
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
        .then(r => {
          console.log(r.data);
          r.data.forEach(e => {
            if (e.type === "nobita") {
              e.data.forEach(i => {
                this.nobita.push(i);
              });
            }
            if (e.type === "shizuka") {
              e.data.forEach(i => {
                this.shizuka.push(i.domain);
              });
            }
            if (e.type === "suneo") {
              this.suneo = e.data;
            }
            if (e.type === "geo") {
              this.geo = e.data;
              this.ip = e.data.ip;
              this.domain = e.data.domain;
              this.loadLocation(this.geo.lat, this.geo.lon);
            }
          });
        })
        .catch(e => {
          console.log(e.response);
        });
    },

    loadLocation(lat, lon) {
      if (lat !== undefined || lon !== undefined) {
        this.center = [lat, lon];
        this.markerLatLng = [lat, lon];
      }
    },

    getToken() {
      let token = {
        headers: {
          Authorization: "Bearer " + this.$store.state.token
        }
      };
      return token;
    }
  }
};
</script>

<style>
h2,
h3 {
  font-family: "Helvetica", sans-serif;
}

.container-map {
  height: 300px;
  width: 100%;
}

.map {
  height: 100%;
  width: 100%;
}

.title-ip {
  color: rgba(0, 0, 0, 0.54);
}

.title-domain {
  font-size: 18px;
  padding-left: 10px;
  font-weight: 400;
  color: #999;
}

.suneo-tech {
  padding: 16px 0px;
}

.suneo-tech-item {
  font-family: "Roboto", sans-serif;
  padding: 0px 16px;
}
</style>
