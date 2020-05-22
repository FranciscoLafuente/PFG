<template>
  <v-container>
    <v-card :elevation="9">
      <form @keypress.enter="submit">
        <div>
          <h1>
            <em>Reset</em> Password
          </h1>
        </div>

        <v-text-field
          v-model="form.email"
          :error-messages="emailErrors"
          label="E-mail"
          required
          @input="$v.form.email.$touch()"
          @blur="$v.form.email.$touch()"
        ></v-text-field>
        <v-container>
          <v-btn color="blue darken-1" dark class="mr-4" @click="submit">Send email</v-btn>
        </v-container>
      </form>
    </v-card>
  </v-container>
</template>

<script>
import { validationMixin } from "vuelidate";
import { required, email } from "vuelidate/lib/validators";
import { FORGOT_PASS } from "../store/actions.type";

export default {
  mixins: [validationMixin],

  validations: {
    form: {
      email: { required, email }
    }
  },

  data: () => ({
    form: {
      email: "",
      show: false
    }
  }),

  computed: {
    emailErrors() {
      const errors = [];
      if (!this.$v.form.email.$dirty) return errors;
      !this.$v.form.email.email && errors.push("Must be valid e-mail");
      !this.$v.form.email.required && errors.push("E-mail is required");
      return errors;
    }
  },

  methods: {
    submit() {
      console.log(this.form);
      this.$store.dispatch(`${FORGOT_PASS}`, this.form);
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
