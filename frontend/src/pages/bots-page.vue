<template>
  <v-container>
    <v-data-table :headers="headers" :items="bots" sort-by="Bot Name" class="elevation-1">
      <template v-slot:top>
        <v-toolbar flat color="white">
          <v-toolbar-title>{{ title }}</v-toolbar-title>
          <v-spacer></v-spacer>

            <dialogScan :dialog="dialog" @isShow="dialog = $event" @newScan="editedItem = $event"></dialogScan>

        </v-toolbar>
      </template>
      <template v-slot:item.action="{ item }">
        <v-icon small class="mr-2" @click="editItem(item)">add</v-icon>
      </template>
      <template v-slot:no-data>
        <v-btn color="primary" @click="initialize">Reset</v-btn>
      </template>
    </v-data-table>
    <div class="folder-button">
      <v-btn color="blue darken-1" @click="dialogBot = true" dark fab>
        <dialogBot :dialogBot="dialogBot" @isShow="dialogBot = $event" @newBot="editedItem = $event"></dialogBot>
        <v-icon>add</v-icon>
      </v-btn>
    </div>
  </v-container>
</template>

<script>
import axios from "axios";
import dialogScan from "../components/dialog-scan-component";
import dialogBot from "../components/dialog-bot-component"

export default {
  components: {
    dialogScan,
    dialogBot
  },
  data: () => ({
    title: "Bots",
    dialog: false,
    dialogBot: false,
    headers: [
      {
        text: "Bot Name",
        align: "left",
        sortable: true,
        value: "name"
      },
      { text: "IP", value: "ip"},
      { text: "Type Bot", value: "type" },
      { text: "Generate Token", value: "action", sortable: false }
    ],
    bots: [],
    currentProject: Number,
    editedItem: {
      name: "",
      ip: "",
      type: [],
    },
  }),

  watch: {
    editedItem() {
      if(this.editedItem.name != "") { // && this.editItem.ip != "" && this.editedItem.type != []
        console.log("EditBot in watch");
      }
    },
  },

  created() {
    this.initialize()
  },

  methods: {
    initialize() {
      let token = this.getToken()

      axios
        .get("http://localhost:5000/myproject", token)
        .then(r => {
          console.log(r.data);
          
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

    addProject() {
      let token = this.getToken()

      let new_project = {}

      axios
        .post("http://localhost:5000/myproject", this.editProject, token)
        .then(r => {
          console.log("Data del back", r.data);
          
          new_project = {
            'name': r.data.name,
            'type': r.data.type,
            'scans': [],
          }
          this.projects.push(new_project)
          console.log("Nuevo Projecto", new_project);
          console.log("Lista de Projects", this.projects);
          
          
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
