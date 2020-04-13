<template>
  <v-container>
    <v-data-table
      :headers="headers"
      :items="bots"
      sort-by="Bot Name"
      class="elevation-1"
    >
      <template v-slot:top>
        <v-toolbar flat color="white">
          <v-toolbar-title>{{ title }}</v-toolbar-title>
          <v-spacer></v-spacer>
          <dialogToken
            :dialog="dialog"
            :tokenBot="tokenBot"
            @isShow="dialog = $event"
          ></dialogToken>
        </v-toolbar>
      </template>
      <template v-slot:item.action="{ item }">
        <v-icon small class="button-add mr-2" @click="generateToken(item)"
          >add</v-icon
        >
      </template>
      <template v-slot:item.delete="{ item }">
        <v-icon small class="button-delete mr-2" @click="deleteItem(item)"
          >delete</v-icon
        >
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
import dialogToken from "../components/DialogGenerateToken";
import dialogBot from "../components/DialogBot.vue";
import { mapGetters } from "vuex";
import {
  FETCH_BOTS,
  BOT_CREATE,
  BOT_TOKEN,
  BOT_DELETE
} from "../store/actions.type";

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
    editedItem: {
      name: "",
      ip: "",
      type: []
    },
    tokenBot: ""
  }),

  mounted() {
    this.$store.dispatch(`bots/${FETCH_BOTS}`);
  },

  watch: {
    editedItem() {
      if (
        this.editedItem.name !== "" &&
        this.editItem.ip != "" &&
        this.editedItem.type !== []
      ) {
        this.addBot();
      }
    }
  },

  computed: {
    ...mapGetters({ bots: "bots/bots" })
  },

  methods: {
    addBot() {
      this.$store.dispatch(BOT_CREATE, this.editedItem);
    },

    generateToken(item) {
      if (!item.token) {
        this.$store.dispatch(BOT_TOKEN, item.id);
        //let index = this.bots.indexOf(item);
        //this.tokenBot = JSON.parse(JSON.stringify(r.data));
        //this.bots[index].token = this.tokenBot;
        this.dialog = true;
      } else {
        this.alert = true;
      }
    },

    deleteItem(item) {
      if (confirm("Are you sure you want to delete this item?")) {
        this.$store.dispatch(BOT_DELETE, item.id);
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
