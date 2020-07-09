import { mapGetters } from 'vuex'
import { VueAutosuggest } from 'vue-autosuggest'
import { debounce } from 'lodash'

import axios from '~/axios'

export default {
  name: 'search',
  components: {
    VueAutosuggest
  },
  props: {
    selectOptions: {
      type: Object,
      default: function() {
        return {
          name: '',
          options: []
        }
      }
    },
    checkboxOptions: {
      type: Object,
      default: function() {
        return {
          name: '',
          options: []
        }
      }
    },
    placeholder: {
      type: String,
      default: function() {
        return this.$t('Search-by-keywords')
      }
    },
    value: {
      type: String
    }
  },
  data() {
    return {
      searchText: this.value,
      suggestions: []
    }
  },
  methods: {
    onInputChange(query) {
      this.searchSuggestions(query, this)
      this.$emit('input', query)
    },
    searchSuggestions: debounce(async function(search) {
      if (!search) {
        this.suggestions = []
        return
      }

      const { data } = await axios.get('keywords/', {
        params: { query: search }
      })

      this.suggestions = [{ data }]
    }, 350),
    onSelectSuggestion(result) {
      this.$emit('input', result.item)
      this.$emit('onSearch')
    },
    onSubmit() {
      if (!this.searchText) {
        return
      }

      this.$emit('onSearch')
    },
    changeSelectedOption($event) {
      this.$emit('selectDropdownOption', $event.target.value)
    },
    changeCheckboxOption($event) {
      this.$emit('selectCheckboxOption', {
        value: $event.target.value,
        checked: $event.target.checked
      })
    }
  },
  watch: {
    value(value) {
      this.searchText = value
    }
  },
  computed: {
    ...mapGetters({
      keywords: 'materials_keywords'
    }),
    autosuggestInputProps: function() {
      return {
        placeholder: this.placeholder,
        id: 'autosuggest__input',
        type: 'search',
        class: {
          'with-dropdown': this.suggestions.length > 0
        }
      }
    },
    autosuggestClasses: function() {
      return {
        'with-dropdown': this.suggestions.length > 0
      }
    }
  }
}
