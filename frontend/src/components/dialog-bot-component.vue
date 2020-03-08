<template>
    <v-dialog v-model="dialogBot" max-width="500px">
        <v-card>
            <v-card-title>
                <span class="headline">{{ formTitle }}</span>
            </v-card-title>

            <v-card-text>
                <v-container>
                  <v-row>
                    <v-col>
                      <v-text-field v-model="editedItem.name" label="Bot name"></v-text-field>
                    </v-col>
                  </v-row>
                </v-container>
                <v-container>
                  <v-row>
                    <v-col>
                      <v-textarea v-model="editedItem.ip" label="IPs" clearable=""></v-textarea>
                    </v-col>
                  </v-row>
                </v-container>
                <v-container fluid>
                  <v-row>
                    <v-col>
                      <v-select :items="items" v-model="editedItem.type" label="Type" clearable=""></v-select>
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
  props: ["dialogBot"],
  data: () => ({
    formTitle: "New Bot",
    items: ['Nobita', 'Shuneo'],
    editedItem: {
      name: "",
      ip: "",
      type: [],
    },
  }),

  methods: {
      save() {
        this.$emit('newBot', this.editedItem)
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