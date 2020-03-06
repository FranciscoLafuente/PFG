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
                    <v-col>
                      <v-text-field v-model="editedItem.name" label="Scan name"></v-text-field>
                    </v-col>
                  </v-row>
                </v-container>
                <v-container>
                  <v-row>
                    <v-col>
                      <v-textarea v-model="editedItem.hosts" label="Hosts" clearable=""></v-textarea>
                    </v-col>
                  </v-row>
                </v-container>
                <v-container>
                  <v-row>
                    <v-col>
                      <Select :bots="bots" @listBots="selectedBots = $event" :value="editedItem.bots" 
                      :listBots="(editedItem.bots = selectedBots)"></Select>
                    </v-col>
                  </v-row>
                </v-container>
                <v-container>
                  <v-row>
                    <v-col>
                      <v-menu
                        ref="menu"
                        v-model="menu"
                        :close-on-content-click="false"
                        :return-value.sync="date"
                        transition="scale-transition"
                        offset-y
                        min-width="290px"
                      >
                        <template v-slot:activator="{ on }">
                          <v-text-field
                            v-model="date"
                            label="Picker in menu"
                            prepend-icon="event"
                            readonly
                            v-on="on"
                          ></v-text-field>
                        </template>
                        <v-date-picker v-model="date" no-title scrollable :min-date="new Date()">
                          <v-spacer></v-spacer>
                          <v-btn text color="primary" @click="menu = false">Cancel</v-btn>
                          <v-btn text color="primary" @click="$refs.menu.save(date)">OK</v-btn>
                        </v-date-picker>
                      </v-menu>
                    </v-col>
                    <v-col cols="11" sm="5">
                      <v-menu
                        ref="menu"
                        v-model="menu2"
                        :close-on-content-click="false"
                        :nudge-right="40"
                        :return-value.sync="time"
                        transition="scale-transition"
                        offset-y
                        max-width="290px"
                        min-width="290px"
                      >
                        <template v-slot:activator="{ on }">
                          <v-text-field
                            v-model="time"
                            label="Picker in menu"
                            prepend-icon="access_time"
                            readonly
                            v-on="on"
                          ></v-text-field>
                        </template>
                        <v-time-picker
                          v-if="menu2"
                          v-model="time"
                          full-width
                          @click:minute="$refs.menu.save(time)"
                        ></v-time-picker>
                      </v-menu>
                    </v-col>
                  </v-row>
                </v-container>
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
    title: "My Projects",
    dialog: false,
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
    editedIndex: -1,
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
    bots: ["BotA", "BotB", "BotC", "BotD"],
    selectedBots: [],
    date: new Date().toISOString().substr(0, 10),
    menu: false,
    time: null,
    menu2: false,
  }),

  computed: {
    formTitle() {
      return this.editedIndex === -1 ? "New Project" : "New Scan";
    }
  },

  watch: {
    dialog(val) {
      val || this.close();
    }
  },

  created() {
    this.initialize();
  },

  methods: {
    initialize() {
      let token = this.getToken();
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
          console.log(e.response);
        });
    },

    addScan() {
      let token = this.getToken();
      let id = this.editedItem['_id'];     

      axios
        .post("http://localhost:5000/myproject/" + id, this.editedItem, token)
        .then(r => {
          this.save(r.data);
        })
        .catch(e => {
          console.log(e.response);
        });
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
