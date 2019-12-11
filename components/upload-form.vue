<template>
  <div class="field">
    <label class="label">{{ title }}</label>
    <div class="control file has-name is-fullwidth">
      <label class="file-label">
        <input
          class="file-input"
          type="file"
          :accept="acceptFile"
          @input="$emit('input', $event.target.files)"
        />
        <span class="file-cta">
          <span class="file-icon">
            <ion-icon name="cloud-upload" />
          </span>
          <span class="file-label">Choose a file...</span>
        </span>
        <span class="file-name">{{ fileName }}</span>
      </label>
    </div>
  </div>
</template>

<script>
export default {
  props: ['title', 'acceptFile', 'fileName', 'value']
}
</script>
