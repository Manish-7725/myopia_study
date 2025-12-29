// =================================================================================
// Globals and Configuration
// =================================================================================

let currentPage = 1;
const PAGE_SIZE = 50;
let currentSearch = "";
let studentToDelete = null;
let currentVisit = {};

// =================================================================================
// API and Data Fetching
// =================================================================================

/**
 * A wrapper for the fetch API that includes authorization and error handling.
 * @param {string} url - The URL to fetch.
 * @param {object} options - Fetch options.
 * @returns {Promise<Response>}
 */
async function apiFetch(url, options = {}) {
    const token = localStorage.getItem("access");
    if (!token) {
        logout("Session expired. Please login again.");
        return Promise.reject(new Error("Unauthorized"));
    }

    const res = await fetch(url, {
        ...options,
        headers: {
            "Authorization": "Bearer " + token,
            "Content-Type": "application/json",
            ...(options.headers || {}),
        },
    });

    if (res.status === 401) {
        logout("Session expired. Please login again.");
        throw new Error("Unauthorized");
    }

    return res;
}

async function loadDashboardOverview() {
    try {
        const res = await apiFetch("http://127.0.0.1:8000/api/admin/overview/");
        const data = await res.json();
        document.getElementById("totalStudents").innerText = data.total_students;
        document.getElementById("totalFollowups").innerText = data.total_followups;
        document.getElementById("dueThisWeek").innerText = data.due_this_week;
        document.getElementById("missedFollowups").innerText = data.missed_followups;
    } catch (err) {
        console.error("Dashboard overview failed", err);
    }
}

async function loadStudents(search = "") {
    currentSearch = search;
    const tbody = document.getElementById("studentsTableBody");
    tbody.innerHTML = `<tr><td colspan="6" class="text-center py-4"><div class="spinner-border spinner-border-sm"></div> Loading…</td></tr>`;

    try {
        const res = await apiFetch(`http://127.0.0.1:8000/api/admin/students/?q=${encodeURIComponent(search)}&page=${currentPage}`);
        if (!res.ok) throw new Error("Failed to load students");

        const data = await res.json();
        const students = data.results || data;

        if (students.length === 0) {
            tbody.innerHTML = `<tr><td colspan="6" class="text-center text-muted py-4">No students found</td></tr>`;
            return;
        }

        tbody.innerHTML = students.map(s => `
            <tr>
                <td class="fw-bold ps-4">${s.student_id}</td>
                <td>${s.name}</td>
                <td>${s.age} yrs / ${s.gender}</td>
                <td>${s.school || "-"}</td>
                <td>${s.last_followup || "None"}</td>
                <td class="text-end pe-4">
                    <button class="btn btn-sm btn-outline-primary" onclick="viewStudent('${s.student_id}')" title="View Profile"><i class="bi bi-eye"></i></button>
                    <button class="btn btn-sm btn-outline-warning" onclick="editStudent('${s.student_id}')" title="Edit Student"><i class="bi bi-pencil"></i></button>
                    <button class="btn btn-sm btn-outline-danger" onclick="deleteStudent('${s.student_id}', '${s.name}')" title="Delete Student"><i class="bi bi-trash"></i></button>
                </td>
            </tr>
        `).join("");
    } catch (err) {
        console.error(err);
        tbody.innerHTML = `<tr><td colspan="6" class="text-danger text-center py-4">Failed to load students</td></tr>`;
    }
}

async function loadProfile(studentId) {
    showSection('profile');
    const container = document.getElementById("profileContent");
    container.innerHTML = "Loading...";

    try {
        const res = await apiFetch(`http://127.0.0.1:8000/api/admin/student/${studentId}/`);
        if (!res.ok) throw new Error("Failed to load profile.");

        const s = await res.json();
        container.innerHTML = `
            <h5>${s.name}</h5>
            <p>ID: ${s.student_id}</p>
            <p>Age: ${s.age}</p>
            <p>Gender: ${s.gender}</p>
            <!-- More profile details here -->
        `;
    } catch (err) {
        container.innerHTML = `<div class='text-danger'>${err.message}</div>`;
    }
}

