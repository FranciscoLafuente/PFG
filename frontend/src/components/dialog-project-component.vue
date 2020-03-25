<template>
  <v-dialog v-model="dialogPro" persistent max-width="500px">
    <v-card>
      <v-card-title>
        <span class="headline">{{ formTitle }}</span>
      </v-card-title>

      <v-card-text>
        <v-container>
          <v-text-field
            v-model="editedItem.name"
            label="Project name"
            :error-messages="nameErrors"
            :counter="8"
            @input="$v.editedItem.name.$touch()"
            @blur="$v.editedItem.name.$touch()"
          ></v-text-field>
        </v-container>
        <v-container fluid>
          <v-select :items="items" v-model="editedItem.type" label="Type" clearable></v-select>
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
import { validationMixin } from "vuelidate";
import { required, maxLength } from "vuelidate/lib/validators";

export default {
  mixins: [validationMixin],

  validations: {
    editedItem: {
      name: { required, maxLength: maxLength(8) }
    }
  },
  props: ["dialogPro"],
  data: () => ({
    formTitle: "New Project",
    items: ["Public", "Private"],
    editedItem: {
      name: "",
      type: true,
      scans: []
    }
  }),
  computed: {
    nameErrors() {
      const errors = [];
      if (!this.$v.editedItem.name.$dirty) return errors;
      !this.$v.editedItem.name.maxLength &&
        errors.push("Name must be at most 8 characters long");
      !this.$v.editedItem.name.required && errors.push("Name is required.");
      return errors;
    }
  },

  methods: {
    save() {
      this.$emit("newProject", this.editedItem);
      this.$emit("isShow", false);
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
  padding: initial;
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

.container > .col {
  padding: none;
}
</style>