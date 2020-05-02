<template>
  <v-card class="my-4 mx-auto" max-width="1200">
    <v-container class="container-map">
      <l-map class="map" :zoom="zoom" :center="center">
        <l-tile-layer :url="url"></l-tile-layer>
        <l-marker :lat-lng="markerLatLng"></l-marker>
      </l-map>
    </v-container>
    <v-container class="container-tables">
      <v-card-title>
        <v-icon>public</v-icon>
        <small class="title-domain">{{ domain }}</small>
      </v-card-title>
      <v-card-text>
        <v-card>
          <v-card-title>Geo</v-card-title>
          <v-card-text>
            <div class="text-subcard" v-for="(element, index) in geoFormat" :key="index">
              <span class="subtitle-2">{{ index }}:&nbsp;&nbsp;</span>
              <span>{{ element }}</span>
            </div>
          </v-card-text>
        </v-card>
        <v-card class="my-2" v-for="(item, i) in scansFormat" :key="i">
          <v-card-title>{{ item.bot.charAt(0).toUpperCase() + item.bot.substr(1) }}</v-card-title>
          <v-card-text class="text-subcard">
            <div v-if="item.bot === 'nobita'">
              <div v-for="(element, index) in item.results" :key="index">
                <div v-for="(e, i) in element" :key="i">
                  <div>
                    <span class="subtitle-2">{{ i }}:&nbsp;&nbsp;</span>
                    <span>{{ e }}</span>
                  </div>
                </div>
              </div>
            </div>
            <div v-if="item.bot === 'shizuka'">
              <div v-for="(element, index) in item.results" :key="index">
                <span class="body-2">{{ element }}</span>
              </div>
            </div>
            <div v-if="item.bot === 'suneo'">
              <div v-for="(element, index) in item.results" :key="index">
                <div v-for="(e, i) in element" :key="i">
                  <div>
                    <span class="subtitle-2">{{ i }}:&nbsp;&nbsp;</span>
                    <span>{{ e }}</span>
                  </div>
                </div>
              </div>
            </div>
          </v-card-text>
        </v-card>
      </v-card-text>
    </v-container>
  </v-card>
</template>

<script>
import { LMap, LTileLayer, LMarker } from "vue2-leaflet";
import { mapGetters } from "vuex";
import { FETCH_INFO } from "../store/actions.type";

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
    scansFormat: [],
    geoFormat: {}
  }),

  created() {
    let id_scan = this.$route.params.id_scan.toString();
    this.domain = this.$route.params.ip.toString();
    //let num = this.$route.params.index.toString();

    this.$store.dispatch(`scans/${FETCH_INFO}`, id_scan).then(() => {
      this.initialize();
    });
  },

  computed: {
    ...mapGetters({
      scan: "scans/oneScan",
      geo: "scans/fullScan"
    })
  },

  methods: {
    initialize() {
      this.scan.forEach(e => {
        let s = {
          bot: Object.keys(e)[0],
          results: Object.values(e)[0]
        };
        this.scansFormat.push(s);
      });
      this.geo.forEach(e => {
        let dict = {
          continent: e["continent"],
          country: e["country"],
          organization: e["organization"]
        };
        this.geoFormat = dict;
        console.log("GEO FORMAT", this.geoFormat);

        this.loadLocation(e[("latitude", e["longitude"])]);
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

.text-subcard {
  text-align: left;
}

.suneo-tech {
  padding: 16px 0px;
}

.suneo-tech-item {
  font-family: "Roboto", sans-serif;
  padding: 0px 16px;
}
</style>
