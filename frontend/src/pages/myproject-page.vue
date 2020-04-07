<template>
  <v-container>
    <v-data-table :headers="headers" :items="projects" sort-by="Project Name" class="elevation-1">
      <template v-slot:top>
        <v-toolbar flat color="white">
          <v-toolbar-title>{{ title }}</v-toolbar-title>
          <v-spacer></v-spacer>

          <dialogScan
            :dialog="dialog"
            :bots="bots"
            @isShow="dialog = $event"
            @newScan="editedItem = $event"
          ></dialogScan>
        </v-toolbar>
      </template>
      <template v-slot:item.actions="{ item }">
        <v-icon small class="mr-2" @click="editItem(item)">add</v-icon>
        <v-icon small class="mr-2" @click="visualizeScan(item)">visibility</v-icon>
        <v-icon small class="mr" @click="deleteProject(item)">delete</v-icon>
      </template>
    </v-data-table>
    <div class="folder-button">
      <v-btn color="blue darken-1" @click="dialogPro = true" dark fab>
        <dialogProject
          :dialogPro="dialogPro"
          @isShow="dialogPro = $event"
          @newProject="editProject = $event"
        ></dialogProject>
        <v-icon>add</v-icon>
      </v-btn>
    </div>
    <v-dialog v-model="createdScan" persistent max-width="195px">
      <v-card>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="green darken-1" text @click="createdScan = false">
            <v-icon>clear</v-icon>
          </v-btn>
        </v-card-actions>
        <v-icon class="icon-error">done</v-icon>
        <v-card-title class="headline">
          <span class="title-dialog">Success!</span>
        </v-card-title>
        <v-card-text>The scan has been created successfully</v-card-text>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<script>
import axios from "axios";
import dialogScan from "../components/dialog-scan-component";
import dialogProject from "../components/dialog-project-component";
import constants from "../constants";

export default {
  components: {
    dialogScan,
    dialogProject
  },
  data: () => ({
    title: "My Projects",
    dialog: false,
    dialogPro: false,
    createdScan: false,
    headers: [
      {
        text: "Project Name",
        align: "left",
        sortable: true,
        value: "name"
      },
      { text: "Public", value: "type" },
      { text: "Actions", value: "actions", sortable: false }
    ],
    projects: [],
    bots: [],
    fullBots: [],
    currentProject: Number,
    index: Number,
    editedItem: {
      name: "",
      bots: 0,
      executiontime: 0,
      hosts: ""
    },
    editProject: {
      name: "",
      type: true,
      scans: []
    }
  }),

  watch: {
    editedItem() {
      if (
        this.editedItem.name != "" &&
        this.editedItem.hosts != "" &&
        this.editedItem.bots != 0
      ) {
        this.addScan();
      }
    },

    editProject() {
      if (this.editProject.name != "") {
        this.addProject();
      }
    }
  },

  created() {
    this.initialize();
  },

  methods: {
    initialize() {
      let token = this.getToken();
      this.initializeBots(token);

      axios
        .get(constants.END_POINT_LOCAL + "/myproject", token)
        .then(r => {
          r.data.forEach(e => {
            this.projects.push(e);
          });
        })
        .catch(e => {
          console.log(e.response);
        });
    },

    initializeBots(token) {
      axios
        .get(constants.END_POINT_LOCAL + "/bots", token)
        .then(r => {
          r.data.forEach(e => {
            this.bots.push(e.name);
            this.fullBots.push(e);
          });
        })
        .catch(error => {
          console.log(error.response);
        });
    },

    addProject() {
      let token = this.getToken();

      axios
        .post(constants.END_POINT_LOCAL + "/myproject", this.editProject, token)
        .then(r => {
          this.projects.push(r.data);
        })
        .catch(error => {
          console.log(error.response);
        });
    },

    addScan() {
      let token = this.getToken();
      let id = this.currentProject;
      let botId = "";
      this.fullBots.forEach(b => {
        if (this.editedItem.bot === b.name) {
          botId = b.id;
        }
      });

      let scan = {
        name: this.editedItem.name,
        bot: botId,
        executiontime: this.editedItem.executiontime,
        hosts: this.editedItem.hosts
      };

      axios
        .post(constants.END_POINT_LOCAL + "/myproject/" + id, scan, token)
        .then(() => {
          this.createdScan = true;
        })
        .catch(error => {
          console.log(error.response);
        });
    },

    visualizeScan(item) {
      let currentProject = item.id;
      this.$router.push("/myproject/" + currentProject);
    },

    deleteProject(item) {
      const index = this.projects.indexOf(item);
      if (confirm("Are you sure you want to delete this item?")) {
        let token = this.getToken();
        let id = item.id;

        axios
          .delete(constants.END_POINT_LOCAL + "/myproject/" + id, token)
          .then(() => {
            this.projects.splice(index, 1);
          })
          .catch(error => {
            console.log(error.response);
          });
      }
    },

    getToken() {
      let token = {
        headers: {
          Authorization: "Bearer " + this.$store.state.token
        }
      };
      return token;
    },

    editItem(item) {
      this.currentProject = item.id;
      this.index = this.projects.indexOf(item);

      this.dialog = true;
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

.button-add {
  display: flex;
  margin-left: 1.2em;
}

.button-delete {
  display: flex;
  margin-left: 2em;
}

.v-application .elevation-1 {
  width: inherit;
}

.folder-button {
  bottom: 15%;
  right: 10%;
  position: absolute;
}

.v-btn--icon.v-size--default .v-icon,
.v-btn--fab.v-size--default .v-icon {
  font-size: 40px;
}

.select-bots {
  padding: inherit;
}

.v-card:not(.v-sheet--tile):not(.v-card--shaped) {
  text-align: center;
}

.title-dialog {
  margin: auto;
}
</style>
