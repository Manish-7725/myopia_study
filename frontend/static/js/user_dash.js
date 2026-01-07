// --- Core Logic ---
let ACCESS_TOKEN = localStorage.getItem("access");
const $ = (sel) => document.querySelector(sel);
const $$ = (sel) => document.querySelectorAll(sel);

// Mock Data Storage & Filtering State
let patientsData = [], formsData = [], followupsData = [];
let filteredPatients = [], filteredForms = [], filteredFollowups = [];

// Pagination State
let pages = { patients: 1, forms: 1, followups: 1 };
const PER_PAGE = 10;

// Sort State
const sortState = {
    patients: { key: null, dir: 'asc' },
    forms: { key: null, dir: 'asc' },
    followups: { key: null, dir: 'asc' }
};

// Responsive Sidebar Toggle
function toggleSidebar() {
    const sidebar = document.getElementById('sidebar');
    const content = document.getElementById('content');
    const overlay = document.getElementById('mobileOverlay');
    if (window.innerWidth >= 992) {
        sidebar.classList.toggle('collapsed');
        content.classList.toggle('expanded');
    } else {
        sidebar.classList.toggle('mobile-show');
        overlay.classList.toggle('show');
    }
}

function showSection(id, el) {
    $$(".spa-section").forEach(s => s.classList.remove("active"));
    $("#" + id).classList.add("active");
    $$(".nav-link-custom").forEach(i => i.classList.remove("active"));
    if (el) el.classList.add("active");
    if (window.innerWidth < 992) {
        document.getElementById('sidebar').classList.remove('mobile-show');
        document.getElementById('mobileOverlay').classList.remove('show');
    }
}

function switchFormState(state) { ["formsListState", "formsEntryState", "formsSuccessState"].forEach(id => $("#" + id).style.display = "none"); const target = { list: "formsListState", entry: "formsEntryState", success: "formsSuccessState" }[state]; if (target) $("#" + target).style.display = "block"; }

// --- Feature: Sorting ---
function handleSort(type, key) {
    const state = sortState[type];
    if (state.key === key) {
        state.dir = state.dir === 'asc' ? 'desc' : 'asc';
    } else {
        state.key = key;
        state.dir = 'asc';
    }

    const ths = document.querySelectorAll(`#${type}Table th`);
    ths.forEach(th => {
        th.classList.remove('sorted-asc', 'sorted-desc');
        if (th.getAttribute('onclick')?.includes(key)) {
            th.classList.add(`sorted-${state.dir}`);
        }
    });

    // Sort the *Filtered* data
    let data = type === 'patients' ? filteredPatients : type === 'forms' ? filteredForms : filteredFollowups;

    data.sort((a, b) => {
        let valA = a[key] ? a[key].toString().toLowerCase() : '';
        let valB = b[key] ? b[key].toString().toLowerCase() : '';
        if (valA < valB) return state.dir === 'asc' ? -1 : 1;
        if (valA > valB) return state.dir === 'asc' ? 1 : -1;
        return 0;
    });

    if (type === 'patients') renderPatients(filteredPatients);
    if (type === 'forms') renderForms(filteredForms);
    if (type === 'followups') renderFollowups(filteredFollowups);
}

// --- Skeleton Loading Helpers ---
function renderSkeleton(cols) {
    let html = '';
    for (let i = 0; i < 3; i++) {
        html += '<tr>';
        for (let j = 0; j < cols; j++) html += `<td><div class="skeleton" style="width:${Math.floor(Math.random() * 40 + 40)}px"></div></td>`;
        html += '</tr>';
    }
    return html;
}

