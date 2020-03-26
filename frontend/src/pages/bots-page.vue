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
      <template v-slot:item.delete="{ item }">
        <v-icon small class="button-delete mr-2" @click="deleteItem(item)">delete</v-icon>
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
    <v-dialog v-model="this.alert" persistent max-width="400px">
      <v-card>
        <v-card-text>
          <v-container>
            <span class="headline">This token already has been created</span>
          </v-container>
        </v-card-text>
        <v-card-actions>
          <v-btn color="blue darken-1" text @click="alert = !alert">OK</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
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
    alert: false,
    headers: [
      {
        text: "Bot Name",
        align: "left",
        sortable: true,
        value: "name"
      },
      { text: "IPs", value: "ip" },
      { text: "Type Bot", value: "type" },
      { text: "Generate Token", value: "action", sortable: false },
      { text: "Delete Bot", value: "delete", sortable: false }
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
      if (item.token === "") {
        let user_token = this.getToken();
        this.currentBot = item._id;

        axios
          .get("http://localhost:5000/bots/" + this.currentBot, user_token)
          .then(r => {
            this.tokenBot = JSON.parse(JSON.stringify(r.data[0]));
            // Search de index in bots array
            const index = this.bots.findIndex(e => e._id === this.currentBot);
            // Change the value with the generated token
            Object.assign(this.bots[index], r.data[1]);
          })
          .catch(e => {
            console.log(e.response);
          });

        this.dialog = true;
      } else {
        this.alert = true;
      }
    },

    deleteItem(item) {
      const index = this.bots.indexOf(item);
      if (confirm("Are you sure you want to delete this item?")) {
        let token = this.getToken();
        let id = item._id;

        axios
          .delete("http://localhost:5000/bots/" + id, token)
          .then(() => {
            this.bots.splice(index, 1);
          })
          .catch(e => {
            console.log(e.response);
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
  margin-left: 2em;
}

.button-delete {
  display: flex;
  margin-left: 1.5em;
}

.v-btn--icon.v-size--default .v-icon,
.v-btn--fab.v-size--default .v-icon {
  font-size: 40px;
}

.select-bots {
  padding: inherit;
}
</style>
