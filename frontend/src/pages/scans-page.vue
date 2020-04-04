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
  </v-container>
</template>

<script>
import constants from "../constants";
import axios from "axios";

export default {
  data: () => ({
    title: "SCANS",
    dialog: false,
    headers: [
      {
        text: "IP",
        align: "start",
        sortable: false,
        value: "hosts"
      },
      { text: "Country", value: "country" },
      { text: "Date", value: "created" },
      { text: "ISP", value: "isp" },
      { text: "Actions", value: "actions", sortable: false }
    ],
    scans: [],
    id_project: ""
  }),

  created() {
    this.initialize();
  },

  methods: {
    initialize() {
      this.id_project = this.$route.params.id.toString();
      let token = this.getToken();
      axios
        .get(constants.END_POINT_LOCAL + "/myproject/" + this.id_project, token)
        .then(r => {
          r.data.forEach(e => {
            console.log(e);
            this.scans.push(e);
          });
        })
        .catch(error => {
          console.log(error.response);
        });
    },

    deleteScan(item) {
      const index = this.scans.indexOf(item);
      if (confirm("Are you sure you want to delete this item?")) {
        let token = this.getToken();
        let id_scan = item._id;

        axios
          .delete(
            constants.END_POINT_LOCAL +
              "/myproject/" +
              this.id_project +
              "/" +
              id_scan,
            token
          )
          .then(() => {
            this.scans.splice(index, 1);
          })
          .catch(e => {
            console.log(e.response);
          });
      }
    },

    openScan(item) {
      let id_scan = item._id;
      this.$router.push("/myproject/" + this.id_project + "/scan/" + id_scan);
    },

    renewScan(item) {
      //let token = this.getToken();
      let id_scan = item._id;

      axios
        .put(constants.END_POINT_LOCAL + "/myproject/scan/" + id_scan)
        .then(r => {
          console.log(r.data);
        })
        .catch(error => {
          console.log(error.response);
        });
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
</style>