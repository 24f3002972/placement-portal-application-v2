import { createRouter, createWebHistory } from 'vue-router'

import Homepage from '@/pages/Homepage.vue'
import Loginpage from '@/pages/Loginpage.vue'
import Signuppage from '@/pages/Signuppage.vue'
import AdminDashboard from "@/pages/Admin/AdminDashboard.vue";
import CompanyDashboard from "@/pages/Company/CompanyDashboard.vue";
import StudentDashboard from "@/pages/Student/StudentDashboard.vue";
import CompanyDriveDetails from "@/pages/Company/CompanyDriveDetails.vue";
import CreateDrive from "@/pages/Company/CreateDrive.vue";
import CompanyProfile from "@/pages/profiles/CompanyProfile.vue";
import DriveProfile from "@/pages/profiles/DriveProfile.vue";
import StudentHistory from "@/pages/Student/StudentHistory.vue"
import EditProfile from "@/pages/Student/EditProfile.vue"
import DriveApplications from "@/pages/Company/DriveApplications.vue";
import ApplicationReview from "@/pages/Application/ApplicationReview.vue";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {path: '/', name: "home", component: Homepage},
    {path: '/login', name: "login", component: Loginpage},
    {path: '/register', name: "register", component: Signuppage},
    {path: "/admin", component: AdminDashboard },
    {path: "/company", component: CompanyDashboard },
    {path: "/student", component: StudentDashboard },
    {path: "/company/drive/:id", component: CompanyDriveDetails },
    {path: "/company/create_drive", component: CreateDrive},
    {path: "/company/:id", name: "CompanyProfile", component: CompanyProfile},
    {path: "/drive/:id", name: "DriveProfile", component: DriveProfile},
    {path: "/student/history", component: StudentHistory},
    {path: "/student/edit", component: EditProfile},
    {path: "/company/drive/:id/applications", component: DriveApplications},
    {path: "/application/:id", component: ApplicationReview}
  ],
})

export default router
