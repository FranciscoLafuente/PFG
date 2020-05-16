<template>
  <v-container>
    <v-card :elevation="9" class="form-card">
      <form enctype="multipart/form-data" @keypress.enter="upload" class="form-data">
        <div class="my-3">
          <h1>
            {{ title }}
            <em>Shodita</em>
          </h1>
        </div>

        <v-text-field v-model="name" label="Bot name" prepend-icon="adb" required></v-text-field>

        <v-file-input
          v-model="file"
          accept="text/x-python"
          placeholder="Pick an field"
          prepend-icon="attach_file"
          label="File"
        ></v-file-input>

        <v-textarea v-model="description" prepend-icon="reorder" label="Bot description"></v-textarea>

        <v-btn color="blue darken-1" dark class="mr-4" @click="upload">Upload</v-btn>
        <div class="description">
          <h4>How upload</h4>
          <p
            class="paragraph"
          >To upload a bot, you have to assign a name to it, select a file containing the bot with a .py extension and a short description of how it works. It should have the following imports: from abc import abstractmethod, ABC and from cement import Interface, Handler. Then there must be 2 classes, the first with the name you want plus Interface (Interface), for example: class BotInterface (Interface). Within this class, you have to clarify another one as follows: class Meta: and then, interface = 'anynameIf', This declares the methods to be used, with the @abstractmethod decorator. The second class must be created as follows: class BotHandler (BotInterface, Handler, ABC), with an internal class: class Meta: label = 'any name' and the methods you want, and a main one bot_scan (self, * args) which will be called from the main function.</p>
        </div>
      </form>
    </v-card>
    <dialogMessage
      :dialogMsg="dialogMsg"
      :title="msg_title"
      :icon="msg_icon"
      :message="msg_text"
      @showMsg="dialogMsg = $event"
    ></dialogMessage>
  </v-container>
</template>


<script>
import dialogMessage from "../components/DialogMessage";
import { UPLOAD_TITLE, UPLOAD_ICON, UPLOAD_TEXT } from "../common/dialogMsg";
import { BOT_UPLOAD } from "../store/actions.type";

export default {
  components: { dialogMessage },
  data: () => ({
    dialogMsg: false,
    title: "Add your own bot to",
    name: "",
    file: {},
    description: "",
    msg_title: "",
    msg_icon: "",
    msg_text: ""
  }),

  methods: {
    upload() {
      const formData = new FormData();
      formData.append("file", this.file);
      formData.append("name", this.name);
      formData.append("description", this.description);

      this.$store.dispatch(`bots/${BOT_UPLOAD}`, formData).then(() => {
        this.msg_title = UPLOAD_TITLE;
        this.msg_icon = UPLOAD_ICON;
        this.msg_text = UPLOAD_TEXT;
        this.dialogMsg = true;
        (this.file = {}), (this.name = ""), (this.description = "");
      });
    }
  }
};
</script>

<style scoped>
.container {
  width: 100%;
  height: 88%;
  display: flex;
  justify-content: center;
  text-align: center;
}

.form-card {
  width: 70%;
  padding: inherit;
  margin: auto;
  display: flex;
  justify-content: center;
  text-align: center;
}

.form-data {
  width: 80%;
}

h1 {
  font-size: 1.6rem;
  font-weight: 300;
}
em {
  font-style: normal;
  font-weight: 700;
}

a {
  font-size: 1rem;
  color: #888;
  margin: 1em 0 0.5em;
  float: right;
}

a:link,
a:visited,
a:active {
  text-decoration: none;
}

.v-card:not(.v-sheet--tile):not(.v-card--shaped) {
  text-align: center;
}

.title-dialog {
  margin: auto;
}

.description {
  text-align: left;
  margin: 2em;
}
.paragraph {
  color: #888;
  font-size: 14px;
}
</style>