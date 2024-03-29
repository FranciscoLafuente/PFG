<template>
  <div class="container">
    <div class="description">
      <v-card class="mx-auto">
        <v-card-title>Description</v-card-title>
        <v-card-text>
          This page shows the bots that have been created. A new one can be created with the large
          <v-icon small>add</v-icon>&nbsp; symbol. To do this, you have to choose the type of the bot and the IP from where it will launch. The small
          <v-icon small>add</v-icon>&nbsp; symbol generates a token for the bot, the
          <v-icon small>autorenew</v-icon>&nbsp; button regenerates the token in case it has been lost. The
          <v-icon small>delete</v-icon>&nbsp; button removes the bot.
        </v-card-text>
      </v-card>
    </div>
    <div>
      <v-data-table :headers="headers" :items="myBots" sort-by="Bot Name" class="elevation-1">
        <template v-slot:top>
          <v-toolbar flat color="white">
            <v-toolbar-title>{{ title }}</v-toolbar-title>
            <v-spacer></v-spacer>
            <dialogToken :dialog="dialog" :tokenBot="tokenBot" @isShow="dialog = $event"></dialogToken>
          </v-toolbar>
        </template>
        <template v-slot:item.action="{ item }">
          <div class="action-icons">
            <v-icon small class="mr-2" @click="generateToken(item)">add</v-icon>
            <v-icon small class="mr-2" @click="renewToken(item)">autorenew</v-icon>
            <v-icon small class="mr-2" @click="deleteItem(item)">delete</v-icon>
          </div>
        </template>
      </v-data-table>
      <div class="folder-button">
        <v-btn color="blue darken-1" @click="dialogBot = true" dark fab>
          <dialogBot
            :dialogBot="dialogBot"
            :bots="bots"
            @isShow="dialogBot = $event"
            @newBot="editedItem = $event"
          ></dialogBot>
          <v-icon>add</v-icon>
        </v-btn>
      </div>
      <dialogMessage
        :dialogMsg="dialogMsg"
        :title="msg_title"
        :icon="msg_icon"
        :message="msg_text"
        @showMsg="dialogMsg = $event"
      ></dialogMessage>
    </div>
  </div>
</template>

<script>
import dialogToken from "../components/DialogGenerateToken";
import dialogBot from "../components/DialogBot.vue";
import dialogMessage from "../components/DialogMessage";
import {
  TOKEN_TITLE,
  TOKEN_ICON,
  TOKEN_TEXT,
  GENERIC_TITLE,
  GENERIC_ICON,
  RELUNCH_TITLE,
  RELUNCH_ICON,
  RELUNCH_TEXT
} from "../common/dialogMsg";
import { mapGetters } from "vuex";
import {
  FETCH_MY_BOTS,
  FETCH_BOTS,
  BOT_CREATE,
  BOT_TOKEN,
  BOT_DELETE,
  TOKEN_RELUNCH
} from "../store/actions.type";

export default {
  components: {
    dialogToken,
    dialogBot,
    dialogMessage
  },
  data: () => ({
    title: "Bots",
    dialog: false,
    dialogBot: false,
    dialogMsg: false,
    headers: [
      {
        text: "Bot Name",
        align: "left",
        sortable: true,
        value: "name"
      },
      { text: "IPs", value: "ip" },
      { text: "Type Bot", value: "type" },
      { text: "Actions", value: "action", sortable: false }
    ],
    editedItem: {
      name: "",
      ip: "",
      type: []
    },
    tokenBot: "",
    msg_title: "",
    msg_icon: "",
    msg_text: ""
  }),

  mounted() {
    this.$store.dispatch(`bots/${FETCH_MY_BOTS}`);
    this.$store.dispatch(`bots/${FETCH_BOTS}`);
  },

  watch: {
    editedItem() {
      if (
        this.editedItem.name !== "" &&
        this.editedItem.ip !== "" &&
        this.editedItem.type !== []
      ) {
        this.addBot();
      }
    }
  },

  computed: {
    ...mapGetters({
      myBots: "bots/myBots",
      bots: "bots/bots"
    })
  },

  methods: {
    addBot() {
      this.$store
        .dispatch(`bots/${BOT_CREATE}`, this.editedItem)
        .catch(error => {
          this.setMessage(GENERIC_TITLE, GENERIC_ICON, error);
          this.dialogMsg = true;
        });
    },

    generateToken(item) {
      if (!item.token) {
        this.$store.dispatch(`bots/${BOT_TOKEN}`, item.id).then(res => {
          this.tokenBot = JSON.parse(JSON.stringify(res.data));
        });
        this.dialog = true;
      } else {
        this.setMessage(TOKEN_TITLE, TOKEN_ICON, TOKEN_TEXT);
        this.dialogMsg = true;
      }
    },

    deleteItem(item) {
      if (confirm("Are you sure you want to delete this item?")) {
        this.$store.dispatch(`bots/${BOT_DELETE}`, {
          id: item.id,
          index: this.myBots.indexOf(item)
        });
      }
    },

    renewToken(item) {
      let id = item.id;

      this.$store.dispatch(`bots/${TOKEN_RELUNCH}`, id).then(() => {
        this.setMessage(RELUNCH_TITLE, RELUNCH_ICON, RELUNCH_TEXT);
        this.dialogMsg = true;
      });
    },

    setMessage(title, icon, text) {
      this.msg_title = title;
      this.msg_icon = icon;
      this.msg_text = text;
    }
  }
};
</script>

<style scoped>
.container {
  height: 90%;
  width: 80%;
}

.description {
  margin: 2em;
}

.v-application .elevation-1 {
  width: inherit;
}

.folder-button {
  bottom: 15%;
  right: 10%;
  position: absolute;
}

.delete-icon {
  display: flex;
  justify-content: center;
  align-items: center;
}

.v-btn--icon.v-size--default .v-icon,
.v-btn--fab.v-size--default .v-icon {
  font-size: 40px;
}

.select-bots {
  padding: inherit;
}
</style>
