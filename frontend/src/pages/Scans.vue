<template>
  <v-container>
    <v-data-table :headers="headers" :items="scans" class="elevation-1">
      <template v-slot:top>
        <v-toolbar flat color="white">
          <v-toolbar-title>{{ title }}</v-toolbar-title>
          <v-spacer></v-spacer>
        </v-toolbar>
      </template>
      <template v-slot:item.actions="{ item }">
        <v-icon small class="mr-2" @click="renewScan(item)">autorenew</v-icon>
        <v-icon small class="mr-2" @click="openScan(item)">visibility</v-icon>
        <v-icon small @click="deleteScan(item)">mdi-delete</v-icon>
      </template>
    </v-data-table>
    <v-dialog v-model="dialog" persistent max-width="195px">
      <v-card>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="green darken-1" text @click="dialog = false">
            <v-icon>clear</v-icon>
          </v-btn>
        </v-card-actions>
        <v-icon class="icon-error">autorenew</v-icon>
        <v-card-title class="headline">
          <span class="title-dialog">Relunched!</span>
        </v-card-title>
        <v-card-text>The scan has been successfully relaunched</v-card-text>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<script>
import { mapGetters } from "vuex";
import { FETCH_SCANS, SCAN_RELUNCH, SCAN_DELETE } from "../store/actions.type";

export default {
  data: () => ({
    title: "SCANS",
    dialog: false,
    headers: [
      {
        text: "Name",
        align: "start",
        sortable: false,
        value: "name"
      },
      { text: "Date", value: "created" },
      { text: "Actions", value: "actions", sortable: false }
    ],
    id_project: ""
  }),

  mounted() {
    this.id_project = this.$route.params.id.toString();
    this.$store.dispatch(`scans/${FETCH_SCANS}`, this.id_project);
  },

  computed: {
    ...mapGetters({ scans: "scans/scans" })
  },

  methods: {
    deleteScan(item) {
      //const index = this.scans.indexOf(item);
      if (confirm("Are you sure you want to delete this item?")) {
        let id_scan = item.id;
        this.$store.dispatch(`scans/${SCAN_DELETE}`, {
          id_project: this.id_project,
          id_scan: id_scan,
          index: this.scans.indexOf(item)
        });
        //this.scans.splice(index, 1);
      }
    },

    openScan(item) {
      let id_scan = item.id;
      this.$router.push(`/scan=${id_scan}`);
    },

    renewScan(item) {
      let id_scan = item.id;
      this.$store.dispatch(`scans/${SCAN_RELUNCH}`, id_scan).then(() => {
        this.dialog = true;
      });
    }
  }
};
</script>

<style scoped>
.container {
  height: 90%;
  width: 80%;
  justify-content: center;
  display: flex;
  align-items: center;
}

.v-application .elevation-1 {
  width: inherit;
}

.v-card:not(.v-sheet--tile):not(.v-card--shaped) {
  text-align: center;
}

.title-dialog {
  margin: auto;
}
</style>