// --- Mock Data Load & Render ---
document.addEventListener("DOMContentLoaded", () => {
    // Init Loaders
    $("#recentActivityList").innerHTML = renderSkeleton(4);
    $("#patientsTable tbody").innerHTML = renderSkeleton(6);
    $("#formsTable tbody").innerHTML = renderSkeleton(6);
    $("#followupsTable tbody").innerHTML = renderSkeleton(5);

    // Simulate API Delay
    setTimeout(() => {
        // Dashboard
        $("#totalStudents").innerText = "128"; $("#followupsDue").innerText = "5"; $("#totalFollowups").innerText = "42"; $("#todayEntries").innerText = "3";

        // Recent
        $("#recentActivityList").innerHTML = `<tr><td class="ps-4 fw-medium">Sunita Devi</td><td>New Entry</td><td>2026-01-05</td><td class="text-end pe-4"><button class="btn btn-sm btn-light border py-0">View</button></td></tr><tr><td class="ps-4 fw-medium">Amit Singh</td><td>Registered</td><td>2026-01-04</td><td class="text-end pe-4"><button class="btn btn-sm btn-light border py-0">View</button></td></tr>`;

        // Patients Mock
        patientsData = [
            { student_id: 'STU-1088', name: 'Amit Patel', school_name: 'ABC School', age: 12, gender: 'Male', last_visit: '2025-10-20' },
            { student_id: 'STU-1090', name: 'Priya Sharma', school_name: 'XYZ High', age: 14, gender: 'Female', last_visit: '2025-11-02' }
        ];
        filteredPatients = [...patientsData];
        renderPatients(filteredPatients);

        // Forms Mock
        formsData = [
            { student_id: 'FM-2045', date_submitted: '2024-12-08', student_name: 'Rahul Kumar', school_name: 'ABC School', status: 'Completed' },
            { student_id: 'FM-2046', date_submitted: '2024-12-09', student_name: 'Sara Khan', school_name: 'Global School', status: 'Pending' }
        ];
        filteredForms = [...formsData];
        renderForms(filteredForms);

        // Followups Mock
        followupsData = [
            { student_id: 'STU-1088', student_name: 'Amit Patel', last_visit: '2024-09-20', status: 'Completed' },
            { student_id: 'STU-1092', student_name: 'Sara Khan', last_visit: '2024-10-15', status: 'Overdue' }
        ];
        filteredFollowups = [...followupsData];
        renderFollowups(filteredFollowups);

    }, 800);
});

// Render Functions with Pagination
function renderPatients(data) {
    const start = (pages.patients - 1) * PER_PAGE;
    const end = start + PER_PAGE;
    const sliced = data.slice(start, end);

    $("#patientsTable tbody").innerHTML = sliced.map(p => `
        <tr><td class="ps-4"><div class="fw-bold">${p.name}</div><div class="small text-muted" style="font-size:0.75rem;">${p.student_id}</div></td>
        <td>${p.school_name}</td><td>${p.age}</td><td><span class="badge bg-light text-dark border">${p.gender}</span></td><td>${p.last_visit}</td>
        <td class="text-end pe-4"><button class="btn btn-sm btn-light me-1 border py-0"><i class="bi bi-eye"></i></button><button class="btn btn-sm btn-primary py-0"><i class="bi bi-plus"></i></button></td></tr>
    `).join('');
    $("#patientPaginationInfo").innerText = data.length > 0 ? `Showing ${start + 1}-${Math.min(end, data.length)} of ${data.length}` : 'No records';

    const prevBtn = document.getElementById('patientPrevBtn');
    const nextBtn = document.getElementById('patientNextBtn');
    if (prevBtn) prevBtn.disabled = pages.patients === 1;
    if (nextBtn) nextBtn.disabled = end >= data.length;
}

function renderForms(data) {
    const start = (pages.forms - 1) * PER_PAGE;
    const end = start + PER_PAGE;
    const sliced = data.slice(start, end);

    $("#formsTable tbody").innerHTML = sliced.map(f => `
        <tr><td class="ps-4 fw-bold text-primary">${f.student_id}</td><td>${f.date_submitted}</td><td>${f.student_name}</td><td>${f.school_name}</td>
        <td><span class="badge ${f.status === 'Completed' ? 'bg-success' : 'bg-warning text-dark'} bg-opacity-10 text-${f.status === 'Completed' ? 'success' : 'dark'}">${f.status}</span></td>
        <td class="text-end pe-4"><button class="btn btn-sm btn-light border py-0">View</button></td></tr>
    `).join('');
    $("#paginationInfo").innerText = data.length > 0 ? `Showing ${start + 1}-${Math.min(end, data.length)} of ${data.length}` : 'No records';

    const prevBtn = document.getElementById('prevBtn');
    const nextBtn = document.getElementById('nextBtn');
    if (prevBtn) prevBtn.disabled = pages.forms === 1;
    if (nextBtn) nextBtn.disabled = end >= data.length;
}

