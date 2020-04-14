<template>
  <v-container>
    <v-card :elevation="9">
      <form @keypress.enter="submit">
        <div>
          <h1><em>Reset</em> Password</h1>
        </div>

        <v-text-field
          v-model="form.password"
          :error-messages="passwordErrors"
          label="New password"
          :type="form.show ? 'text' : 'password'"
          :append-icon="form.show ? 'mdi-eye' : 'mdi-eye-off'"
          required
          @input="$v.form.password.$touch()"
          @blur="$v.form.password.$touch()"
          @click:append="form.show = !form.show"
        ></v-text-field>
        <v-container>
          <v-btn color="blue darken-1" dark class="mr-4" @click="submit"
            >reset password</v-btn
          >
        </v-container>
      </form>
    </v-card>
  </v-container>
</template>

<script>
import { validationMixin } from "vuelidate";
import { required, minLength } from "vuelidate/lib/validators";
import axios from "axios";

export default {
  mixins: [validationMixin],

  validations: {
    form: {
      password: { required, minLength: minLength(8) }
    }
  },

  data: () => ({
    form: {
      password: "",
      show: false
    }
  }),

  computed: {
    passwordErrors() {
      const errors = [];
      if (!this.$v.form.password.$dirty) return errors;
      !this.$v.form.password.minLength &&
        errors.push("Password must be at least 8 characters long");
      !this.$v.form.password.required && errors.push("Password is required");
      return errors;
    }
  },

  methods: {
    submit() {
      let token = this.getToken(this.$route.params.reset_token.toString());
      console.log(token);

      let data = {
        reset_token: this.$route.params.reset_token.toString(),
        password: "nuevapass"
      };

      axios
        .post("http://localhost:5000/" + "/reset", data, token)
        .catch(error => {
          console.log(error);
        });
    },

    getToken(reset_token) {
      let token = {
        headers: {
          Authorization: "Bearer " + reset_token
        }
      };
      return token;
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
