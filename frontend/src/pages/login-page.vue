<template>
  <v-container>
    <v-card :elevation="9" class="form-card">
      <form @keypress.enter="login" class="form-data">
        <div>
          <h1>
            Login with
            <em>Shodita</em>
          </h1>
        </div>

        <v-text-field
          v-model="email"
          :error-messages="emailErrors"
          label="E-mail"
          required
          @input="$v.email.$touch()"
          @blur="$v.email.$touch()"
        ></v-text-field>

        <v-text-field
          v-model="password"
          :error-messages="passwordErrors"
          :type="show ? 'text' : 'password'"
          :append-icon="show ? 'mdi-eye' : 'mdi-eye-off'"
          label="Password"
          required
          @input="$v.password.$touch()"
          @blur="$v.password.$touch()"
          @click:append="show = !show"
        ></v-text-field>

        <v-btn color="blue darken-1" dark class="mr-4" @click="login">login</v-btn>
        <div>
          <router-link :to="{ path: 'forgot' }">Forgot Password?</router-link>
        </div>
      </form>
    </v-card>
    <v-dialog v-model="dialog" persistent max-width="195px">
      <v-card>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="green darken-1" text @click="dialog = false">
            <v-icon>clear</v-icon>
          </v-btn>
        </v-card-actions>
        <v-icon class="icon-error">lock</v-icon>
        <v-card-title class="headline">
          <span class="title-dialog">No Access!</span>
        </v-card-title>
        <v-card-text>Wrong email or password</v-card-text>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<script>
import { validationMixin } from "vuelidate";
import { required, email, minLength } from "vuelidate/lib/validators";

export default {
  mixins: [validationMixin],

  validations: {
    email: { required, email },
    password: { required, minLength: minLength(8) }
  },

  data: () => ({
    email: "",
    password: "",
    show: false,

    form: {},
    dialog: false
  }),

  computed: {
    emailErrors() {
      const errors = [];
      if (!this.$v.email.$dirty) return errors;
      !this.$v.email.email && errors.push("Must be valid e-mail");
      !this.$v.email.required && errors.push("E-mail is required");
      return errors;
    },
    passwordErrors() {
      const errors = [];
      if (!this.$v.password.$dirty) return errors;
      !this.$v.password.minLength &&
        errors.push("Password must be at least 8 characters long");
      !this.$v.password.required && errors.push("Password is required");
      return errors;
    }
  },

  methods: {
    login: function() {
      let email = this.email;
      let password = this.password;
      this.$store
        .dispatch("login", { email, password })
        .then(() => this.$router.push("/"))
        .catch(() => {
          this.dialog = true;
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
</style>
