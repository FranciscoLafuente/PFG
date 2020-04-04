<template>
  <div class="container-map">
    <l-map class="map" :zoom="zoom" :center="center">
      <l-tile-layer :url="url"></l-tile-layer>
      <l-marker :lat-lng="markerLatLng"></l-marker>
    </l-map>
  </div>
</template>

<script>
import { LMap, LTileLayer, LMarker } from "vue2-leaflet";

export default {
  components: {
    LMap,
    LTileLayer,
    LMarker,
  },
  data() {
    return {
      url: "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
      zoom: 8,
      center: [40.4168, -3.70379],
      markerLatLng: [40.4168, -3.70379],
    };
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
