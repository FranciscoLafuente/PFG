<template>
  <v-container>
    <v-card :elevation="9">
      <form>
        <div>
          <h1><em>Create</em> New Account</h1>
        </div>

        <v-text-field
          v-model="name"
          :error-messages="nameErrors"
          :counter="10"
          label="Name"
          required
          @input="$v.name.$touch()"
          @blur="$v.name.$touch()"
        ></v-text-field>

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

        <v-btn color="blue darken-1" dark class="mr-4" @click="register"
          >create</v-btn
        >
      </form>
    </v-card>
  </v-container>
</template>

<script>
import { validationMixin } from "vuelidate";
import {
  required,
  maxLength,
  minLength,
  email
} from "vuelidate/lib/validators";

export default {
  mixins: [validationMixin],

  validations: {
    name: { required, maxLength: maxLength(10) },
    email: { required, email },
    password: { required, minLength: minLength(8) }
  },

  data: () => ({
    name: "",
    email: "",
    password: "",
    show: false,

    form: {}
  }),

  computed: {
    nameErrors() {
      const errors = [];
      if (!this.$v.name.$dirty) return errors;
      !this.$v.name.maxLength &&
        errors.push("Name must be at most 10 characters long");
      !this.$v.name.required && errors.push("Name is required.");
      return errors;
    },
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
    register: function() {
      let data = {
        name: this.name,
        email: this.email,
        password: this.password,
        is_admin: this.is_admin
      };
      this.$store
        .dispatch("register", data)
        .then(() => this.$router.push("/"))
        .catch(err => console.log(err));
    },

    clear() {
      this.$v.$reset();
      this.name = "";
      this.email = "";
      this.password = "";
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

.v-card {
  width: 40%;
  padding: inherit;
  margin: auto;
  display: flex;
  justify-content: center;
  text-align: center;
}
.v-card > *:last-child:not(.v-btn):not(.v-chip) {
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
</style>
