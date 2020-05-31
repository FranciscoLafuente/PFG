<template>
  <div class="container">
    <div class="description">
      <v-card class="mx-auto">
        <v-card-title>Description</v-card-title>
        <v-card-text>
          This page shows the scans of the project. you can choose another bot
          <v-icon small>create</v-icon>&nbsp;, relaunch the scan
          <v-icon small>autorenew</v-icon>&nbsp;, access more detailed information
          <v-icon small>visibility</v-icon>&nbsp;or delete the scan
          <v-icon small>delete</v-icon>&nbsp;.
        </v-card-text>
      </v-card>
    </div>
    <div>
      <v-data-table :headers="headers" :items="scans" class="elevation-1">
        <template v-slot:top>
          <v-toolbar flat color="white">
            <v-toolbar-title>{{ title }}</v-toolbar-title>
            <v-spacer></v-spacer>
          </v-toolbar>
        </template>
        <template v-slot:item.actions="{ item }">
          <v-icon small class="mr-2" @click="editScan(item)">create</v-icon>
          <v-icon small class="mr-2" @click="renewScan(item)">autorenew</v-icon>
          <v-icon
            small
            class="mr-2"
            @click="openScan(item)"
            :disabled="item.done === false"
          >visibility</v-icon>
          <v-icon small @click="deleteScan(item)">mdi-delete</v-icon>
        </template>
      </v-data-table>
      <v-dialog v-model="dialogEdit" persistent max-width="500px">
        <v-card>
          <v-card-title>
            <span class="headline">Edit Scan</span>
          </v-card-title>
          <v-card-text>
            <v-select v-model="newBot" :items="bots" label="Bots"></v-select>
          </v-card-text>
          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn color="blue darken-1" text @click="dialogEdit = false">Cancel</v-btn>
            <v-btn color="blue darken-1" text @click="save">Save</v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>
      <dialogMessage
        :dialogMsg="dialogMsg"
        :title="msg_title"
        :icon="msg_icon"
        :message="msg_text"
        @showMsg="dialogMsg = $event"
      ></dialogMessage>
    </div>
  </div>
</template>

<script>
import { mapGetters } from "vuex";
import {
  FETCH_SCANS,
  //HAVE_SCANS,
  SCAN_RELUNCH,
  SCAN_DELETE,
  FETCH_MY_BOTS,
  SCAN_EDIT
} from "../store/actions.type";
import dialogMessage from "../components/DialogMessage";
import {
  RELUNCH_TITLE,
  RELUNCH_ICON,
  RELUNCH_TEXT,
  RENAME_TITLE,
  RENAME_ICON,
  RENAME_TEXT
} from "../common/dialogMsg";

export default {
  components: { dialogMessage },
  data: () => ({
    title: "SCANS",
    dialogEdit: false,
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
    newBot: "",
    id_project: "",
    select_scan: "",
    msg_title: "",
    msg_icon: "",
    msg_text: ""
  }),

  mounted() {
    this.id_project = this.$route.params.id.toString();
    this.$store.dispatch(`scans/${FETCH_SCANS}`, this.id_project).then(() => {
      this.scans.forEach(e => {
        console.log(e);
      });
    });
    this.$store.dispatch(`bots/${FETCH_MY_BOTS}`);
  },

  computed: {
    ...mapGetters({ scans: "scans/scans", bots: "bots/name" })
  },

  methods: {
    editScan(item) {
      this.select_scan = item.id;
      this.dialogEdit = true;
    },

    renewScan(item) {
      let id_scan = item.id;
      this.$store.dispatch(`scans/${SCAN_RELUNCH}`, id_scan).then(() => {
        this.msg_title = RELUNCH_TITLE;
        this.msg_icon = RELUNCH_ICON;
        this.msg_text = RELUNCH_TEXT;
        this.dialogMsg = true;
      });
    },

    openScan(item) {
      let id_scan = item.id;
      this.$router.push(`/myproject=${this.id_project}/scan=${id_scan}`);
    },

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

    save() {
      this.dialogEdit = false;
      let params = {
        id: this.select_scan,
        name: {
          bot: this.newBot
        }
      };
      this.$store.dispatch(`scans/${SCAN_EDIT}`, params).then(() => {
        this.msg_title = RENAME_TITLE;
        this.msg_icon = RENAME_ICON;
        this.msg_text = RENAME_TEXT;
        this.dialogMsg = true;
      });
    }
  }
};
</script>

<style scoped>
.container {
  height: 90%;
  width: 70%;
}

.description {
  margin: 2em;
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
