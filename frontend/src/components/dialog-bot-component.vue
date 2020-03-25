<template>
  <v-dialog v-model="dialogBot" persistent max-width="500px">
    <v-card>
      <v-card-title>
        <span class="headline">{{ formTitle }}</span>
      </v-card-title>

      <v-card-text>
        <v-container>
          <v-text-field
            v-model="editedItem.name"
            label="Bot name"
            :error-messages="nameErrors"
            :counter="8"
            @input="$v.editedItem.name.$touch()"
            @blur="$v.editedItem.name.$touch()"
          ></v-text-field>
        </v-container>
        <v-container>
          <v-textarea
            v-model="editedItem.ip"
            label="IPs"
            clearable
            :error-messages="ipErrors"
            @input="$v.editedItem.ip.$touch()"
            @blur="$v.editedItem.ip.$touch()"
          ></v-textarea>
        </v-container>
        <v-container fluid>
          <Select
            :bots="bots"
            @listBots="selectedBots = $event"
            :value="editedItem.type"
            :listBots="(editedItem.type = selectedBots)"
          ></Select>
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
import { helpers } from "vuelidate/lib/validators";
import Select from "../components/select-component";
import constants from "../constants";

const ip_address = helpers.regex("ip_address", constants.VALID_IP_ADDRESS);

export default {
  components: {
    Select
  },
  mixins: [validationMixin],

  validations: {
    editedItem: {
      name: { required, maxLength: maxLength(8) },
      ip: { required, ip_address }
    }
  },
  props: ["dialogBot"],
  data: () => ({
    formTitle: "New Bot",
    bots: constants.BOTS,
    selectedBots: [],
    editedItem: {
      name: "",
      ip: "",
      type: []
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
    },
    ipErrors() {
      const errors = [];
      if (!this.$v.editedItem.ip.$dirty) return errors;
      !this.$v.editedItem.ip.ip_address && errors.push("Must be valid ip");
      !this.$v.editedItem.ip.required && errors.push("Ip is required");
      return errors;
    }
  },

  methods: {
    save() {
      this.$emit("newBot", this.editedItem);
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
</style>