<template>
  <div class="container">
    <h3 class="title">Data detecting</h3>
    <h5 class="subtitle">Check if an image contains any secret data.</h5>
    <section class="section">
      <upload-form
        title="Image to check"
        acceptFile="image/png"
        :fileName="imageFileName"
        @input="changeImageFile"
      />
      <div class="field">
        <div class="control">
          <button v-if="checking" class="button is-dark is-loading">Checking</button>
          <button v-else-if="checked" class="button is-success">Checked</button>
          <button v-else class="button is-dark" @click="check">Check</button>
        </div>
      </div>
      <div v-if="checked && hasSecretData" class="field has-text-success">
        <span class="icon">
          <ion-icon name="checkmark"></ion-icon>
        </span>
        <span>This image MAY have secret data inside!</span>
      </div>
      <div v-else-if="checked" class="field has-text-danger">
        <span class="icon">
          <ion-icon name="close"></ion-icon>
        </span>
        <span>This image does not have secret data inside!</span>
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
      imageFile: null,
      imageFileName: 'No image chosen...',
      checking: false,
      checked: false,
      hasSecretData: false
    }
  },
  methods: {
    changeImageFile(event) {
      this.imageFile = event[0]
      this.imageFileName = event[0].name

      this.checked = false
    },
    check() {
      this.checking = true

      const formData = new FormData()
      formData.append('files', this.imageFile)
      axios
        .post('/api/detect', formData, {
          headers: { 'content-type': 'multipart/form-data' }
        })
        .then((res) => {
          const { status, data } = res
          if (status !== 200) return
          if (data.result !== undefined) {
            this.hasSecretData = data.result
          } else throw new Error(data.error)

          this.checking = false
          this.checked = true
        })
        .catch((err) => {
          console.error(err)

          this.checking = false
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
