<template>
  <div>
    <!-- Hero Section -->
    <div class="bg-primary bg-gradient text-white py-5">
      <div class="container">
        <div class="row align-items-center">
          <div class="col-lg-6">
            <h1 class="display-4 fw-bold mb-3">
                Empowering Careers, Connecting Talent
            </h1>
            <p class="lead mb-4">
                A comprehensive placement management platform for students, companies, and administrators.
            </p>
            <router-link to="/register" class="btn btn-light btn-lg">
              Start Applying
            </router-link>
          </div>
          <div class="col-lg-6 d-none d-lg-block text-center">
            <!-- Replaced image with Bootstrap icon -->
            <i
              class="bi-mortarboard-fill display-1 mb-3"
              style="font-size: 200px"
            ></i>
          </div>
        </div>
      </div>
    </div>

    <!-- Features Section -->
    <div class="container py-5">
        <div class="row">
          <div class="card h-100 border-0 shadow-sm">
            <div class="card-body text-center p-4">
              <div class="display-5 mb-3 text-primary">
                <i class="bi bi-bag-heart"></i>
              </div>
              <h5 class="card-title">Placement Season is Live</h5>
              <p class="card-text text-muted">
                Explore 100+ active job opportunities.<!--explore button will be nice-->
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Categories Section -->
    <div class="bg-light py-5">
      <div class="container">
        <h2 class="text-center mb-4">Popular Drives</h2>
      </div>
  </div>
</template>

<script>
export default {
  name: "HomePage",
  data() {
    return {
    };
  },
};
</script>

<style scoped>
.hover-lift {
  transition: transform 0.2s ease;
}
.hover-lift:hover {
  transform: translateY(-5px);
}
.bg-primary {
  background: linear-gradient(45deg, #0d6efd, #0dcaf0) !important;
}
.bi-basket2-fill {
  opacity: 0.9;
  opacity: 0.9;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.1) 2px 2px 4px rgba(0, 0, 0, 0.1);
}
</style>