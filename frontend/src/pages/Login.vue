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

        <v-btn color="blue darken-1" dark class="mr-4" @click="login"
          >login</v-btn
        >
        <div>
          <router-link :to="{ path: 'forgot' }">Forgot Password?</router-link>
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
import { validationMixin } from "vuelidate";
import { required, email, minLength } from "vuelidate/lib/validators";
import { LOGIN } from "../store/actions.type";
import dialogMessage from "../components/DialogMessage";
import { ACCESS_TITLE, ACCESS_ICON, ACCESS_TEXT } from "../common/dialogMsg";

export default {
  components: { dialogMessage },
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
    dialogMsg: false,
    msg_title: ACCESS_TITLE,
    msg_icon: ACCESS_ICON,
    msg_text: ACCESS_TEXT
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
        .dispatch(LOGIN, { email, password })
        .then(() => this.$router.push({ name: "home" }))
        .catch(() => {
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
</style>
