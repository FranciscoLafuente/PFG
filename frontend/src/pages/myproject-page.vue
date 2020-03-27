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
      <template v-slot:item.action="{ item }">
        <v-icon small class="button-add mr-2" @click="editItem(item)">add</v-icon>
      </template>
      <template v-slot:item.delete="{ item }">
        <v-icon small class="button-delete" @click="deleteItem(item)">delete</v-icon>
      </template>
      <template v-slot:no-data>
        <v-btn color="primary" @click="initialize">Reset</v-btn>
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
  </v-container>
</template>

<script>
import axios from "axios";
import dialogScan from "../components/dialog-scan-component";
import dialogProject from "../components/dialog-project-component";

export default {
  components: {
    dialogScan,
    dialogProject
  },
  data: () => ({
    title: "My Projects",
    dialog: false,
    dialogPro: false,
    headers: [
      {
        text: "Project Name",
        align: "left",
        sortable: true,
        value: "name"
      },
      { text: "Scans", value: "scans" },
      { text: "Public", value: "type" },
      { text: "New Scan", value: "action", sortable: false },
      { text: "Delete Project", value: "delete", sortable: false }
    ],
    projects: [],
    bots: [],
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
      let scans = [];

      axios
        .get("http://localhost:5000/myproject", token)
        .then(r => {
          r.data.forEach(e => {
            // Show scans by name
            e.scans.forEach(s => {
              scans.push(s.name);
            });
            e.scans = scans;
            this.projects.push(e);
            scans = [];
          });
        })
        .catch(e => {
          console.log(e.response);
        });
    },

    addScan() {
      let token = this.getToken();
      let id = this.currentProject;

      axios
        .post("http://localhost:5000/myproject/" + id, this.editedItem, token)
        .then(r => {
          this.projects[this.index].scans.push(r.data["name"]);
        })
        .catch(e => {
          console.log(e.response);
        });
    },

    initializeBots(token) {
      axios
        .get("http://localhost:5000/bots", token)
        .then(r => {
          for (let i in r.data) {
            this.bots.push(r.data[i].name);
          }
        })
        .catch(e => {
          console.log(e.response);
        });
    },

    addProject() {
      let token = this.getToken();

      axios
        .post("http://localhost:5000/myproject", this.editProject, token)
        .then(r => {
          this.projects.push(r.data);
        })
        .catch(e => {
          console.log(e.response);
        });
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
      this.currentProject = item._id;
      this.index = this.projects.indexOf(item);

      this.dialog = true;
    },

    deleteItem(item) {
      const index = this.projects.indexOf(item);
      if (confirm("Are you sure you want to delete this item?")) {
        let token = this.getToken();
        let id = item._id;

        axios
          .delete("http://localhost:5000/myproject/" + id, token)
          .then(() => {
            this.projects.splice(index, 1);
          })
          .catch(e => {
            console.log(e.response);
          });
      }
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
</style>
