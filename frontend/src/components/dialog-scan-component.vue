<template>
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
              <v-textarea v-model="editedItem.hosts" label="Hosts" clearable></v-textarea>
            </v-col>
          </v-row>
        </v-container>
        <v-container>
          <v-row>
            <v-col>
              <Select
                :bots="bots"
                @listBots="selectedBots = $event"
                :value="editedItem.bots"
                :listBots="(editedItem.bots = selectedBots)"
              ></Select>
            </v-col>
          </v-row>
        </v-container>
        <v-container fluid>
          <v-checkbox v-model="checkbox" label="Schedule"></v-checkbox>
        </v-container>
        <v-container v-if="checkbox">
          <v-row>
            <v-col>
              <v-menu
                v-model="menu2"
                :close-on-content-click="false"
                :nudge-right="40"
                transition="scale-transition"
                offset-y
                min-width="290px"
              >
                <template v-slot:activator="{ on }">
                  <v-text-field
                    v-model="date"
                    label="Picker without buttons"
                    prepend-icon="event"
                    readonly
                    v-on="on"
                  ></v-text-field>
                </template>
                <v-date-picker v-model="date" @input="menu2 = false"></v-date-picker>
              </v-menu>
            </v-col>
            <v-col>
              <v-menu
                ref="menu"
                v-model="menu"
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
                  v-if="menu"
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
        <v-btn color="blue darken-1" text @click="$emit('isShow', false)">Cancel</v-btn>
        <v-btn color="blue darken-1" text @click="save">Save</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
import axios from "axios";
import Select from "../components/select-component";

export default {
  components: {
    Select
  },
  props: ["dialog"],
  data: () => ({
    formTitle: "New Scan",
    newItem: {},
    editedIndex: -1,
    editedItem: {
      name: "",
      bots: [],
      executiontime: "",
      hosts: ""
    },
    bots: [],
    botsAll: [],
    selectedBots: [],
    date: new Date().toISOString().substr(0, 10),
    menu2: false,
    time: null,
    menu: false,
    checkbox: false
  }),

  created() {
    this.initializeBots();
  },

  methods: {
    initializeBots() {
      let token = this.getToken();

      axios
        .get("http://localhost:5000/bots", token)
        .then(r => {
          for (let i in r.data) {
            this.bots.push(r.data[i].name);
            this.botsAll.push(r.data);
          }
        })
        .catch(e => {
          console.log(e.response);
        });
    },

    save() {
      if (this.editedItem.executiontime === "") {
        this.editedItem.executiontime = this.dateNow();
      } else {
        // If Scheduled
        this.editedItem.executiontime = this.date + " " + this.time;
      }
      this.$emit("newScan", this.editedItem);
      this.$emit("isShow", false);
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

    dateNow() {
      let time = new Date().toLocaleTimeString();
      let date = new Date().toISOString().substr(0, 10);
      return date + " " + time;
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
  padding: 0%;
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