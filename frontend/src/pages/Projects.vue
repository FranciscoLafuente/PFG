<template>
  <v-container>
    <v-data-table
      :headers="headers"
      :items="projects"
      sort-by="Project Name"
      class="elevation-1"
    >
      <template v-slot:top>
        <v-toolbar flat color="white">
          <v-toolbar-title>{{ title }}</v-toolbar-title>
          <v-spacer></v-spacer>

          <dialogScan
            :dialog="dialog"
            :bots="bots"
            @isShow="dialog = $event"
            @newScan="editedItem = $event"
          ></dialogScan>
        </v-toolbar>
      </template>
      <template v-slot:item.actions="{ item }">
        <v-icon small class="mr-2" @click="editItem(item)">add</v-icon>
        <v-icon small class="mr-2" @click="visualizeScan(item)"
          >visibility</v-icon
        >
        <v-icon small class="mr" @click="deleteProject(item)">delete</v-icon>
      </template>
    </v-data-table>
    <div class="folder-button">
      <v-btn color="blue darken-1" @click="dialogPro = true" dark fab>
        <dialogProject
          :dialogPro="dialogPro"
          @isShow="dialogPro = $event"
          @newProject="editProject = $event"
        ></dialogProject>
        <v-icon>add</v-icon>
      </v-btn>
    </div>
    <v-dialog v-model="createdScan" persistent max-width="195px">
      <v-card>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="green darken-1" text @click="createdScan = false">
            <v-icon>clear</v-icon>
          </v-btn>
        </v-card-actions>
        <v-icon class="icon-error">done</v-icon>
        <v-card-title class="headline">
          <span class="title-dialog">Success!</span>
        </v-card-title>
        <v-card-text>The scan has been created successfully</v-card-text>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<script>
import dialogScan from "../components/DialogScan";
import dialogProject from "../components/DialogProject";
import { mapGetters } from "vuex";
import {
  FETCH_PROJECTS,
  PROJECT_CREATE,
  PROJECT_DELETE,
  FETCH_BOTS,
  SCAN_CREATE
} from "../store/actions.type";

export default {
  components: {
    dialogScan,
    dialogProject
  },
  data: () => ({
    title: "My Projects",
    dialog: false,
    dialogPro: false,
    createdScan: false,
    headers: [
      {
        text: "Project Name",
        align: "left",
        sortable: true,
        value: "name"
      },
      { text: "Public", value: "type" },
      { text: "Actions", value: "actions", sortable: false }
    ],
    currentProject: Number,
    index: Number,
    editedItem: {
      name: "",
      bots: 0,
      executiontime: 0,
      hosts: ""
    },
    editProject: {
      name: "",
      type: true,
      scans: []
    }
  }),

  mounted() {
    this.$store.dispatch(`project/${FETCH_PROJECTS}`);
    this.$store.dispatch(`bots/${FETCH_BOTS}`);
  },

  watch: {
    editedItem() {
      if (
        this.editedItem.name !== "" &&
        this.editedItem.hosts !== "" &&
        this.editedItem.bots !== 0
      ) {
        this.addScan();
      }
    },

    editProject() {
      if (this.editProject.name !== "") {
        this.addProject();
      }
    }
  },

  computed: {
    ...mapGetters({
      projects: "project/projects",
      bots: "bots/name"
    })
  },

  methods: {
    addProject() {
      this.$store.dispatch(`project/${PROJECT_CREATE}`, this.editProject);
    },

    deleteProject(item) {
      if (confirm("Are you sure you want to delete this item?")) {
        const index = this.projects.indexOf(item);
        let id = item.id;
        this.$store.dispatch(`project/${PROJECT_DELETE}`, {
          id: id,
          index: index
        });
      }
    },

    addScan() {
      let id = this.currentProject;
      this.$store
        .dispatch(`scans/${SCAN_CREATE}`, { id: id, scan: this.editedItem })
        .then(() => {
          this.createdScan = true;
        });
    },

    visualizeScan(item) {
      let currentProject = item.id;
      this.$router.push(`/myproject/${currentProject}`);
    },

    editItem(item) {
      this.currentProject = item.id;
      this.index = this.projects.indexOf(item);

      this.dialog = true;
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

.button-add {
  display: flex;
  margin-left: 1.2em;
}

.button-delete {
  display: flex;
  margin-left: 2em;
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

.v-card:not(.v-sheet--tile):not(.v-card--shaped) {
  text-align: center;
}

.title-dialog {
  margin: auto;
}
</style>
