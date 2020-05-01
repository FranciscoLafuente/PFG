<template>
  <v-container class="main-container">
    <v-row dense>
      <v-col cols="4">
        <v-card class="mx-auto" max-width="300">
          <v-card-title>Description</v-card-title>
          <v-card-text>Lorem ipsum dolor sit amet consectetur adipisicing elit. Officia corrupti facilis delectus consectetur cum aliquid ad modi! Optio ipsum velit nam! Atque explicabo exercitationem saepe repellat pariatur odio laborum nulla?</v-card-text>
        </v-card>
      </v-col>
      <v-col cols="8" class="scan-col">
        <div class="cards-container">
          <v-card class="mx-auto" min-width="400">
            <v-card color="blue darken-1" flat>
              <v-card-title class="pa-2 lighten-3">
                <h3 class="title font-weight-light text-center grow">
                  <strong class="text-title">Scans Performed</strong>
                </h3>
              </v-card-title>
            </v-card>
            <v-card>
              <v-timeline dense>
                <v-timeline-item v-for="(item, i) in data_tl" :key="i" small>
                  <v-row>
                    <v-btn @click="redirectUser(item, i)">
                      <span v-text="item.created"></span>
                    </v-btn>
                  </v-row>
                </v-timeline-item>
              </v-timeline>
            </v-card>
          </v-card>
        </div>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import { FETCH_TIMELINE, SAVE_FULL_SCAN } from "../store/actions.type";
import { mapGetters } from "vuex";

export default {
  data: () => ({
    id_scan: String,
    domain: String
  }),

  mounted() {
    this.id_scan = this.$route.params.id_scan.toString();
    this.domain = this.$route.params.ip.toString();

    let params = {
      id_scan: this.id_scan,
      domain: this.domain
    };
    this.$store.dispatch(`scans/${FETCH_TIMELINE}`, params);
  },

  computed: {
    ...mapGetters({ data_tl: "scans/timeline" })
  },

  methods: {
    redirectUser(item, i) {
      this.$store.dispatch(`scans/${SAVE_FULL_SCAN}`, item.results);

      this.$router.push(
        `/myproject=${this.id_project}/scan=${this.id_scan}/host=${this.domain}/${i}`
      );
    }
  }
};
</script>

<style scoped>
.main-container {
  margin: 5em;
}

.scan-col {
  justify-content: start;
  text-align: start;
  display: flex;
}

.text-title {
  color: white;
}
</style>
