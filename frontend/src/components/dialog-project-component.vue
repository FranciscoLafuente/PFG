<template>
    <v-dialog v-model="dialogPro" max-width="500px">
        <v-card>
            <v-card-title>
                <span class="headline">{{ formTitle }}</span>
            </v-card-title>

            <v-card-text>
                <v-container>
                  <v-row>
                    <v-col>
                      <v-text-field v-model="editedItem.name" label="Project name"></v-text-field>
                    </v-col>
                  </v-row>
                </v-container>
                <v-container>
                  <v-row>
                    <v-col>
                      <v-text-field v-model="editedItem.hosts" label="Type" clearable=""></v-text-field>
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
export default {
  props: ["dialogPro"],
  data: () => ({
    formTitle: "New Project",
    newItem: {},
    editedIndex: -1,
    editedItem: {
      name: "",
      bots: 0,
      executiontime: 0,
      hosts: ""
    },
  }),

  methods: {
      save() {
        this.$emit('newScan', this.editedItem)
        this.$emit('isShow', false)
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