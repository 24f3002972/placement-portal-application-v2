<template>
  <footer class="bg-light border-top mt-auto">
    <div class="container py-3 d-flex flex-column flex-md-row justify-content-between align-items-center">
        <div class="text-muted small mb-2 mb-md-0">{{year}} Placement Portal Application</div>
    </div>
  </footer>
</template>

<script>
export default {
  name: "Footer",
  data() {
    return {
      year: 2026,
    };
  },
};
</script>

<style scoped>
footer {
  font-size: 0.9rem;
}
</style>