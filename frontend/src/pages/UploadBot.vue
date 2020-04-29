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
          prepend-icon="email"
          required
          @input="$v.email.$touch()"
          @blur="$v.email.$touch()"
        ></v-text-field>

        <v-file-input
          :rules="rules"
          multiple
          accept=".py"
          placeholder="Pick an field"
          prepend-icon="adb"
          label="Bot"
        ></v-file-input>

        <v-btn color="blue darken-1" dark class="mr-4" @click="login">login</v-btn>
        <div>
          <router-link :to="{ path: 'forgot' }">Forgot Password?</router-link>
        </div>
      </form>
    </v-card>
  </v-container>
</template>


<script>
export default {
  data: () => ({
    rules: [
      value =>
        !value || value.size < 2000000 || "File size should be less than 2 MB!"
    ]
  })
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