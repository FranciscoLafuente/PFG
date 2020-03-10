<template>
  <v-container>
    <v-data-table :headers="headers" :items="bots" sort-by="Bot Name" class="elevation-1">
      <template v-slot:top>
        <v-toolbar flat color="white">
          <v-toolbar-title>{{ title }}</v-toolbar-title>
          <v-spacer></v-spacer>
          <dialogToken :dialog="dialog" :tokenBot="tokenBot" @isShow="dialog = $event"></dialogToken>
        </v-toolbar>
      </template>
      <template v-slot:item.action="{ item }">
        <v-icon small class="button-add mr-2" @click="generateToken(item)">add</v-icon>
      </template>
      <template v-slot:no-data>
        <v-btn color="primary" @click="initialize">Reset</v-btn>
      </template>
    </v-data-table>
    <div class="folder-button">
      <v-btn color="blue darken-1" @click="dialogBot = true" dark fab>
        <dialogBot
          :dialogBot="dialogBot"
          @isShow="dialogBot = $event"
          @newBot="editedItem = $event"
        ></dialogBot>
        <v-icon>add</v-icon>
      </v-btn>
    </div>
  </v-container>
</template>

<script>
import axios from "axios";
import dialogToken from "../components/dialog-generateToken-component";
import dialogBot from "../components/dialog-bot-component";

export default {
  components: {
    dialogToken,
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
      { text: "IP", value: "ip" },
      { text: "Type Bot", value: "type" },
      { text: "Generate Token", value: "action", sortable: false }
    ],
    bots: [],
    currentBot: Number,
    editedItem: {},
    tokenBot: ""
  }),

  watch: {
    editedItem() {
      if (this.editedItem.name != "") {
        // && this.editItem.ip != "" && this.editedItem.type != []
        this.addBot();
        console.log("EditBot in watch");
      }
    }
  },

  created() {
    this.initialize();
  },

  methods: {
    initialize() {
      let token = this.getToken();
      axios
        .get("http://localhost:5000/bots", token)
        .then(r => {
          r.data.forEach(e => {
            this.bots.push(e);
          });
        })
        .catch(e => {
          console.log(e.response);
        });
    },

    addBot() {
      let token = this.getToken();
      axios
        .post("http://localhost:5000/bots", this.editedItem, token)
        .then(r => {
          this.bots.push(r.data);
        })
        .catch(e => {
          console.log(e.response);
        });
    },

    generateToken(item) {
      this.currentBot = item._id;
      //let token = this.getToken()
      axios
        .post("http://localhost:5000/bots/" + this.currentBot)
        .then(r => {
          this.tokenBot = JSON.parse(JSON.stringify(r.data));
        })
        .catch(e => {
          console.log(e.response);
        });

      this.dialog = true;
    },

    deleteItem(item) {
      const index = this.projects.indexOf(item);
      confirm("Are you sure you want to delete this item?") &&
        this.projects.splice(index, 1);
    },

    save(projectsUpdated) {
      Object.assign(this.projects, projectsUpdated);
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

.button-add {
  display: flex;
  margin-left: 2.6em;
}

.v-btn--icon.v-size--default .v-icon,
.v-btn--fab.v-size--default .v-icon {
  font-size: 40px;
}

.select-bots {
  padding: inherit;
}
</style>
