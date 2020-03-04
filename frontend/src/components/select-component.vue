<template>
    <v-select v-model="selectedBots" :items="bots" label="Select Bots" multiple>
      <template v-slot:prepend-item>
        <v-list-item ripple @click="toggle">
          <v-list-item-action>
            <v-icon :color="selectedBots.length > 0 ? 'indigo darken-4' : ''">{{ icon }}</v-icon>
          </v-list-item-action>
          <v-list-item-content>
            <v-list-item-title>Select All</v-list-item-title>
          </v-list-item-content>
        </v-list-item>
        <v-divider class="mt-2"></v-divider>
      </template>
    </v-select>
</template>

<script>
  export default {
    props: ["bots"],
    data: () => ({
      selectedBots: [],
    }),

    computed: {
      allBots () {
        return this.selectedBots.length === this.bots.length
      },
      someBot () {
        return this.selectedBots.length > 0 && !this.allBots
      },
      icon () {
        if (this.allBots) return 'mdi-close-box'
        if (this.someBot) return 'mdi-minus-box'
        return 'mdi-checkbox-blank-outline'
      },
    },
    updated() {
      this.$emit('listBots', this.selectedBots)
    },

    methods: {
      toggle () {
        this.$nextTick(() => {
          if (this.allBots) {
            this.selectedBots = []
          } else {
            this.selectedBots = this.bots.slice()
          }
        })
      }
    }
  }
</script>