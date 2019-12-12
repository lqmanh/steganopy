<template>
  <div class="container">
    <h3 class="title">Data revealing</h3>
    <h5 class="subtitle">Extract secret data from an image.</h5>
    <section class="section">
      <upload-form
        title="Image to extract"
        accept-file="image/png"
        :file-name="imageFileName"
        @input="changeImageFile"
      />
      <div class="field">
        <div class="control">
          <button v-if="processing" class="button is-dark is-loading">Processing</button>
          <button v-else-if="processed" class="button is-success">Processed</button>
          <button v-else class="button is-dark" @click="process">Process</button>
        </div>
      </div>
      <div v-if="responseDataUrl" class="field">
        <label class="label">Output</label>
        <div class="field has-addons">
          <div class="control">
            <input class="input" type="text" :value="responseDataUrl" readonly />
          </div>
          <div class="control">
            <button class="button is-info">
              <span class="file-icon">
                <ion-icon name="cloud-download" />
              </span>
              <span class="file-label">
                <a :href="responseDataUrl" target="_blank">Download</a>
              </span>
            </button>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script>
import axios from 'axios'
import toastr from 'toastr'
import UploadForm from '../components/upload-form'

export default {
  components: { UploadForm },
  data() {
    return {
      imageFile: null,
      imageFileName: 'No image chosen...',
      processing: false,
      processed: false,
      responseDataUrl: ''
    }
  },
  methods: {
    changeImageFile(event) {
      this.imageFile = event[0]
      this.imageFileName = event[0].name

      this.processed = false
    },
    process() {
      this.processing = true

      const formData = new FormData()
      formData.append('files', this.imageFile)
      axios
        .post('/api/reveal', formData, {
          headers: { 'Content-Type': 'multipart/form-data' }
        })
        .then((res) => {
          const { status, data } = res
          if (status !== 200) throw new Error('UNKNOWN_ERROR')
          if (data.url) {
            this.responseDataUrl = data.url
          } else throw new Error(data.error)

          this.processing = false
          this.processed = true
        })
        .catch((err) => {
          toastr.error(err)

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
a {
  color: white;
}
</style>
