<template>
  <div class="container py-4">

    <div class="d-flex justify-content-between align-items-center mb-4">
      <h2 class="fw-bold">Welcome Admin</h2>
    </div>

    <!-- Search -->
    <div class="row mb-4">
      <div class="col-md-6">
        <div class="input-group">
          <input
            v-model="search"
            class="form-control"
            placeholder="Search companies, students, drives..."
          >
          <button
            class="btn btn-outline-secondary"
            type="button"
            @click="search = ''"
          >
            Clear
          </button>
        </div>
      </div>
    </div>

    <!-- Loading -->
    <div v-if="loading" class="text-center py-5">
      <div class="spinner-border text-primary"></div>
    </div>

    <div v-else>

      <!-- Dashboard Cards -->
      <div class="row g-3 mb-4">
        <div class="col-md-3">
          <div class="card shadow-sm">
            <div class="card-body text-center">
              <h3>{{ companies.length }}</h3>
              <p class="mb-0">Companies</p>
            </div>
          </div>
        </div>
        <div class="col-md-3">
          <div class="card shadow-sm">
            <div class="card-body text-center">
              <h3>{{ students.length }}</h3>
              <p class="mb-0">Students</p>
            </div>
          </div>
        </div>
        <div class="col-md-3">
          <div class="card shadow-sm">
            <div class="card-body text-center">
              <h3>{{ ongoingDrives.length }}</h3>
              <p class="mb-0">Ongoing Drives</p>
            </div>
          </div>
        </div>
        <div class="col-md-3">
          <div class="card shadow-sm">
            <div class="card-body text-center">
              <h3>{{ applications.length }}</h3>
              <p class="mb-0">Applications</p>
            </div>
          </div>
        </div>
      </div>

      <!-- Registered Companies -->
      <div class="card shadow-sm mb-4">
        <div class="card-header fw-bold">Registered Companies</div>
        <div class="card-body p-0">
          <table class="table table-bordered table-hover mb-0">
            <thead class="table-light">
              <tr>
                <th>Company</th>
                <th>Status</th>
                <th width="150">Action</th>
              </tr>
            </thead>
            <tbody>
              <tr v-if="filteredCompanies.length === 0">
                <td colspan="3">No companies found.</td>
              </tr>
              <tr
                v-for="company in filteredCompanies"
                :key="company.id"
              >
                <td>{{ company.company_name }}</td>
                <td>
                  <span
                    class="badge"
                    :class="company.active ? 'bg-success' : 'bg-danger'"
                  >
                    {{ company.active ? "Active" : "Blacklisted" }}
                  </span>
                </td>
                <td>
                  <button
                    v-if="company.active"
                    class="btn btn-danger btn-sm"
                    @click="blacklist(company.user_id)"
                  >
                    Blacklist
                  </button>
                  <button
                    v-else
                    class="btn btn-success btn-sm"
                    @click="unblacklist(company.user_id)"
                  >
                    Activate
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- Registered Students -->
      <div class="card shadow-sm mb-4">
        <div class="card-header fw-bold">Registered Students</div>
        <div class="card-body p-0">
          <table class="table table-bordered table-hover mb-0">
            <thead class="table-light">
              <tr>
                <th>Name</th>
                <th>Branch</th>
                <th>CGPA</th>
                <th>Year</th>
                <th width="150">Action</th>
              </tr>
            </thead>
            <tbody>
              <tr v-if="filteredStudents.length === 0">
                <td colspan="5">No students found.</td>
              </tr>
              <tr
                v-for="student in filteredStudents"
                :key="student.id"
              >
                <td>{{ student.user?.name }}</td>
                <td>{{ student.branch }}</td>
                <td>{{ student.cgpa }}</td>
                <td>{{ student.year }}</td>
                <td>
                  <button
                    v-if="student.user?.active"
                    class="btn btn-danger btn-sm"
                    @click="blacklist(student.user.id)"
                  >
                    Blacklist
                  </button>
                  <button
                    v-else
                    class="btn btn-success btn-sm"
                    @click="unblacklist(student.user?.id)"
                  >
                    Activate
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- Company Requests -->
      <div class="card shadow-sm mb-4">
        <div class="card-header fw-bold">Company Registration Requests</div>
        <div class="card-body p-0">
          <table class="table table-bordered table-hover mb-0">
            <thead class="table-light">
              <tr>
                <th>Company</th>
                <th>Status</th>
                <th width="220">Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr v-if="filteredCompanyRequests.length === 0">
                <td colspan="3">No pending requests.</td>
              </tr>
              <tr
                v-for="request in filteredCompanyRequests"
                :key="request.id"
              >
                <td>{{ request.data?.company_name }}</td>
                <td>{{ request.status }}</td>
                <td>
                  <button
                    class="btn btn-success btn-sm me-2"
                    @click="approveRequest(request.id)"
                  >
                    Approve
                  </button>
                  <button
                    class="btn btn-danger btn-sm"
                    @click="rejectRequest(request.id)"
                  >
                    Reject
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- Ongoing Drives -->
      <div class="card shadow-sm mb-4">
        <div class="card-header fw-bold">Ongoing Drives</div>
        <div class="card-body p-0">
          <table class="table table-bordered table-hover mb-0">
            <thead class="table-light">
              <tr>
                <th width="80">Sr No</th>
                <th>Company</th>
                <th>Drive</th>
                <th>Deadline</th>
                <th>Status</th>
                <th width="200">Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr v-if="ongoingDrives.length === 0">
                <td colspan="6">No ongoing drives.</td>
              </tr>
              <tr
                v-for="(drive, index) in ongoingDrives"
                :key="drive.id"
              >
                <td>{{ index + 1 }}</td>
                <td>{{ drive.company_name }}</td>
                <td>{{ drive.job_title }}</td>
                <td>{{ formatDate(drive.deadline) }}</td>
                <td>
                  <span class="badge bg-primary">{{ drive.status }}</span>
                </td>
                <td>
                  <button
                    class="btn btn-primary btn-sm me-2"
                    @click="$router.push('/drive/' + drive.id)"
                  >
                    View
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- Student Applications -->
      <div class="card shadow-sm mb-4">
        <div class="card-header fw-bold">Student Applications</div>
        <div class="card-body p-0">
          <table class="table table-bordered table-hover mb-0">
            <thead class="table-light">
              <tr>
                <th width="80">Sr No</th>
                <th>Student</th>
                <th>Company</th>
                <th>Drive</th>
                <th>Status</th>
                <th width="140">Action</th>
              </tr>
            </thead>
            <tbody>
              <tr v-if="filteredApplications.length === 0">
                <td colspan="6">No applications found.</td>
              </tr>
              <tr
                v-for="(application, index) in filteredApplications"
                :key="application.id"
              >
                <td>{{ index + 1 }}</td>
                <td>{{ application.student?.user?.name }}</td>
                <td>{{ application.drive?.company_name }}</td>
                <td>{{ application.drive?.job_title }}</td>
                <td>
                  <span
                    class="badge"
                    :class="{
                      'bg-warning': application.status === 'Applied',
                      'bg-info': application.status === 'Shortlisted',
                      'bg-success': application.status === 'Selected',
                      'bg-danger': application.status === 'Rejected'
                    }"
                  >
                    {{ application.status }}
                  </span>
                </td>
                <td>
                  <button
                    class="btn btn-outline-primary btn-sm"
                    @click="$router.push('/application/' + application.id)"
                  >
                    View
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

    </div>
  </div>
