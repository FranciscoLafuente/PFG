<template>
  <div class="worldmap">
    <vue-world-map
      id="worldmap"
      :countryData="visitedCountries"
      :defaultCountryFillColor="map.defaultCountryFillColor"
      :highColor="map.highColor"
      :countryStrokeColor="map.countryStrokeColor"
      :lowColor="map.lowColor"
    ></vue-world-map>
  </div>
</template>

<script>
import VueWorldMap from "vue-world-map";

export default {
  components: {
    VueWorldMap
  },
  props: {
    visitedCountries: Object
  },

  data: () => ({
    map: {
      defaultCountryFillColor: "#999",
      highColor: "grey",
      lowColor: "grey",
      countryStrokeColor: "white"
    }
  })
};
</script>