async function loadFollowups() {
    const tbody = document.getElementById("followupsTableBody");
    tbody.innerHTML = `<tr><td colspan="5" class="text-center py-4 text-muted"><div class="spinner-border spinner-border-sm"></div> Loading follow-ups...</td></tr>`;

    try {
        const res = await apiFetch("http://127.0.0.1:8000/api/admin/followups/");
        if (!res.ok) throw new Error("Failed to load follow-ups");
        const data = await res.json();

        if (data.length === 0) {
            tbody.innerHTML = `<tr><td colspan="5" class="text-center text-muted py-4">No follow-ups found</td></tr>`;
            return;
        }

        tbody.innerHTML = data.map(f => `
            <tr>
                <td>${f.id}</td>
                <td>${f.student_name}</td>
                <td>${f.visit_date}</td>
                <td><span class="badge ${f.power_changed_last_3yrs ? 'bg-warning' : 'bg-success'}">${f.power_changed_last_3yrs ? 'Power Changed' : 'Stable'}</span></td>
                <td class="text-end"><button class="btn btn-sm btn-outline-primary" onclick="viewFollowup(${f.id})">View</button></td>
            </tr>
        `).join("");
    } catch (err) {
        console.error(err);
        tbody.innerHTML = `<tr><td colspan="5" class="text-danger text-center py-4">${err.message}</td></tr>`;
    }
}

// =================================================================================
// Student Actions (CRUD)
// =================================================================================

function handleAddStudent(e) {
    e.preventDefault();
    const form = e.target;
    let ok = true;
    ok &= validateRequired(form.name, "Student Name");
    ok &= validateRequired(form.student_id, "Student ID");
    ok &= validateNumber(form.age, "Age", 3, 20);
    ok &= validateRequired(form.school, "School");
    ok &= validateRequired(form.parent, "Parent Name");

    if (!ok) return;

    // Here you would typically send data to a server API
    console.log("Form is valid. Submitting new student...");

    // Visual feedback
    alert(`New student ${form.name.value} (${form.student_id.value}) added.`);
    loadStudents(); // Refresh the list
    bootstrap.Modal.getInstance(document.getElementById("addStudentModal")).hide();
    form.reset();
}

async function editStudent(studentId) {
    try {
        const res = await apiFetch(`http://127.0.0.1:8000/api/admin/student/${studentId}/`);
        if (!res.ok) throw new Error("Failed to load student data");
        const s = await res.json();

        document.getElementById("editStudentId").value = s.student_id;
        document.getElementById("editName").value = s.name;
        document.getElementById("editAge").value = s.age;
        document.getElementById("editGender").value = s.gender;
        document.getElementById("editSchool").value = s.school || "";

        new bootstrap.Modal(document.getElementById("editStudentModal")).show();
    } catch (err) {
        alert(err.message);
    }
}

async function saveStudentEdits() {
    const studentId = document.getElementById("editStudentId").value;
    const payload = {
        name: document.getElementById("editName").value,
        age: document.getElementById("editAge").value,
        gender: document.getElementById("editGender").value,
        school: document.getElementById("editSchool").value,
    };

    try {
        const res = await apiFetch(`http://127.0.0.1:8000/api/admin/student/${studentId}/`, {
            method: "PUT",
            body: JSON.stringify(payload),
        });

        if (res.ok) {
            bootstrap.Modal.getInstance(document.getElementById("editStudentModal")).hide();
            loadStudents();
        } else {
            alert("Update failed");
        }
    } catch (err) {
        alert("An error occurred during update.");
    }
}

function deleteStudent(studentId, studentName) {
    studentToDelete = studentId;
    document.getElementById("deleteStudentName").innerText = studentName;
    new bootstrap.Modal(document.getElementById("deleteStudentModal")).show();
}

async function confirmDeleteStudent() {
    if (!studentToDelete) return;
    try {
        const res = await apiFetch(`http://127.0.0.1:8000/api/admin/student/${studentToDelete}/`, {
            method: "DELETE"
        });
        if (res.ok) {
            bootstrap.Modal.getInstance(document.getElementById("deleteStudentModal")).hide();
            loadStudents();
        } else {
            alert("Delete failed");
        }
    } catch (err) {
        alert("An error occurred during deletion.");
    } finally {
        studentToDelete = null;
    }
}