</template>

<script>
import api from "@/utils/api";

export default {
  name: "AdminDashboard",

  data() {
    return {
      companies: [],
      students: [],
      companyRequests: [],
      drives: [],
      applications: [],
      search: "",
      loading: false,
      error: ""
    };
  },

  computed: {
    filteredCompanies() {
      const q = this.search.toLowerCase();
      return this.companies.filter(company =>
        (company.company_name || "").toLowerCase().includes(q)
      );
    },

    filteredStudents() {
      const q = this.search.toLowerCase();
      return this.students.filter(student =>
        (student.user?.name || "").toLowerCase().includes(q) ||
        (student.branch || "").toLowerCase().includes(q)
      );
    },

    filteredCompanyRequests() {
      const q = this.search.toLowerCase();
      return this.companyRequests.filter(request =>
        (request.data?.company_name || "").toLowerCase().includes(q)
      );
    },

    ongoingDrives() {
      const today = new Date();
      const q = this.search.toLowerCase();
      return this.drives.filter(drive =>
        new Date(drive.deadline) >= today &&
        (
          (drive.job_title || "").toLowerCase().includes(q) ||
          (drive.company_name || "").toLowerCase().includes(q)
        )
      );
    },

    filteredApplications() {
      const q = this.search.toLowerCase();
      return this.applications.filter(application =>
        (application.student?.user?.name || "").toLowerCase().includes(q) ||
        (application.drive?.company_name || "").toLowerCase().includes(q) ||
        (application.drive?.job_title || "").toLowerCase().includes(q)
      );
    }
  },

  created() {
    this.fetchData();
  },

  methods: {
    async fetchData() {
      this.loading = true;
      this.error = "";

      try {
        this.companies = await api.get("/company");
      } catch (err) {
        console.error("Company:", err);
        this.companies = [];
      }

      try {
        this.students = await api.get("/student");
      } catch (err) {
        console.error("Student:", err);
        this.students = [];
      }

      try {
        const requests = await api.get("/request");
        this.companyRequests = requests.filter(
          request => request.request_type === "company_registration"
        );
      } catch (err) {
        console.error("Request:", err);
        this.companyRequests = [];
      }

      try {
        this.drives = await api.get("/drive");
      } catch (err) {
        console.error("Drive:", err);
        this.drives = [];
      }

      try {
        this.applications = await api.get("/application");
      } catch (err) {
        console.error("Application:", err);
        this.applications = [];
      }

      this.loading = false;
    },

    async blacklist(id) {
      if (!id) return;
      try {
        await api.patch(`/user/${id}`, { action: "blacklist" });
        alert("User blacklisted successfully.");
        this.fetchData();
      } catch (err) {
        alert(err.message);
      }
    },

    async unblacklist(id) {
      if (!id) return;
      try {
        await api.patch(`/user/${id}`, { action: "unblacklist" });
        alert("User activated successfully.");
        this.fetchData();
      } catch (err) {
        alert(err.message);
      }
    },

    async approveRequest(id) {
      try {
        await api.patch(`/request/${id}`, { action: "approve" });
        alert("Request approved.");
        this.fetchData();
      } catch (err) {
        alert(err.message);
      }
    },

    async rejectRequest(id) {
      try {
        await api.patch(`/request/${id}`, { action: "reject" });
        alert("Request rejected.");
        this.fetchData();
      } catch (err) {
        alert(err.message);
      }
    },

    formatDate(date) {
      if (!date) return "";
      return new Date(date).toLocaleDateString();
    }
  }
};
</script>

<style scoped>
.container {
  max-width: 1400px;
}

.card {
  border: none;
  border-radius: 12px;
}

.card-header {
  background: #0d6efd;
  color: white;
  font-size: 18px;
  font-weight: 600;
}

.card-body {
  background: #fff;
}

.table {
  margin-bottom: 0;
}

.table th {
  background: #f8f9fa;
  font-weight: 600;
  vertical-align: middle;
  text-align: center;
}

.table td {
  vertical-align: middle;
  text-align: center;
}

.table tbody tr:hover {
  background: #f8f9fa;
}

.badge {
  padding: 8px 12px;
  font-size: 13px;
}

.btn {
  border-radius: 6px;
}

.input-group input {
  height: 45px;
}

.input-group .btn {
  min-width: 100px;
}

.spinner-border {
  width: 3rem;
  height: 3rem;
}

h2 {
  font-weight: 700;
}

.card h3 {
  color: #0d6efd;
  font-weight: 700;
  margin-bottom: 6px;
}

.card p {
  margin-bottom: 0;
  color: #6c757d;
}

@media (max-width: 768px) {
  .table {
    font-size: 13px;
  }

  .btn {
    margin-bottom: 5px;
  }

  .card-header {
    font-size: 16px;
  }
}
</style>
