<template>
  <v-container fluid>
    <v-row dense>
      <v-col cols="4">
        <v-card class="mx-auto" max-width="300">
          <v-card-title>Description</v-card-title>
          <v-card-text>A timeline is displayed with all the dates of the scans performed. Each date links to a page where all the information collected from a specific host appears.</v-card-text>
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
    <div class="text-center pt-2">
      <v-pagination
        v-model="page"
        :length="pageCount"
        @next="getFromApiNext"
        @previous="getFromapiPrev"
      ></v-pagination>
    </div>
  </v-container>
</template>

<script>
import { FETCH_TIMELINE, TIMELINE_ITEMS } from "../store/actions.type";
import { mapGetters } from "vuex";

export default {
  data: () => ({
    id_scan: String,
    domain: String,
    page: 1,
    pageCount: 10,
    itemsPerPage: 7,
    start: 0,
    end: 7
  }),

  mounted() {
    this.id_scan = this.$route.params.id_scan.toString();
    this.domain = this.$route.params.ip.toString();
    let args = {
      id_scan: this.id_scan,
      domain: this.domain
    };
    this.$store.dispatch(`scans/${TIMELINE_ITEMS}`, args).then(() => {
      // Get total pages
      this.pageCount = Math.ceil(this.items / this.itemsPerPage);
      // Get paginated items
      let params = {
        id_scan: this.id_scan,
        domain: this.domain,
        page: this.start,
        size: this.end
      };
      this.$store.dispatch(`scans/${FETCH_TIMELINE}`, params);
    });
  },

  computed: {
    ...mapGetters({ data_tl: "scans/timeline", items: "scans/getItems" })
  },

  methods: {
    getFromApiNext() {
      this.start = this.start + this.itemsPerPage;
      this.end = this.start + this.itemsPerPage;

      let params = {
        id_scan: this.id_scan,
        domain: this.domain,
        page: this.start,
        size: this.end
      };
      this.$store.dispatch(`scans/${FETCH_TIMELINE}`, params);
    },

    getFromapiPrev() {
      this.end = this.end - this.itemsPerPage;
      this.start = this.end - this.itemsPerPage;

      let params = {
        id_scan: this.id_scan,
        domain: this.domain,
        page: this.start,
        size: this.end
      };
      this.$store.dispatch(`scans/${FETCH_TIMELINE}`, params);
    },

    redirectUser(item, i) {
      this.$router.push(`/scan=${this.id_scan}/host=${this.domain}/${i}`);
    }
  }
};
</script>

<style scoped>
.cards-container {
  padding: 2em;
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