// =================================================================================
// User Management
// =================================================================================

function handleCreateUser(e) {
    e.preventDefault();
    const form = e.target;
    let ok = true;
    ok &= validateRequired(form.fullname, "Full Name");
    ok &= validateRequired(form.username, "Username");
    ok &= validateEmailField(form.email);
    ok &= validateRequired(form.password, "Password");

    if (!ok) return;
    
    // Mock user creation
    console.log("Form is valid. Submitting new user...");
    alert(`User ${form.username.value} created successfully.`);
    // Here you would call an API and then refresh the user list
    bootstrap.Modal.getInstance(document.getElementById("addUserModal")).hide();
    form.reset();
}

function handleCreateAdmin(e) {
    e.preventDefault();
    const form = e.target;
    let ok = true;
    ok &= validateRequired(form.username, "Username");
    ok &= validateEmailField(form.email);
    ok &= validateRequired(form.password, "Password");

    if (!ok) return;

    // Mock admin creation
    console.log("Form is valid. Submitting new admin...");
    alert(`Admin privileges granted to ${form.username.value}.`);
    // Here you would call an API and then refresh the user list
    bootstrap.Modal.getInstance(document.getElementById("addAdminModal")).hide();
    form.reset();
}

function removeUser(button) {
    if (confirm("Are you sure you want to remove this user? This will revoke their access immediately.")) {
        // API call to delete user would go here
        const row = button.closest('tr');
        row.style.opacity = '0';
        setTimeout(() => row.remove(), 300);
    }
}

// =================================================================================
// Visit/Follow-up Actions
// =================================================================================

async function editVisit(studentId, visitDate) {
    try {
        const res = await apiFetch(`http://127.0.0.1:8000/api/admin/student/${studentId}/visit/${visitDate}/`);
        const data = await res.json();
        currentVisit = { studentId, visitDate };

        // These render functions would need to be created
        // document.getElementById("tabLifestyle").innerHTML = renderLifestyle(data.lifestyle);
        // document.getElementById("tabEnvironment").innerHTML = renderEnvironment(data.environment);
        // ... etc.

        new bootstrap.Modal(document.getElementById("editVisitModal")).show();
    } catch (err) {
        alert("Failed to load visit data.");
    }
}

async function saveVisitEdits() {
    const payload = {
        // These collect functions would need to be created
        // lifestyle: collectLifestyle(),
        // environment: collectEnvironment(),
        // ... etc.
    };

    try {
        const res = await apiFetch(
            `http://127.0.0.1:8000/api/admin/student/${currentVisit.studentId}/visit/${currentVisit.visitDate}/`,
            { method: "PUT", body: JSON.stringify(payload) }
        );

        if (res.ok) {
            bootstrap.Modal.getInstance(document.getElementById("editVisitModal")).hide();
            loadProfile(currentVisit.studentId);
        } else {
            alert("Failed to save visit");
        }
    } catch (err) {
        alert("An error occurred while saving the visit.");
    }
}


function viewStudent(studentId) {
    loadProfile(studentId);
}

function viewFollowup(id) {
    // Simulation
    alert('FollowUp ' + id + '\nDate: 2024-11-12\nNotes: Routine checkup. No significant changes.');
}

// =================================================================================
// Exporting
// =================================================================================

async function exportStudents(type) {
    const token = localStorage.getItem("access");
    if (!token) return;

    const url = type === "csv" 
        ? "http://127.0.0.1:8000/api/admin/export/students/csv/" 
        : "http://127.0.0.1:8000/api/admin/export/students/excel/";

    try {
        const response = await fetch(url, { headers: { "Authorization": "Bearer " + token } });
        if (!response.ok) throw new Error("Export failed");
        
        const blob = await response.blob();
        const fileURL = window.URL.createObjectURL(blob);
        const a = document.createElement("a");
        a.href = fileURL;
        a.download = `students.${type}`;
        document.body.appendChild(a);
        a.click();
        a.remove();
        window.URL.revokeObjectURL(fileURL);
    } catch (err) {
        alert(err.message);
    }
}

