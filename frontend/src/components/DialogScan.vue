<template>
  <v-dialog v-model="dialog" persistent max-width="500px">
    <v-card>
      <v-card-title>
        <span class="headline">{{ formTitle }}</span>
      </v-card-title>

      <v-card-text>
        <v-container>
          <v-text-field
            v-model="editedItem.name"
            label="Scan name"
            :error-messages="nameErrors"
            @input="$v.editedItem.name.$touch()"
            @blur="$v.editedItem.name.$touch()"
          ></v-text-field>
        </v-container>
        <v-container>
          <v-textarea
            v-model="hosts"
            :error-messages="hostsErrors"
            label="Hosts"
            clearable
            @input="$v.hosts.$touch()"
            @blur="$v.hosts.$touch()"
          ></v-textarea>
        </v-container>
        <v-container>
          <v-select
            v-model="editedItem.bot"
            :items="bots"
            label="Bots"
          ></v-select>
        </v-container>
        <v-container fluid>
          <v-checkbox v-model="checkbox" label="Schedule"></v-checkbox>
        </v-container>
        <v-container v-if="checkbox">
          <v-row>
            <v-col>
              <v-menu
                v-model="menu2"
                :close-on-content-click="false"
                :nudge-right="40"
                transition="scale-transition"
                offset-y
                min-width="290px"
              >
                <template v-slot:activator="{ on }">
                  <v-text-field
                    v-model="date"
                    label="Picker without buttons"
                    prepend-icon="event"
                    readonly
                    v-on="on"
                  ></v-text-field>
                </template>
                <v-date-picker
                  v-model="date"
                  @input="menu2 = false"
                ></v-date-picker>
              </v-menu>
            </v-col>
            <v-col>
              <v-menu
                ref="menu"
                v-model="menu"
                :close-on-content-click="false"
                :nudge-right="40"
                :return-value.sync="time"
                transition="scale-transition"
                offset-y
                max-width="290px"
                min-width="290px"
              >
                <template v-slot:activator="{ on }">
                  <v-text-field
                    v-model="time"
                    label="Picker in menu"
                    prepend-icon="access_time"
                    readonly
                    v-on="on"
                  ></v-text-field>
                </template>
                <v-time-picker
                  v-if="menu"
                  v-model="time"
                  full-width
                  @click:minute="$refs.menu.save(time)"
                ></v-time-picker>
              </v-menu>
            </v-col>
          </v-row>
        </v-container>
      </v-card-text>

      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn color="blue darken-1" text @click="$emit('isShow', false)"
          >Cancel</v-btn
        >
        <v-btn color="blue darken-1" text @click="save">Save</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
import { validationMixin } from "vuelidate";
import { required } from "vuelidate/lib/validators";
import { helpers } from "vuelidate/lib/validators";
import constants from "../common/constants";

const ip_address = helpers.regex("ip_address", constants.VALID_HOST_NAME);

export default {
  components: {
    //Select
  },
  mixins: [validationMixin],

  validations: {
    editedItem: {
      name: { required }
    },
    hosts: { required, ip_address }
  },
  props: ["dialog", "bots"],
  data: () => ({
    selectedValue: null,
    formTitle: "New Scan",
    newItem: {},
    editedIndex: -1,
    editedItem: {
      name: "",
      bot: "",
      executiontime: "",
      hosts: []
    },
    hosts: "",
    selectedBots: [],
    date: new Date().toISOString().substr(0, 10),
    menu2: false,
    time: "",
    menu: false,
    checkbox: false
  }),
  computed: {
    nameErrors() {
      const errors = [];
      if (!this.$v.editedItem.name.$dirty) return errors;
      !this.$v.editedItem.name.required && errors.push("Name is required.");
      return errors;
    },
    hostsErrors() {
      const errors = [];
      if (!this.$v.hosts.$dirty) return errors;
      !this.$v.hosts.ip_address && errors.push("Must be valid host");
      !this.$v.hosts.required && errors.push("At least one host is required");
      return errors;
    }
  },

  methods: {
    save() {
      if (this.date !== "" && this.time !== "") {
        console.log("No ha detecta execution time");
        // If Scheduled
        this.editedItem.executiontime = this.date + " " + this.time;
      }
      this.editedItem.hosts = this.hosts.split(",");
      console.log(this.editedItem);
      this.$emit("newScan", this.editedItem);
      this.$emit("isShow", false);
      this.editedItem = {
        name: "",
        bot: "",
        executiontime: "",
        hosts: []
      };
    },

    dateNow() {
      let time = new Date().toLocaleTimeString();
      let date = new Date().toISOString().substr(0, 10);
      return date + " " + time;
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
  padding: 0%;
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
