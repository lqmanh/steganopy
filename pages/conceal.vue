<template>
  <div class="container">
    <h3 class="title">Data concealing</h3>
    <h5 class="subtitle">Embed data into an image.</h5>
    <section class="section">
      <upload-form
        title="Cover image"
        accept-file="image/jpeg,image/png"
        :file-name="imageFileName"
        @input="changeImageFile"
      />
      <upload-form
        title="Secret data file"
        :file-name="secretFileName"
        @input="changeSecretFile"
      />
      <div class="field">
        <div class="control">
          <button v-if="processing" class="button is-dark is-loading">Processing</button>
          <button v-else-if="processed" class="button is-success">Processed</button>
          <button v-else class="button is-dark" @click="process">Process</button>
        </div>
      </div>
      <div v-if="responseImageUrl" class="field">
        <label class="label">Output</label>
        <a :href="responseImageUrl" target="_blank">
          <img :src="responseImageUrl" alt="Embed-image" />
        </a>
      </div>
    </section>
  </div>
</template>

<script>
import axios from 'axios'
import UploadForm from '../components/upload-form'

export default {
  components: { UploadForm },
  data() {
    return {
      secretFile: null,
      imageFile: null,
      secretFileName: 'No file chosen...',
      imageFileName: 'No image chosen...',
      processing: false,
      processed: false,
      responseImageUrl: ''
    }
  },
  methods: {
    changeSecretFile(event) {
      this.secretFile = event[0]
      this.secretFileName = event[0].name

      this.processed = false
    },
    changeImageFile(event) {
      this.imageFile = event[0]
      this.imageFileName = event[0].name

      this.processed = false
    },
    process() {
      this.processing = true

      const formData = new FormData()
      formData.append('files', this.imageFile)
      formData.append('files', this.secretFile)
      axios
        .post('/api/conceal', formData, {
          headers: { 'content-type': 'multipart/form-data' }
        })
        .then((res) => {
          const { status, data } = res
          if (status !== 200) return
          if (data.url) {
            this.responseImageUrl = data.url
          } else throw new Error(data.error)

          this.processing = false
          this.processed = true
        })
        .catch((err) => {
          console.error(err)

          this.processing = false
        })
    }
  }
}
</script>

<style scoped>
.section {
  padding: 3rem 0;
}
</style>
