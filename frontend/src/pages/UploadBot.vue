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
          label="Bot"
        ></v-file-input>

        <v-btn color="blue darken-1" dark class="mr-4" @click="upload">Upload</v-btn>
        <div class="description">
          <h4>Description</h4>
          <p
            class="paragraph"
          >Lorem, ipsum dolor sit amet consectetur adipisicing elit. Ea numquam, tempore dignissimos sed, repellendus excepturi aliquam aut, sunt natus similique qui. Unde omnis veniam inventore, animi et magni soluta labore!</p>
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
    msg_title: "",
    msg_icon: "",
    msg_text: ""
  }),

  methods: {
    upload() {
      let params = {
        name: this.name,
        file: this.file
      };
      this.$store.dispatch(`bots/${BOT_UPLOAD}`, params).then(() => {
        this.msg_title = UPLOAD_TITLE;
        this.msg_icon = UPLOAD_ICON;
        this.msg_text = UPLOAD_TEXT;
        this.dialogMsg = true;
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
  width: 40%;
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