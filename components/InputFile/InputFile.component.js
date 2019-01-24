export default {
  name: 'input-file',
  mounted() {},
  props: {
    imagesrc: {
      default: false
    },
    title: {
      default: ''
    },
    refinput: {
      default: 'file'
    }
  },
  data() {
    return {
      max_size: 1024, // 1 mb
      image: null,
      imageText: null,
      imageLink: null,
      accept: 'image/jpeg,image/gif,image/png'
    };
  },
  watch: {},
  methods: {
    /**
     * Watcher on changing the file
     * @param e - Event
     */
    onFileChange(e) {
      if (!this.errors.has('file')) {
        let files = e.target.files || e.dataTransfer.files;
        if (!files.length) return;
        this.createImage(files[0]);
        this.imageText = files[0].name;
      }
    },
    /**
     * Create image
     * @param file
     */
    createImage(file) {
      if (!this.errors.has('file')) {
        let reader = new FileReader();
        let that = this;

        reader.onload = e => {
          that.image = e.target.result;
        };
        reader.readAsDataURL(file);
      }
    },
    /**
     * Remove image
     * @param e - event
     */
    removeImage: function(e) {
      this.image = '';
      this.imageText = '';
      this.imageLink = '';
      this.$refs.file.value = null;
      this.errors.clear();
    }
  },
  computed: {
    /**
     * Get image path
     * @returns String
     */
    imagePath() {
      this.imageLink = this.image;
      return this.imageLink !== null ? this.imageLink : this.imagesrc;
    },
    /**
     * Get image name
     * @returns String
     */
    imagePathTxt() {
      return this.imageText !== null ? this.imageText : this.imagesrc;
    }
  }
};