// =================================================================================
// UI Interaction and Navigation
// =================================================================================

function toggleSidebar() {
    const sidebar = document.getElementById("sidebar");
    const isMobile = window.innerWidth <= 768;

    if (isMobile) {
        sidebar.classList.toggle("mobile-open");
        document.getElementById("sidebarBackdrop").classList.toggle("show");
    } else {
        sidebar.classList.toggle("collapsed");
        document.getElementById("content").classList.toggle("expanded", sidebar.classList.contains("collapsed"));
        localStorage.setItem("sidebar-collapsed", sidebar.classList.contains("collapsed") ? "1" : "0");
    }
}

function closeMobileSidebar() {
    document.getElementById("sidebar").classList.remove("mobile-open");
    document.getElementById("sidebarBackdrop").classList.remove("show");
}

function showSection(id, element) {
    document.querySelectorAll(".spa-section").forEach(s => s.classList.remove("active"));
    const target = document.getElementById(id);
    if (target) target.classList.add("active");

    document.querySelectorAll("#sidebar .list-group-item").forEach(i => i.classList.remove("active"));
    if (element) element.classList.add("active");

    if (id === 'students') loadStudents();
    if (id === 'overview') loadDashboardOverview();
    if (id === 'followups') loadFollowups();
}

function logout(message = "Log out?") {
    if (message && !confirm(message)) return;
    localStorage.clear();
    window.location.href = "login.html";
}

// =================================================================================
// Form Validation
// =================================================================================

function showError(input, message) {
    clearError(input);
    const div = document.createElement("div");
    div.className = "error-msg";
    div.innerText = message;
    input.classList.add("is-invalid");
    input.parentElement.appendChild(div);
}

function clearError(input) {
    input.classList.remove("is-invalid");
    const err = input.parentElement.querySelector(".error-msg");
    if (err) err.remove();
}

function validateRequired(input, label) {
    if (!input.value.trim()) {
        showError(input, `${label} is required`);
        return false;
    }
    clearError(input);
    return true;
}

function validateEmailField(input) {
    const pattern = /^[^ - @]+@[^ - @]+\.[^ - @]+$/;
    if (!pattern.test(input.value.trim())) {
        showError(input, "Enter a valid email address");
        return false;
    }
    clearError(input);
    return true;
}

function validateNumber(input, label, min = null, max = null) {
    const value = Number(input.value);
    if (isNaN(value)) {
        showError(input, `${label} must be a number`);
        return false;
    }
    if (min !== null && value < min) { showError(input, `${label} must be at least ${min}`); return false; }
    if (max !== null && value > max) { showError(input, `${label} must be at most ${max}`); return false; }
    clearError(input);
    return true;
}

// =================================================================================
// Initialization
// =================================================================================

document.addEventListener("DOMContentLoaded", () => {
    // Check authentication and authorization
    const token = localStorage.getItem("access");
    const role = localStorage.getItem("role");

    if (!token) {
        window.location.href = "login.html";
        return;
    }
    if (role !== "admin") {
        alert("Access denied: Admins only");
        localStorage.clear();
        window.location.href = "login.html";
        return;
    }

    // Restore sidebar state
    if (localStorage.getItem("sidebar-collapsed") === "1" && window.innerWidth > 768) {
        document.getElementById("sidebar").classList.add("collapsed");
        document.getElementById("content").classList.add("expanded");
    }

    // Add tooltips to sidebar icons
    document.querySelectorAll('#sidebar .list-group-item').forEach(item => {
        const text = item.querySelector('.sidebar-text');
        if (text && !item.title) item.title = text.textContent.trim();
    });

    // Load initial data
    loadDashboardOverview();
    loadStudents();

    // Setup chart
    const ctx = document.getElementById('activityChart');
    if (ctx) {
        new Chart(ctx, {
            type: 'line',
            data: {
                labels: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
                datasets: [{ label: 'Follow-ups', data: [5, 8, 6, 10, 7, 4, 3], borderColor: 'var(--blue)', tension: 0.3 }]
            },
            options: { responsive: true, plugins: { legend: { display: false } } }
        });
    }
});
