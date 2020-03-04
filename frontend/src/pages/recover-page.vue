<template>
  <v-container>
    <v-card :elevation=9>
      <form>
        <div>
          <h1><em>Reset</em> Password</h1>
        </div>

        <v-text-field
          v-model="form.email"
          :error-messages="emailErrors"
          label="E-mail"
          required
          @input="$v.email.$touch()"
          @blur="$v.email.$touch()"
        ></v-text-field>

        <v-btn color="blue darken-1" dark class="mr-4" @click="submit">reset password</v-btn>

      </form>
    </v-card>
  </v-container>
</template>

<script>
  import { validationMixin } from 'vuelidate'
  import { required, email } from 'vuelidate/lib/validators'
  import axios from "axios";


  export default {
      mixins: [validationMixin],

    validations: {
      email: { required, email },
    },

    data: () => ({
        form: {
            email: '',
            show: false,
        }
    }),

    computed: {
      emailErrors () {
        const errors = []
        if (!this.$v.email.$dirty) return errors
        !this.$v.email.email && errors.push('Must be valid e-mail')
        !this.$v.email.required && errors.push('E-mail is required')
        return errors
      },
    },

    methods: {
      submit (evt) {
        evt.preventDefault();
        console.log(this.form);
        
        axios.get("http://localhost:5000/login", this.form).then(r => {
            console.log(r);
        });
      },
    },
  }
</script>

<style scoped>
.container {
    width: 100%;
    height:88%;
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