<template>

<nav class="navbar navbar-expand-lg navbar-light bg-white shadow-sm">

    <div class="container">

        <router-link
            class="navbar-brand fw-bold"
            to="/"
        >
            Placement Portal
        </router-link>

        <button
            class="navbar-toggler"
            type="button"
            data-bs-toggle="collapse"
            data-bs-target="#mainNav"
            aria-controls="mainNav"
            aria-expanded="false"
            aria-label="Toggle navigation"
        >

            <span class="navbar-toggler-icon"></span>

        </button>

        <div
            class="collapse navbar-collapse"
            id="mainNav"
        >

            <ul class="navbar-nav ms-auto">

                <li class="nav-item">

                    <router-link
                        class="nav-link"
                        to="/"
                    >
                        Home
                    </router-link>

                </li>

            </ul>

        </div>

    </div>

</nav>

</template>

<script>

export default {

    name: "Navbar"

}

</script>

<style scoped>

.navbar-brand{

    letter-spacing:0.3px;

}

</style>