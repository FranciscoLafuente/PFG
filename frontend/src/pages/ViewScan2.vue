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
          <small class="title-domain">{{ domain }}</small>
        </h2>
      </v-container>
      <v-container>
        <v-row v-for="(item, i) in scan" :key="i">
          <v-col cols="6">
            <v-simple-table>
              <template v-slot:default>
                <thead>
                  <h3 class="text-left">{{ item.bot }}</h3>
                </thead>
                <tbody>
                  <tr v-for="(item, index) in item.results" :key="index">
                    <td>{{ item }}</td>
                  </tr>
                </tbody>
              </template>
            </v-simple-table>
          </v-col>
        </v-row>
      </v-container>
    </v-container>
  </div>
</template>

<script>
import { LMap, LTileLayer, LMarker } from "vue2-leaflet";
import { mapGetters } from "vuex";
import { ONE_SCAN_INFO } from "../store/actions.type";

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
    domain: String,
    ip: String,
    nobita: [],
    shizuka: [],
    suneo: {},
    gigante: {},
    geo: {},
    listNobita: [],
    aux: []
  }),

  created() {
    let id_scan = this.$route.params.id_scan.toString();
    this.domain = this.$route.params.ip.toString();
    let num = this.$route.params.index.toString();
    let params = {
      id_scan: id_scan,
      domain: this.domain,
      num: num
    };
    this.$store.dispatch(`scans/${ONE_SCAN_INFO}`, params).then(() => {});
    this.initialize();
  },

  computed: {
    ...mapGetters({ scan: "scans/oneScan" })
  },

  methods: {
    initialize() {
      console.log("Initialize in ViewScan -scan-", this.scan);

      Array.from(this.scan).forEach(e => {
        console.log("Inside forEach e", e);
      });
    },

    loadLocation(lat, lon) {
      if (lat !== undefined || lon !== undefined) {
        this.center = [lat, lon];
        this.markerLatLng = [lat, lon];
      }
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
