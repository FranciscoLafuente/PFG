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
    <dialogMessage
      :dialogMsg="dialogMsg"
      :title="msg_title"
      :icon="msg_icon"
      :message="msg_text"
      @showMsg="dialogMsg = $event"
    ></dialogMessage>
  </v-container>
</template>

<script>
import { mapGetters } from "vuex";
import { FETCH_SCANS, SCAN_RELUNCH, SCAN_DELETE } from "../store/actions.type";
import dialogMessage from "../components/DialogMessage";
import { RELUNCH_TITLE, RELUNCH_ICON, RELUNCH_TEXT } from "../common/dialogMsg";

export default {
  components: { dialogMessage },
  data: () => ({
    title: "SCANS",
    dialogMsg: false,
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
    id_project: "",
    msg_title: RELUNCH_TITLE,
    msg_icon: RELUNCH_ICON,
    msg_text: RELUNCH_TEXT
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
      if (confirm("Are you sure you want to delete this item?")) {
        let id_scan = item.id;
        this.$store.dispatch(`scans/${SCAN_DELETE}`, {
          id_project: this.id_project,
          id_scan: id_scan,
          index: this.scans.indexOf(item)
        });
      }
    },

    openScan(item) {
      let id_scan = item.id;
      this.$router.push(`/myproject=${this.id_project}/scan=${id_scan}`);
    },

    renewScan(item) {
      let id_scan = item.id;
      this.$store.dispatch(`scans/${SCAN_RELUNCH}`, id_scan).then(() => {
        this.dialogMsg = true;
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