function renderFollowups(data) {
    const start = (pages.followups - 1) * PER_PAGE;
    const end = start + PER_PAGE;
    const sliced = data.slice(start, end);

    $("#followupsTable tbody").innerHTML = sliced.map(f => `
        <tr><td class="ps-4 fw-medium">${f.student_id}</td><td class="ps-4 fw-medium">${f.student_name}</td><td>${f.last_visit}</td>
        <td><span class="badge ${f.status === 'Overdue' ? 'bg-danger' : 'bg-success'}">${f.status}</span></td>
        <td class="text-end pe-4"><button class="btn btn-sm btn-light border py-0">View</button></td></tr>
    `).join('');

    // Note: HTML for followups pagination info ID is not standard in snippet, adding check
    const infoEl = document.getElementById('followupPaginationInfo');
    if (infoEl) infoEl.innerText = data.length > 0 ? `Showing ${start + 1}-${Math.min(end, data.length)} of ${data.length}` : 'No records';

    const prevBtn = document.getElementById('followupPrevBtn');
    const nextBtn = document.getElementById('followupNextBtn');
    if (prevBtn) prevBtn.disabled = pages.followups === 1;
    if (nextBtn) nextBtn.disabled = end >= data.length;
}

// --- Filter Functions ---
function filterPatients() {
    const searchTerm = document.getElementById('patientSearchInput').value.toLowerCase();
    const dateFrom = document.getElementById('dateFromFilter').value;
    const dateTo = document.getElementById('dateToFilter').value;
    const date = document.getElementById('dateFilter').value;
    const school = document.getElementById('schoolFilter').value.toLowerCase();
    const gender = document.getElementById('genderFilter').value;
    const age = document.getElementById('ageFilter').value;

    filteredPatients = patientsData.filter(p => {
        const matchesSearch = !searchTerm || p.name.toLowerCase().includes(searchTerm) || p.student_id.toLowerCase().includes(searchTerm);
        const matchesSchool = !school || p.school_name.toLowerCase().includes(school);
        const matchesGender = !gender || p.gender === gender;
        const matchesAge = !age || p.age == age;
        const matchesDate = (!date || p.last_visit === date) &&
            (!dateFrom || p.last_visit >= dateFrom) &&
            (!dateTo || p.last_visit <= dateTo);
        return matchesSearch && matchesSchool && matchesGender && matchesAge && matchesDate;
    });
    pages.patients = 1;
    renderPatients(filteredPatients);
}
function applyPatientFilters() { filterPatients(); }
function clearPatientFilters() {
    document.getElementById('patientSearchInput').value = '';
    document.getElementById('schoolFilter').value = '';
    document.getElementById('genderFilter').value = '';
    document.getElementById('ageFilter').value = '';
    document.getElementById('dateFilter').value = '';
    document.getElementById('dateFromFilter').value = '';
    document.getElementById('dateToFilter').value = '';
    filteredPatients = [...patientsData];
    pages.patients = 1;
    renderPatients(filteredPatients);
}

function filterForms() {
    const term = document.getElementById('searchInput').value.toLowerCase();
    const status = document.getElementById('statusFilter').value;

    filteredForms = formsData.filter(f => {
        const matchesTerm = !term || f.student_name.toLowerCase().includes(term) || f.student_id.toLowerCase().includes(term) || f.school_name.toLowerCase().includes(term);
        const matchesStatus = !status || f.status === status;
        return matchesTerm && matchesStatus;
    });

    pages.forms = 1;
    renderForms(filteredForms);
}
function applyDateFilter() { filterForms(); }

