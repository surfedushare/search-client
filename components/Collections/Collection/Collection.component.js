import BreadCrumbs from '~/components/BreadCrumbs';
import DirectSearch from '~/components/FilterCategories/DirectSearch';
import ShareMaterialCollection from '~/components/Popup/ShareMaterialCollection';
import ShareCollection from '~/components/Popup/ShareCollection';

export default {
  name: 'collection',
  props: {
    collection: {
      default: false
    },
    contenteditable: {
      default: false
    },
    setEditable: {
      default: false
    },
    submitting: {
      default: false
    },
    changeViewType: {
      default: false
    },
    'items-in-line': {
      default: 4
    }
  },
  components: {
    BreadCrumbs,
    DirectSearch,
    ShareMaterialCollection,
    ShareCollection
  },
  mounted() {
    const { collection } = this;
    if (collection) {
      this.setTitle(collection.title);
      this.setSocialCounters();
    }
    this.href = window.location.href;
  },
  data() {
    return {
      href: '',
      collection_title: null,
      search: {},
      isShowShareMaterial: false,
      isShowShareCollection: false,
      is_copied: false
    };
  },
  methods: {
    setTitle(title) {
      if (title) {
        this.collection_title = title;
        // if (this.$refs.title) {
        //   this.$refs.title.innerText = title;
        // }
      }
    },
    onChangeTitle() {
      if (this.$refs.title) {
        this.setTitle(this.$refs.title.innerText);
      }
    },
    resetData() {
      this.setTitle(this.collection.title);
    },
    deleteCollection(id) {
      this.$store.dispatch('deleteMyCollection', id).then(() => {
        this.$router.push('/my/collections/');
      });
    },
    showShareMaterial() {
      this.isShowShareMaterial = true;
    },

    closeShareMaterial() {
      this.isShowShareMaterial = false;
      if (this.is_copied) {
        this.closeSocialSharing('link');
      }
    },

    onSubmit() {
      this.$emit('onSubmit', { title: this.collection_title });
    },

    setSocialCounters() {
      this.$nextTick().then(() => {
        const { collection } = this;
        const { social_counters } = this.$refs;

        if (collection && collection.sharing_counters && social_counters) {
          const share = collection.sharing_counters.reduce(
            (prev, next) => {
              prev[next.sharing_type] = next;
              return prev;
            },
            {
              linkedin: {
                counter_value: 0
              },
              twitter: {
                counter_value: 0
              },
              link: {
                counter_value: 0
              }
            }
          );

          if (share.linkedin) {
            social_counters.querySelector('#linkedin_counter').innerText =
              share.linkedin.counter_value;
          }
          if (share.twitter) {
            social_counters.querySelector('#twitter_counter').innerText =
              share.twitter.counter_value;
          }
          if (share.link) {
            social_counters.querySelector('#url_counter').innerText =
              share.link.counter_value;
          }
        }
      });
    },
    closeSocialSharing(type) {
      this.$store
        .dispatch('setCollectionSocial', {
          id: this.$route.params.id,
          params: {
            shared: type
          }
        })
        .then(() => {
          this.setSocialCounters();
        });
    },

    showShareCollection() {
      this.isShowShareCollection = true;
    },

    closeShareCollection() {
      this.isShowShareCollection = false;
      if (this.is_copied) {
        this.closeSocialSharing('link');
      }
    }
  },
  computed: {},
  watch: {
    search(search) {
      this.$emit('input', search);
    },
    contenteditable(isEditable) {
      const { title } = this.$refs;
      this.$nextTick().then(() => {
        title.focus();
      });
      if (!isEditable) {
        this.resetData();
      }
    },
    collection(collection) {
      if (collection) {
        this.setTitle(collection.title);
        this.setSocialCounters();
      }
    }
  }
};
