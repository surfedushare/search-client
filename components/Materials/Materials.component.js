import { mapGetters } from 'vuex';
import StarRating from './../StarRating';

export default {
  name: 'materials',
  props: {
    materials: {
      default: false
    },
    'items-in-line': {
      type: Number,
      default: 4
    },
    'items-length': {
      type: [Number, String],
      default: 'auto'
    },
    loading: {
      type: Boolean,
      default: false
    },
    contenteditable: {
      type: Boolean,
      default: false
    },
    value: {
      // type: Array,
      // default: []
    }
  },
  components: {
    StarRating
  },
  mounted() {
    this.$store.dispatch('getFilterCategories');
  },
  data() {
    return {
      selected_materials: this.value || []
    };
  },
  methods: {
    setMaterial(material) {
      this.$store.commit('SET_MATERIAL', material);
    },
    selectMaterial(material) {
      let selected_materials = this.value.slice(0);

      if (selected_materials.indexOf(material.external_id) === -1) {
        selected_materials.push(material.external_id);
      } else {
        selected_materials = selected_materials.filter(
          item => item !== material.external_id
        );
      }
      this.$emit('input', selected_materials);
    }
  },
  watch: {
    value(value) {
      this.selected_materials = value;
    }
  },
  computed: {
    ...mapGetters(['disciplines', 'educationallevels', 'materials_loading']),
    current_loading() {
      return this.materials_loading || this.loading;
    },
    /**
     * Extend to the material fields "disciplines" & "educationallevels"
     * @returns {*}
     */
    extended_materials() {
      const {
        materials,
        disciplines,
        educationallevels,
        selected_materials
      } = this;
      let arrMaterials;
      if (materials && disciplines && educationallevels) {
        if (materials.records) {
          arrMaterials = materials.records;
        } else {
          arrMaterials = materials;
        }
        return arrMaterials.map(material => {
          return Object.assign(
            {
              selected: selected_materials.indexOf(material.external_id) !== -1
            },
            material,
            {
              disciplines: material.disciplines.reduce((prev, id) => {
                const item = disciplines.items[id];

                if (item) {
                  prev.push(item);
                }

                return prev;
              }, []),
              educationallevels: material.educationallevels.reduce(
                (prev, id) => {
                  const item = educationallevels.items[id];

                  if (item) {
                    prev.push(item);
                  }

                  return prev;
                },
                []
              )
            }
          );
        });
      }

      return false;
    }
  }
};
