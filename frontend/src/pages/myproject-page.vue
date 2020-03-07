<template>
  <v-container>
    <v-data-table :headers="headers" :items="projects" sort-by="Project Name" class="elevation-1">
      <template v-slot:top>
        <v-toolbar flat color="white">
          <v-toolbar-title>{{ title }}</v-toolbar-title>
          <v-spacer></v-spacer>

            <dialogScan :dialog="dialog" @isShow="dialog = $event" @newScan="editedItem = $event"></dialogScan>

        </v-toolbar>
      </template>
      <template v-slot:item.action="{ item }">
        <v-icon small class="mr-2" @click="editItem(item)">add</v-icon>
        <v-icon small @click="deleteItem(item)">delete</v-icon>
      </template>
      <template v-slot:no-data>
        <v-btn color="primary" @click="initialize">Reset</v-btn>
      </template>
    </v-data-table>
    <div class="folder-button">
      <v-btn color="blue darken-1" @click="dialog = true" dark fab>
        <v-icon>add</v-icon>
      </v-btn>
    </div>
  </v-container>
</template>

<script>
import axios from "axios";
import dialogScan from "../components/dialog-scan-component";

export default {
  components: {
    dialogScan
  },
  data: () => ({
    title: "My Projects",
    dialog: false,
    dialogProject: false,
    headers: [
      {
        text: "Project Name",
        align: "left",
        sortable: true,
        value: "name"
      },
      { text: "Scans", value: "scans"},
      { text: "Type", value: "type" },
      { text: "Actions", value: "action", sortable: false }
    ],
    projects: [],
    currentProject: Number,
    editedItem: {
      name: "",
      bots: 0,
      executiontime: 0,
      hosts: ""
    },
    defaultItem: {
      name: "",
      bots: 0,
      executiontime: 0,
      hosts: ""
    },
  }),

  watch: {
    editedItem() {
      if(this.editedItem.name != "" && this.editedItem.hosts != "" && this.editedItem.bots != 0) {
        this.addScan()
      }
    }
  },

  created() {
    this.initialize()
  },

  methods: {
    initialize() {
      let token = this.getToken()
      let scans = []

      axios
        .get("http://localhost:5000/myproject", token)
        .then(r => {
          r.data.forEach(e => { //Esto es para poder mostrar los scans por nombre 
            e.scans.forEach(s => {
              scans.push(s.name)
            })
            e.scans = scans
            this.projects.push(e)
            scans = []
          });
        })
        .catch(e => {
          console.log(e.response)
        });
    },

    addScan() {
      let token = this.getToken()
      let id = this.currentProject   

      axios
        .post("http://localhost:5000/myproject/" + id, this.editedItem, token)
        .then(r => {
          this.save(r.data)
        })
        .catch(e => {
          console.log(e.response)
        });
    },

    editItem(item) {
      this.currentProject = item._id    
      console.log("Esto es en editItem", this.currentProject)
      
      this.dialog = true
    },

    deleteItem(item) {
      const index = this.projects.indexOf(item)
      confirm("Are you sure you want to delete this item?") &&
        this.projects.splice(index, 1)
    },

    save(projectsUpdated) {
        Object.assign(this.projects, projectsUpdated)
    },

    getToken() {
      let user = localStorage.getItem("token")
      let token = {
        headers: {
          Authorization: "Bearer " + user
        }
      }
      return token
    },
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