function searchStudent() {
    const term = document.getElementById('followupSearchInput').value.toLowerCase();
    const status = document.getElementById('followupStatusFilter').value;
    const school = document.getElementById('followupSchoolFilter').value.toLowerCase();
    const date = document.getElementById('followupDateFilter').value;
    const dateFrom = document.getElementById('followupDateFromFilter').value;
    const dateTo = document.getElementById('followupDateToFilter').value;

    filteredFollowups = followupsData.filter(f => {
        const matchesTerm = !term || f.student_name.toLowerCase().includes(term) || f.student_id.toLowerCase().includes(term);
        const matchesStatus = !status || f.status === status;
        // Assuming followups mock data has 'school_name' if needed, otherwise skip
        // const matchesSchool = !school || ...
        const matchesDate = (!date || f.last_visit === date) &&
            (!dateFrom || f.last_visit >= dateFrom) &&
            (!dateTo || f.last_visit <= dateTo);
        return matchesTerm && matchesStatus && matchesDate;
    });
    pages.followups = 1;
    renderFollowups(filteredFollowups);
}
function applyFollowupFilters() { searchStudent(); }
function clearFollowupFilters() {
    document.getElementById('followupSearchInput').value = '';
    document.getElementById('followupStatusFilter').value = '';
    document.getElementById('followupSchoolFilter').value = '';
    document.getElementById('followupDateFilter').value = '';
    document.getElementById('followupDateFromFilter').value = '';
    document.getElementById('followupDateToFilter').value = '';
    filteredFollowups = [...followupsData];
    pages.followups = 1;
    renderFollowups(filteredFollowups);
}

// --- Pagination Functions ---
function prevPatientPage() { if (pages.patients > 1) { pages.patients--; renderPatients(filteredPatients); } }
function nextPatientPage() {
    if (pages.patients < Math.ceil(filteredPatients.length / PER_PAGE)) { pages.patients++; renderPatients(filteredPatients); }
}

function prevPage() { if (pages.forms > 1) { pages.forms--; renderForms(filteredForms); } }
function nextPage() {
    if (pages.forms < Math.ceil(filteredForms.length / PER_PAGE)) { pages.forms++; renderForms(filteredForms); }
}

function prevFollowupPage() { if (pages.followups > 1) { pages.followups--; renderFollowups(filteredFollowups); } }
function nextFollowupPage() {
    if (pages.followups < Math.ceil(filteredFollowups.length / PER_PAGE)) { pages.followups++; renderFollowups(filteredFollowups); }
}

// --- Other Logic ---
function submitLogout() { if (confirm("Logout?")) console.log("Logging out"); }
function openNewFollowup() { new bootstrap.Modal(document.getElementById("followupModal")).show(); }
function hideFollowupForm() { $("#followupEntryCard").style.display = "none"; }
function saveSection(id) { alert("Section " + id + " saved locally."); }
function submitForm() { renderReview(); $("#popupInline").classList.remove("d-none"); $("#popupInline").classList.add("d-flex"); }
function closeReview() { $("#popupInline").classList.add("d-none"); $("#popupInline").classList.remove("d-flex"); }
function editForm() { closeReview(); }
function finalSubmit() { closeReview(); switchFormState('success'); }
function renderReview() { $("#reviewContent").innerHTML = "<p>Reviewing data...</p>"; }

// --- Followup Logic ---
function reviewFollowup() { $("#followupReviewContent").innerHTML = "<p>Followup Data Review...</p>"; $("#followupReviewOverlay").classList.remove("d-none"); $("#followupReviewOverlay").classList.add("d-flex"); bootstrap.Modal.getInstance($("#followupModal")).hide(); }
function closeFollowupReview() { $("#followupReviewOverlay").classList.add("d-none"); $("#followupReviewOverlay").classList.remove("d-flex"); new bootstrap.Modal($("#followupModal")).show(); }