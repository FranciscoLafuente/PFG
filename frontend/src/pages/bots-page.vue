<template>
  <v-container>
    <v-data-table :headers="headers" :items="projects" sort-by="Project Name" class="elevation-1">
      <template v-slot:top>
        <v-toolbar flat color="white">
          <v-toolbar-title>{{ title }}</v-toolbar-title>
          <v-spacer></v-spacer>
          <v-dialog v-model="dialog" max-width="500px">
            <v-card>
              <v-card-title>
                <span class="headline">{{ formTitle }}</span>
              </v-card-title>

              <v-card-text>
                <v-container>
                  <v-row>
                    <v-col cols="12" sm="6" md="4">
                      <v-text-field v-model="editedItem.name" label="Scan name"></v-text-field>
                    </v-col>
                    <v-col cols="12" sm="6" md="4">
                      <v-text-field v-model="editedItem.executiontime" label="Execution Time"></v-text-field>
                    </v-col>
                    <v-col cols="12" sm="6" md="4">
                      <v-text-field v-model="editedItem.hosts" label="Hosts"></v-text-field>
                    </v-col>
                  </v-row>
                </v-container>
                <div class="select-bots">
                  <Select :bots="bots" @listBots="selectedBots = $event" :value="editedItem.bots" 
                  :listBots="(editedItem.bots = selectedBots)"></Select>
                </div>
              </v-card-text>

              <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn color="blue darken-1" text @click="close">Cancel</v-btn>
                <v-btn color="blue darken-1" text @click="addScan">Save</v-btn>
              </v-card-actions>
            </v-card>
          </v-dialog>
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
import Select from "../components/select-component";

export default {
  components: {
    Select
  },
  data: () => ({
    title: "My Bots",
    dialog: false,
    headers: [
      {
        text: "Name Bots",
        align: "left",
        sortable: true,
        value: "name"
      },
      { text: "IPs", value: "ip"},
      { text: "Type", value: "type" },
      { text: "Actions", value: "action", sortable: false }
    ],
    bots: [],
    editedIndex: -1,
    editedItem: {
      name: "",
      bots: 0,
      executiontime: 0,
      hosts: 0
    },
    defaultItem: {
      name: "",
      bots: 0,
      executiontime: 0,
      hosts: 0
    },
    //bots: ["BotA", "BotB", "BotC", "BotD"],
    selectedBots: []
  }),

  computed: {
    formTitle() {
      return this.editedIndex === -1 ? "Generate Token" : "New Bot";
    }
  },

  watch: {
    dialog(val) {
      val || this.close();
    }
  },

  created() {
    //this.initialize();
  },

  methods: {
    initialize() {
      let token = this.getToken();

      axios
        .get("http://localhost:5000/myproject", token)
        .then(r => {
            console.log(r);
        })
        .catch(e => {
          console.log(e.response);
        });
    },

    generateToken() {

    },

    editItem(item) {
      this.editedIndex = this.projects.indexOf(item);          
      this.editedItem = Object.assign({}, item);
      console.log("Esto es en editItem", this.editedItem['_id']);
      
      this.dialog = true;
    },

    deleteItem(item) {
      const index = this.projects.indexOf(item);
      confirm("Are you sure you want to delete this item?") &&
        this.projects.splice(index, 1);
    },

    close() {
      this.dialog = false;
      setTimeout(() => {
        this.editedItem = Object.assign({}, this.defaultItem);
        this.editedIndex = -1;
      }, 300);
    },

    save(projectsUpdated) {
      if (this.editedIndex > -1) {
        Object.assign(this.projects, projectsUpdated);
      } else {
        this.projects.push(this.editedItem);
      }
      this.close();
    },

    getToken() {
      let user = localStorage.getItem("token");
      let token = {
        headers: {
          Authorization: "Bearer " + user
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
