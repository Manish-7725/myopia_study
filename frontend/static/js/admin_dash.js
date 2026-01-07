/*
=====================================================
    Mock Data (Fallback)
=====================================================
*/

const mockData = {
    metrics: {
        totalUsers: 8,
        totalStudents: 125,
        activeClinicians: 5,
        overdueFollowups: 12
    },
    alerts: [
        {
            type: 'critical',
            icon: 'bi-exclamation-triangle-fill',
            title: 'Overdue Follow-ups',
            message: '12 students have missed their scheduled follow-up appointments',
            priority: 'Critical - Requires immediate attention',
            badgeClass: 'bg-danger',
            buttonText: 'View Details',
            buttonClass: 'btn-outline-danger'
        },
        {
            type: 'warning',
            icon: 'bi-person-dash-fill',
            title: 'Inactive Users',
            message: '3 clinicians haven\'t logged in for 7+ days',
            priority: 'Monitor user activity',
            badgeClass: 'bg-warning',
            buttonText: 'Review Users',
            buttonClass: 'btn-outline-warning'
        },
        {
            type: 'info',
            icon: 'bi-shield-exclamation',
            title: 'Data Validation Warnings',
            message: '8 forms contain incomplete or inconsistent data',
            priority: 'Review data quality',
            badgeClass: 'bg-info',
            buttonText: 'Check Forms',
            buttonClass: 'btn-outline-info'
        }
    ],
    recentActions: [
        {
            type: 'user_created',
            icon: 'bi-person-plus-fill',
            title: 'User Created',
            message: 'Dr. Sarah Johnson account activated',
            time: '2 hours ago',
            badgeClass: 'bg-success'
        },
        {
            type: 'form_locked',
            icon: 'bi-file-earmark-lock-fill',
            title: 'Form Locked',
            message: 'Student ID: STU-2024-045 finalized',
            time: '4 hours ago',
            badgeClass: 'bg-primary'
        },
        {
            type: 'record_edited',
            icon: 'bi-pencil-square',
            title: 'Record Edited',
            message: 'Clinical data updated for Alice Johnson',
            time: '6 hours ago',
            badgeClass: 'bg-info'
        },
        {
            type: 'followup_scheduled',
            icon: 'bi-calendar-plus-fill',
            title: 'Follow-up Scheduled',
            message: 'New appointment for Bob Smith',
            time: '8 hours ago',
            badgeClass: 'bg-warning'
        }
    ],
    students: [
        { id: 'STU001', name: 'Alice Johnson', school: 'Lincoln High School', age: 14, gender: 'Female', lastVisit: '2024-01-15' },
        { id: 'STU002', name: 'Bob Smith', school: 'Washington Middle School', age: 13, gender: 'Male', lastVisit: '2024-01-10' },
        { id: 'STU003', name: 'Charlie Brown', school: 'Jefferson Elementary', age: 12, gender: 'Male', lastVisit: '2024-01-08' },
        { id: 'STU004', name: 'Diana Prince', school: 'Lincoln High School', age: 15, gender: 'Female', lastVisit: '2024-01-12' },
        { id: 'STU005', name: 'Edward Norton', school: 'Washington Middle School', age: 14, gender: 'Male', lastVisit: '2024-01-14' },
        { id: 'STU006', name: 'Fiona Green', school: 'Jefferson Elementary', age: 11, gender: 'Female', lastVisit: '2024-01-09' },
        { id: 'STU007', name: 'George Lucas', school: 'Lincoln High School', age: 16, gender: 'Male', lastVisit: '2024-01-13' },
        { id: 'STU008', name: 'Helen Troy', school: 'Washington Middle School', age: 13, gender: 'Female', lastVisit: '2024-01-11' }
    ],
    users: [
        { username: 'admin', fullname: 'System Administrator', role: 'Admin', joined: '2023-01-01' },
        { username: 'dr_smith', fullname: 'Dr. Sarah Smith', role: 'User', joined: '2023-06-15' },
        { username: 'dr_jones', fullname: 'Dr. Michael Jones', role: 'User', joined: '2023-08-20' },
        { username: 'clinician1', fullname: 'Jane Clinician', role: 'Data Entry', joined: '2023-09-10' }
    ]
};

/*
=====================================================
    General Utilities
=====================================================
*/

// Debounce function to limit the rate of function execution
const debounce = (func, delay) => {
    let timeoutId;
    return (...args) => {
        clearTimeout(timeoutId);
        timeoutId = setTimeout(() => {
            func.apply(this, args);
        }, delay);
    };
};

// Get a cookie by name
const getCookie = (name) => {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}


/*
=====================================================
    Authentication & Navigation
=====================================================
*/

// Logout the user
const submitLogout = () => {
    // Perform any necessary cleanup (e.g., clearing tokens)
    document.getElementById('logoutForm').submit();
};

// Handle SPA-like section toggling
const showSection = (sectionId, clickedElement) => {
    // Hide all sections
    document.querySelectorAll('.spa-section').forEach(section => {
        section.classList.remove('active');
    });

    // Show the target section
    const targetSection = document.getElementById(sectionId);
    if (targetSection) {
        targetSection.classList.add('active');
    }

    // Update active state for sidebar links
    document.querySelectorAll('#sidebar .nav-link').forEach(link => {
        link.classList.remove('active');
    });
    if (clickedElement) {
        clickedElement.classList.add('active');
    }
};

// Toggle sidebar visibility (responsive for all devices)
const toggleSidebar = () => {
    const sidebar = document.getElementById('sidebar');
    const overlay = document.querySelector('.sidebar-overlay');

    if (!sidebar) return;

    // Check if we're on mobile/tablet (< 992px)
    const isMobile = window.innerWidth < 992;

    if (isMobile) {
        // Mobile/tablet: toggle overlay
        const isOpen = sidebar.classList.contains('show');
        if (isOpen) {
            sidebar.classList.remove('show');
            if (overlay) overlay.classList.remove('show');
        } else {
            sidebar.classList.add('show');
            if (overlay) overlay.classList.add('show');
        }
    } else {
        // Desktop: toggle collapsed state
        sidebar.classList.toggle('collapsed');
    }
};

/*
=====================================================
    Data Fetching & Rendering
=====================================================
*/


// State for pagination
let studentPage = 1;
const studentsPerPage = 10;
let students = [];
let filteredStudents = [];

// Populate dashboard metrics
const populateMetrics = async () => {
    try {
        const accessToken = getCookie('access_token');
        const response = await fetch('/api/admin/overview/', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${accessToken}`
            }
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();

        document.getElementById('totalStudents').textContent = data.total_students || '--';
        document.getElementById('totalFollowups').textContent = data.total_followups || '--';
        document.getElementById('todayEntries').textContent = data.due_this_week || '--';
    } catch (error) {
        console.error('Error fetching admin overview:', error);
        // Fallback to mock data on error
        document.getElementById('totalUsers').textContent = mockData.metrics.totalUsers;
        document.getElementById('totalStudents').textContent = mockData.metrics.totalStudents;
        document.getElementById('activeClinicians').textContent = mockData.metrics.activeClinicians;
        document.getElementById('overdueFollowups').textContent = mockData.metrics.overdueFollowups;

        // Populate alerts and recent actions with mock data
        populateAlerts(mockData.alerts);
        populateRecentActions(mockData.recentActions);
    }
};

// Render the students table
const renderStudentsTable = async () => {
    try {
        const accessToken = getCookie('access_token');
        const response = await fetch('/api/admin/students/', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${accessToken}`
            }
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        students = await response.json();
        filteredStudents = [...students];

        const tableBody = document.getElementById('studentsTableBody');
        if (!tableBody) return;

        const startIndex = (studentPage - 1) * studentsPerPage;
        const endIndex = startIndex + studentsPerPage;
        const paginatedStudents = filteredStudents.slice(startIndex, endIndex);

        tableBody.innerHTML = paginatedStudents.map(student => `
            <tr>
                <td class="ps-4">${student.id}</td>
                <td>${student.name}</td>
                <td>${student.school}</td>
                <td>${student.age}</td>
                <td>${student.gender}</td>
                <td>${student.lastVisit}</td>
                <td class="text-end pe-4">
                    <button class="btn btn-sm btn-outline-primary" onclick="viewStudent('${student.id}')">
                        <i class="bi bi-eye"></i>
                    </button>
                    <button class="btn btn-sm btn-outline-secondary" onclick="editStudent('${student.id}')">
                        <i class="bi bi-pencil"></i>
                    </button>
                    <button class="btn btn-sm btn-outline-danger" onclick="deleteStudent('${student.id}', '${student.name}')">
                        <i class="bi bi-trash"></i>
                    </button>
                </td>
            </tr>
        `).join('');

        updateStudentPaginationControls();
        populateSchoolFilter();
    } catch (error) {
        console.error('Error fetching students:', error);
        // You might want to show an error message in the UI
    }
};

// Update student pagination controls and info
const updateStudentPaginationControls = () => {
    const totalPages = Math.ceil(filteredStudents.length / studentsPerPage);
    document.getElementById('patientPrevBtn').disabled = studentPage === 1;
    document.getElementById('patientNextBtn').disabled = studentPage >= totalPages;

    const start = (studentPage - 1) * studentsPerPage + 1;
    const end = Math.min(start + studentsPerPage - 1, filteredStudents.length);
    document.getElementById('patientPaginationInfo').textContent = 
        `Showing ${start}-${end} of ${filteredStudents.length}`;
};

// Pagination: Go to the previous page
const prevPatientPage = () => {
    if (studentPage > 1) {
        studentPage--;
        renderStudentsTable();
    }
};

// Pagination: Go to the next page
const nextPatientPage = () => {
    const totalPages = Math.ceil(filteredStudents.length / studentsPerPage);
    if (studentPage < totalPages) {
        studentPage++;
        renderStudentsTable();
    }
};

// Render the users table
const renderUsersTable = async () => {
    try {
        const accessToken = getCookie('access_token');
        const response = await fetch('/api/admin/users/', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${accessToken}`
            }
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const users = await response.json();
        const tableBody = document.getElementById('usersTableBody');
        if (!tableBody) return;

        tableBody.innerHTML = users.map(user => `
            <tr>
                <td class="ps-4">${user.username}</td>
                <td>${user.email || user.fullname}</td>
                <td>
                    <span class="badge ${user.role === 'Admin' ? 'bg-danger' : user.role === 'Data Entry' ? 'bg-info' : 'bg-secondary'}">
                        ${user.role}
                    </span>
                </td>
                <td>${user.date_joined ? new Date(user.date_joined).toLocaleDateString() : user.joined}</td>
                <td>${user.last_login ? new Date(user.last_login).toLocaleString() : 'N/A'}</td>
                <td class="text-end pe-4">
                    <div class="btn-group btn-group-sm">
                        <button class="btn btn-outline-primary" onclick="openAdminOverrideModal(${user.id}, '${user.username}', ${user.is_active})" ${user.role === 'Admin' ? 'disabled' : ''} title="Admin Overrides">
                            <i class="bi bi-gear"></i>
                        </button>
                        <button class="btn btn-outline-warning" onclick="openResetPasswordModal(${user.id}, '${user.username}')" ${user.role === 'Admin' ? 'disabled' : ''} title="Reset Password">
                            <i class="bi bi-key"></i>
                        </button>
                        <button class="btn btn-sm btn-outline-danger" onclick="deleteUser(${user.id}, '${user.username}')" ${user.role === 'Admin' ? 'disabled' : ''} title="Delete User">
                            <i class="bi bi-trash"></i>
                        </button>
                    </div>
                </td>
            </tr>
        `).join('');
    } catch (error) {
        console.error('Error fetching users:', error);
        // You might want to show an error message in the UI
    }
};


/*
=====================================================
    Event Handlers & Modal Logic
=====================================================
*/

// Filter students based on form inputs
const applyPatientFilters = () => {
    const searchTerm = document.getElementById('patientSearchInput').value.toLowerCase();
    
    // Add other filter values here
    const school = document.getElementById('schoolFilter').value.toLowerCase();
    const gender = document.getElementById('genderFilter').value;
    const age = document.getElementById('ageFilter').value;

    filteredStudents = mockData.students.filter(student => {
        const matchesSearch = student.name.toLowerCase().includes(searchTerm) || student.id.toLowerCase().includes(searchTerm);
        const matchesSchool = !school || student.school.toLowerCase().includes(school);
        const matchesGender = !gender || student.gender === gender;
        const matchesAge = !age || student.age.toString() === age;
        return matchesSearch && matchesSchool && matchesGender && matchesAge;
    });

    studentPage = 1; // Reset to first page
    renderStudentsTable();
};

// Clear all patient filters
const clearPatientFilters = () => {
    document.getElementById('patientSearchInput').value = '';
    document.getElementById('schoolFilter').value = '';
    document.getElementById('genderFilter').value = '';
    document.getElementById('ageFilter').value = '';
    document.getElementById('dateFromFilter').value = '';
    document.getElementById('dateToFilter').value = '';
    document.getElementById('dateFilter').value = '';

    filteredStudents = [...mockData.students];
    studentPage = 1;
    renderStudentsTable();
};

// Handle create user form submission
const handleCreateUser = async (event) => {
    event.preventDefault();
    const form = new FormData(event.target);
    const userData = Object.fromEntries(form.entries());

    try {
        const accessToken = getCookie('access_token');
        const response = await fetch('/api/signup/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${accessToken}`
            },
            body: JSON.stringify(userData)
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        renderUsersTable();
        const modal = bootstrap.Modal.getInstance(document.getElementById('addUserModal'));
        modal.hide();
        event.target.reset();
    } catch (error) {
        console.error('Error creating user:', error);
        // You might want to show an error message in the UI
    }
};

// Handle create admin form submission
const handleCreateAdmin = async (event) => {
    event.preventDefault();
    const form = new FormData(event.target);
    const adminData = Object.fromEntries(form.entries());

    try {
        const accessToken = getCookie('access_token');
        const response = await fetch('/api/admin/create-admin/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${accessToken}`
            },
            body: JSON.stringify(adminData)
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        renderUsersTable();
        const modal = bootstrap.Modal.getInstance(document.getElementById('addAdminModal'));
        modal.hide();
        event.target.reset();
    } catch (error) {
        console.error('Error creating admin:', error);
        // You might want to show an error message in the UI
    }
};

// Delete user
const deleteUser = async (userId, username) => {
    if (confirm(`Are you sure you want to delete user "${username}"? This action cannot be undone.`)) {
        try {
            const accessToken = getCookie('access_token');
            const response = await fetch(`/api/admin/user/${userId}/`, {
                method: 'DELETE',
                headers: {
                    'Authorization': `Bearer ${accessToken}`
                }
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.error || `HTTP error! status: ${response.status}`);
            }

            alert(`User "${username}" deleted successfully.`);
            renderUsersTable(); // Refresh the table
        } catch (error) {
            console.error('Error deleting user:', error);
            alert(`Failed to delete user: ${error.message}`);
        }
    }
};

// Open Reset Password Modal
const openResetPasswordModal = (userId, username) => {
    document.getElementById('resetPasswordUserId').value = userId;
    document.getElementById('resetPasswordUsername').textContent = username;
    const resetModal = new bootstrap.Modal(document.getElementById('resetPasswordModal'));
    resetModal.show();
};

// Handle Reset Password Form Submission
const handleResetPassword = async (event) => {
    event.preventDefault();
    const userId = document.getElementById('resetPasswordUserId').value;
    const newPassword = event.target.elements['new_password'].value;
    const confirmPassword = event.target.elements['confirm_password'].value;

    if (newPassword !== confirmPassword) {
        alert('New password and confirm password do not match.');
        return;
    }

    try {
        const accessToken = getCookie('access_token');
        const response = await fetch(`/api/admin/user/${userId}/reset-password/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${accessToken}`
            },
            body: JSON.stringify({ new_password: newPassword })
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.error || `HTTP error! status: ${response.status}`);
        }

        alert('Password reset successfully! User sessions invalidated.');
        const modal = bootstrap.Modal.getInstance(document.getElementById('resetPasswordModal'));
        modal.hide();
        event.target.reset();
        renderUsersTable(); // Refresh the table to show any last login updates (if implemented)
    } catch (error) {
        console.error('Error resetting password:', error);
        alert(`Failed to reset password: ${error.message}`);
    }
};

// Open Admin Override Modal
const openAdminOverrideModal = (userId, username, isActive) => {
    document.getElementById('overrideUserId').value = userId;
    document.getElementById('overrideUsername').textContent = username;
    document.getElementById('userActiveToggle').checked = isActive;
    const overrideModal = new bootstrap.Modal(document.getElementById('adminOverrideModal'));
    overrideModal.show();
};

// Handle Admin Override Form Submission (for is_active toggle)
const handleAdminOverride = async (event) => {
    event.preventDefault();
    const userId = document.getElementById('overrideUserId').value;
    const isActive = document.getElementById('userActiveToggle').checked;

    try {
        const accessToken = getCookie('access_token');
        const response = await fetch(`/api/admin/user/${userId}/`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${accessToken}`
            },
            body: JSON.stringify({ is_active: isActive })
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.error || `HTTP error! status: ${response.status}`);
        }

        alert(`User account ${isActive ? 'activated' : 'deactivated'} successfully.`);
        const modal = bootstrap.Modal.getInstance(document.getElementById('adminOverrideModal'));
        modal.hide();
        renderUsersTable(); // Refresh the table
    } catch (error) {
        console.error('Error updating user status:', error);
        alert(`Failed to update user status: ${error.message}`);
    }
};

// Force Logout User
const forceLogoutUser = async () => {
    const userId = document.getElementById('overrideUserId').value;
    const username = document.getElementById('overrideUsername').textContent;

    if (confirm(`Are you sure you want to force logout "${username}"? This will invalidate all their active sessions.`)) {
        try {
            const accessToken = getCookie('access_token');
            const response = await fetch(`/api/admin/user/${userId}/force-logout/`, {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${accessToken}`
                }
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.error || `HTTP error! status: ${response.status}`);
            }

            alert(`User "${username}" force logged out successfully.`);
            const modal = bootstrap.Modal.getInstance(document.getElementById('adminOverrideModal'));
            modal.hide();
            renderUsersTable(); // Refresh the table
        } catch (error) {
            console.error('Error forcing logout:', error);
            alert(`Failed to force logout user: ${error.message}`);
        }
    }
};

// View student details in a modal
const viewStudent = (studentId) => {
    const student = mockData.students.find(s => s.id === studentId);
    if (!student) return;

    // Populate profile modal
    document.getElementById('profileName').textContent = student.name;
    document.getElementById('profileId').textContent = `ID: ${student.id}`;
    document.getElementById('profileAge').textContent = student.age;
    document.getElementById('profileGender').textContent = student.gender;
    document.getElementById('profileSchool').textContent = student.school;
    document.getElementById('profileCreatedBy').textContent = student.createdBy || 'System';
    document.getElementById('profileLastVisit').textContent = student.lastVisit;
    document.getElementById('profileTotalVisits').textContent = student.totalVisits || '1';
    document.getElementById('profileNextVisit').textContent = student.nextVisit || 'Not scheduled';

    // Set status badge
    const statusBadge = document.getElementById('profileStatus');
    statusBadge.textContent = getStatusText(student.status || 'active');
    statusBadge.className = `badge ${getStatusBadgeClass(student.status || 'active')}`;

    // Populate followups (mock data)
    const followupsBody = document.querySelector('#profileFollowups tbody');
    const mockFollowups = [
        { date: student.lastVisit, type: 'Regular Checkup', status: 'Completed', notes: 'Vision stable' },
        { date: '2023-12-15', type: 'Initial Assessment', status: 'Completed', notes: 'Myopia detected' }
    ];

    followupsBody.innerHTML = mockFollowups.map(followup => `
        <tr>
            <td>${followup.date}</td>
            <td>${followup.type}</td>
            <td><span class="badge bg-success">${followup.status}</span></td>
            <td>${followup.notes}</td>
        </tr>
    `).join('');

    const profileModal = new bootstrap.Modal(document.getElementById('studentProfileModal'));
    profileModal.show();
};

// Open edit student modal
const editStudent = async (studentId) => {
    try {
        const accessToken = getCookie('access_token');
        const response = await fetch(`/api/admin/student/${studentId}/`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${accessToken}`
            }
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const student = await response.json();

        document.getElementById('editStudentId').value = student.student_id;
        document.getElementById('editName').value = student.name;
        document.getElementById('editAge').value = student.age;
        document.getElementById('editGender').value = student.gender;
        document.getElementById('editSchool').value = student.school_name;

        const editModal = new bootstrap.Modal(document.getElementById('editStudentModal'));
        editModal.show();
    } catch (error) {
        console.error('Error fetching student details:', error);
    }
};

// Save edited student details
const saveStudentEdits = async () => {
    const studentId = document.getElementById('editStudentId').value;
    const studentData = {
        name: document.getElementById('editName').value,
        age: document.getElementById('editAge').value,
        gender: document.getElementById('editGender').value,
        school: document.getElementById('editSchool').value,
    };

    try {
        const accessToken = getCookie('access_token');
        const response = await fetch(`/api/admin/student/${studentId}/`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${accessToken}`
            },
            body: JSON.stringify(studentData)
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        renderStudentsTable();
        const modal = bootstrap.Modal.getInstance(document.getElementById('editStudentModal'));
        modal.hide();
    } catch (error) {
        console.error('Error updating student:', error);
    }
};


// Open delete confirmation modal
const deleteStudent = (studentId, studentName) => {
    document.getElementById('deleteStudentId').value = studentId;
    document.getElementById('deleteStudentName').textContent = studentName;
    const deleteModal = new bootstrap.Modal(document.getElementById('deleteStudentModal'));
    deleteModal.show();
};

// Confirm and delete the student
const confirmDeleteStudent = async () => {
    const studentId = document.getElementById('deleteStudentId').value;

    try {
        const accessToken = getCookie('access_token');
        const response = await fetch(`/api/admin/student/${studentId}/`, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${accessToken}`
            }
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        renderStudentsTable();
        const modal = bootstrap.Modal.getInstance(document.getElementById('deleteStudentModal'));
        modal.hide();
    } catch (error) {
        console.error('Error deleting student:', error);
    }
};

/*
=====================================================
    Enhanced Student Management Functions
=====================================================
*/

// Export students data
const exportStudents = () => {
    console.log('Exporting students data');
    // Implement export functionality here
    // Could generate CSV or Excel file
};

// Show merge duplicates interface
const showMergeDuplicates = () => {
    // Find potential duplicates based on name similarity
    const potentialDuplicates = findPotentialDuplicates();

    const duplicatesBody = document.getElementById('duplicatesBody');
    if (potentialDuplicates.length === 0) {
        duplicatesBody.innerHTML = '<tr><td colspan="4" class="text-center text-muted py-4">No potential duplicates found</td></tr>';
    } else {
        duplicatesBody.innerHTML = potentialDuplicates.map(group => `
            <tr>
                <td>
                    <div class="d-flex flex-column gap-1">
                        ${group.map(student => `
                            <div class="d-flex align-items-center gap-2">
                                <input type="radio" name="primary-${group[0].id}" value="${student.id}" ${student === group[0] ? 'checked' : ''}>
                                <span>${student.name} (${student.id})</span>
                            </div>
                        `).join('')}
                    </div>
                </td>
                <td>${group[0].school}</td>
                <td>${group[0].age}/${group[0].gender}</td>
                <td>
                    <button class="btn btn-sm btn-primary" onclick="mergeStudents('${group.map(s => s.id).join(',')}')">Merge Selected</button>
                </td>
            </tr>
        `).join('');
    }

    const mergeModal = new bootstrap.Modal(document.getElementById('mergeDuplicatesModal'));
    mergeModal.show();
};

// Find potential duplicates based on name similarity
const findPotentialDuplicates = () => {
    const duplicates = [];
    const processed = new Set();

    mockData.students.forEach(student => {
        if (processed.has(student.id)) return;

        const similar = mockData.students.filter(s =>
            s.id !== student.id &&
            !processed.has(s.id) &&
            (s.name.toLowerCase().includes(student.name.split(' ')[0].toLowerCase()) ||
             levenshteinDistance(s.name.toLowerCase(), student.name.toLowerCase()) <= 2)
        );

        if (similar.length > 0) {
            const group = [student, ...similar];
            duplicates.push(group);
            group.forEach(s => processed.add(s.id));
        }
    });

    return duplicates;
};

// Simple Levenshtein distance for name similarity
const levenshteinDistance = (str1, str2) => {
    const matrix = [];
    for (let i = 0; i <= str2.length; i++) {
        matrix[i] = [i];
    }
    for (let j = 0; j <= str1.length; j++) {
        matrix[0][j] = j;
    }
    for (let i = 1; i <= str2.length; i++) {
        for (let j = 1; j <= str1.length; j++) {
            if (str2.charAt(i - 1) === str1.charAt(j - 1)) {
                matrix[i][j] = matrix[i - 1][j - 1];
            } else {
                matrix[i][j] = Math.min(
                    matrix[i - 1][j - 1] + 1,
                    matrix[i][j - 1] + 1,
                    matrix[i - 1][j] + 1
                );
            }
        }
    }
    return matrix[str2.length][str1.length];
};

// Merge selected students
const mergeStudents = (studentIds) => {
    const ids = studentIds.split(',');
    const primaryId = document.querySelector(`input[name="primary-${ids[0]}"]:checked`)?.value;

    if (!primaryId) {
        alert('Please select a primary record to keep');
        return;
    }

    if (confirm(`Merge ${ids.length} records into ${primaryId}? This action cannot be undone.`)) {
        console.log('Merging students:', ids, 'into primary:', primaryId);
        // Implement merge functionality
        // Remove duplicate records and update primary with combined data
    }
};

// Show only flagged students
const showFlaggedStudents = () => {
    document.getElementById('statusFilter').value = 'flagged';
    applyPatientFilters();
};

// Show only locked students
const showLockedStudents = () => {
    document.getElementById('statusFilter').value = 'locked';
    applyPatientFilters();
};

// Toggle select all students
const toggleSelectAll = () => {
    const selectAllCheckbox = document.getElementById('selectAllStudents');
    const checkboxes = document.querySelectorAll('#studentsTableBody input[type="checkbox"]');

    checkboxes.forEach(checkbox => {
        checkbox.checked = selectAllCheckbox.checked;
    });
};

// Bulk lock selected students
const bulkLockStudents = () => {
    const selectedStudents = getSelectedStudents();
    if (selectedStudents.length === 0) {
        alert('Please select students to lock');
        return;
    }

    if (confirm(`Lock ${selectedStudents.length} selected student(s)?`)) {
        console.log('Locking students:', selectedStudents);
        // Implement bulk lock functionality
    }
};

// Bulk flag selected students
const bulkFlagStudents = () => {
    const selectedStudents = getSelectedStudents();
    if (selectedStudents.length === 0) {
        alert('Please select students to flag');
        return;
    }

    if (confirm(`Flag ${selectedStudents.length} selected student(s)?`)) {
        console.log('Flagging students:', selectedStudents);
        // Implement bulk flag functionality
    }
};

// Bulk export selected students
const bulkExportStudents = () => {
    const selectedStudents = getSelectedStudents();
    if (selectedStudents.length === 0) {
        alert('Please select students to export');
        return;
    }

    console.log('Exporting selected students:', selectedStudents);
    // Implement bulk export functionality
};

// Get selected student IDs
const getSelectedStudents = () => {
    const checkboxes = document.querySelectorAll('#studentsTableBody input[type="checkbox"]:checked');
    return Array.from(checkboxes).map(checkbox => checkbox.value);
};

// Populate school filter options
const populateSchoolFilter = () => {
    const schoolFilter = document.getElementById('schoolFilter');
    if (!schoolFilter) return;

    // Get unique schools from current students
    const schools = [...new Set(filteredStudents.map(student => student.school))];

    // Clear existing options except "All Schools"
    schoolFilter.innerHTML = '<option value="">All Schools</option>';

    // Add school options
    schools.forEach(school => {
        const option = document.createElement('option');
        option.value = school;
        option.textContent = school;
        schoolFilter.appendChild(option);
    });
};

// Get status badge class
const getStatusBadgeClass = (status) => {
    switch (status) {
        case 'active': return 'bg-success';
        case 'locked': return 'bg-warning';
        case 'flagged': return 'bg-info';
        case 'inactive': return 'bg-secondary';
        default: return 'bg-secondary';
    }
};

// Get status text
const getStatusText = (status) => {
    switch (status) {
        case 'active': return 'Active';
        case 'locked': return 'Locked';
        case 'flagged': return 'Flagged';
        case 'inactive': return 'Inactive';
        default: return 'Active';
    }
};

// Update select all checkbox state
const updateSelectAllState = () => {
    const checkboxes = document.querySelectorAll('#studentsTableBody input[type="checkbox"]');
    const selectAllCheckbox = document.getElementById('selectAllStudents');

    const checkedBoxes = document.querySelectorAll('#studentsTableBody input[type="checkbox"]:checked');
    selectAllCheckbox.checked = checkboxes.length > 0 && checkedBoxes.length === checkboxes.length;
    selectAllCheckbox.indeterminate = checkedBoxes.length > 0 && checkedBoxes.length < checkboxes.length;
};

// Lock a student record
const lockStudent = (studentId) => {
    if (confirm('Lock this student record? Locked records cannot be modified.')) {
        console.log('Locking student:', studentId);
        // Implement lock functionality
    }
};

// Flag a student for review
const flagStudent = (studentId) => {
    if (confirm('Flag this student for review?')) {
        console.log('Flagging student:', studentId);
        // Implement flag functionality
    }
};


/*
=====================================================
    Forms Management
=====================================================
*/

// Switch between form states (list/entry/success)
const switchFormState = (state) => {
    const listState = document.getElementById('formsListState');
    const entryState = document.getElementById('formsEntryState');
    const successState = document.getElementById('formsSuccessState');

    if (listState) listState.style.display = state === 'list' ? 'block' : 'none';
    if (entryState) entryState.style.display = state === 'entry' ? 'block' : 'none';
    if (successState) successState.style.display = state === 'success' ? 'block' : 'none';
};

// Save section progress
const saveSection = (section) => {
    console.log(`Saving section ${section}`);
    // Implement save logic here
};

// Reset section
const resetSection = (section) => {
    console.log(`Resetting section ${section}`);
    // Implement reset logic here
};

// Submit form
const submitForm = () => {
    console.log('Submitting form');
    // Implement submit logic here
    switchFormState('success');
};

// Open edit profile
const openEditProfile = () => {
    console.log('Opening edit profile');
    // Implement edit profile logic here
};

/*
=====================================================
    Follow-ups Management
=====================================================
*/

// Open new followup modal
const openNewFollowup = () => {
    const modal = new bootstrap.Modal(document.getElementById('followupModal'));
    modal.show();
};

// Apply followup filters
const applyFollowupFilters = () => {
    console.log('Applying followup filters');
    // Implement filter logic here
};

// Previous followup page
const prevFollowupPage = () => {
    console.log('Previous followup page');
    // Implement pagination logic here
};

// Next followup page
const nextFollowupPage = () => {
    console.log('Next followup page');
    // Implement pagination logic here
};

// Review followup
const reviewFollowup = () => {
    console.log('Reviewing followup');
    // Implement review logic here
};

// Close followup review
const closeFollowupReview = () => {
    console.log('Closing followup review');
    // Implement close logic here
};

// Edit followup
const editFollowup = () => {
    console.log('Editing followup');
    // Implement edit logic here
};

// Close review overlay
const closeReview = () => {
    const overlay = document.getElementById('popupInline');
    if (overlay) overlay.style.display = 'none';
};

// Edit form (from review overlay)
const editForm = () => {
    closeReview();
    // Switch back to form entry state
    switchFormState('entry');
};

// Final submit from review overlay
const finalSubmit = () => {
    closeReview();
    submitForm();
};

// Submit followup
const submitFollowup = () => {
    console.log('Submitting followup');
    // Implement followup submission logic here
    const modal = bootstrap.Modal.getInstance(document.getElementById('followupModal'));
    modal.hide();
};

// Final followup submit
const followupFinalSubmit = () => {
    console.log('Final followup submit');
    submitFollowup();
};

/*
=====================================================
    Forms & Data Control
=====================================================
*/

// Global variables for forms management
let selectedForms = new Set();
let currentFormsPage = 1;
let formsPerPage = 10;

// Toggle all forms selection
const toggleAllForms = () => {
    const selectAllCheckbox = document.getElementById('selectAllForms');
    const checkboxes = document.querySelectorAll('#formsDataBody input[type="checkbox"]');

    checkboxes.forEach(checkbox => {
        checkbox.checked = selectAllCheckbox.checked;
        const formId = checkbox.value;
        if (selectAllCheckbox.checked) {
            selectedForms.add(formId);
        } else {
            selectedForms.delete(formId);
        }
    });

    updateBulkActionsVisibility();
};

// Toggle individual form selection
const toggleFormSelection = (formId) => {
    const checkbox = document.querySelector(`input[value="${formId}"]`);
    if (checkbox.checked) {
        selectedForms.add(formId);
    } else {
        selectedForms.delete(formId);
    }

    // Update select all checkbox state
    const allCheckboxes = document.querySelectorAll('#formsDataBody input[type="checkbox"]');
    const checkedBoxes = document.querySelectorAll('#formsDataBody input[type="checkbox"]:checked');
    const selectAllCheckbox = document.getElementById('selectAllForms');
    selectAllCheckbox.checked = allCheckboxes.length === checkedBoxes.length && allCheckboxes.length > 0;

    updateBulkActionsVisibility();
};

// Update bulk actions visibility
const updateBulkActionsVisibility = () => {
    const bulkActionsCard = document.getElementById('bulkActionsCard');
    const selectedCount = document.getElementById('selectedCount');

    if (selectedForms.size > 0) {
        bulkActionsCard.style.display = 'block';
        selectedCount.textContent = `${selectedForms.size} form${selectedForms.size > 1 ? 's' : ''} selected`;
    } else {
        bulkActionsCard.style.display = 'none';
    }
};

// Clear form selection
const clearFormSelection = () => {
    selectedForms.clear();
    document.querySelectorAll('#formsDataBody input[type="checkbox"]').forEach(checkbox => {
        checkbox.checked = false;
    });
    document.getElementById('selectAllForms').checked = false;
    updateBulkActionsVisibility();
};

// Bulk lock forms
const bulkLockForms = async () => {
    if (selectedForms.size === 0) return;

    if (confirm(`Lock ${selectedForms.size} selected form(s)? This will prevent further edits.`)) {
        try {
            const accessToken = getCookie('access_token');
            const response = await fetch('/api/forms/bulk-lock/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${accessToken}`
                },
                body: JSON.stringify({ form_ids: Array.from(selectedForms) })
            });

            if (response.ok) {
                alert('Forms locked successfully');
                loadFormsData();
                clearFormSelection();
            } else {
                throw new Error('Failed to lock forms');
            }
        } catch (error) {
            console.error('Error locking forms:', error);
            alert('Failed to lock forms. Please try again.');
        }
    }
};

// Bulk flag forms
const bulkFlagForms = async () => {
    if (selectedForms.size === 0) return;

    if (confirm(`Flag ${selectedForms.size} selected form(s) as invalid?`)) {
        try {
            const accessToken = getCookie('access_token');
            const response = await fetch('/api/forms/bulk-flag/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${accessToken}`
                },
                body: JSON.stringify({ form_ids: Array.from(selectedForms) })
            });

            if (response.ok) {
                alert('Forms flagged successfully');
                loadFormsData();
                clearFormSelection();
            } else {
                throw new Error('Failed to flag forms');
            }
        } catch (error) {
            console.error('Error flagging forms:', error);
            alert('Failed to flag forms. Please try again.');
        }
    }
};

// Bulk validate forms
const bulkValidateForms = async () => {
    if (selectedForms.size === 0) return;

    if (confirm(`Mark ${selectedForms.size} selected form(s) as valid?`)) {
        try {
            const accessToken = getCookie('access_token');
            const response = await fetch('/api/forms/bulk-validate/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${accessToken}`
                },
                body: JSON.stringify({ form_ids: Array.from(selectedForms) })
            });

            if (response.ok) {
                alert('Forms validated successfully');
                loadFormsData();
                clearFormSelection();
            } else {
                throw new Error('Failed to validate forms');
            }
        } catch (error) {
            console.error('Error validating forms:', error);
            alert('Failed to validate forms. Please try again.');
        }
    }
};

// Load forms data
const loadFormsData = async () => {
    try {
        const accessToken = getCookie('access_token');
        const searchQuery = document.getElementById('formsSearchInput').value;
        const statusFilter = document.getElementById('formsStatusFilter').value;
        const userFilter = document.getElementById('formsUserFilter').value;
        const dateFrom = document.getElementById('formsDateFrom').value;
        const dateTo = document.getElementById('formsDateTo').value;

        const params = new URLSearchParams({
            page: currentFormsPage,
            per_page: formsPerPage,
            search: searchQuery,
            status: statusFilter,
            user: userFilter,
            date_from: dateFrom,
            date_to: dateTo
        });

        const response = await fetch(`/api/forms/?${params}`, {
            headers: {
                'Authorization': `Bearer ${accessToken}`
            }
        });

        if (response.ok) {
            const data = await response.json();
            renderFormsTable(data.forms);
            updateFormsPagination(data.total, data.total_pages);
        } else {
            throw new Error('Failed to load forms data');
        }
    } catch (error) {
        console.error('Error loading forms data:', error);
        // Fallback to mock data
        renderFormsTable(mockData.forms || []);
    }
};

// Render forms table
const renderFormsTable = (forms) => {
    const tbody = document.getElementById('formsDataBody');
    const emptyState = document.getElementById('formsEmptyState');

    if (forms.length === 0) {
        tbody.innerHTML = '';
        emptyState.style.display = 'block';
        return;
    }

    emptyState.style.display = 'none';

    tbody.innerHTML = forms.map(form => `
        <tr>
            <td class="ps-4">
                <input type="checkbox" class="form-check-input" value="${form.id}" onchange="toggleFormSelection('${form.id}')">
            </td>
            <td class="fw-bold">${form.id}</td>
            <td>${new Date(form.submitted_at).toLocaleDateString()}</td>
            <td>${form.student_name}</td>
            <td>${form.school}</td>
            <td>
                <span class="badge ${getFormStatusBadgeClass(form.status)}">${form.status}</span>
            </td>
            <td>${form.submitted_by}</td>
            <td class="text-end pe-4">
                <div class="btn-group btn-group-sm">
                    <button class="btn btn-outline-primary btn-sm" onclick="viewForm('${form.id}')" title="View">
                        <i class="bi bi-eye"></i>
                    </button>
                    <button class="btn btn-outline-secondary btn-sm" onclick="editForm('${form.id}')" title="Edit">
                        <i class="bi bi-pencil"></i>
                    </button>
                    <div class="dropdown">
                        <button class="btn btn-outline-secondary btn-sm dropdown-toggle" type="button" data-bs-toggle="dropdown">
                            <i class="bi bi-three-dots"></i>
                        </button>
                        <ul class="dropdown-menu">
                            <li><a class="dropdown-item" href="#" onclick="lockForm('${form.id}')">Lock Form</a></li>
                            <li><a class="dropdown-item" href="#" onclick="flagForm('${form.id}')">Flag Invalid</a></li>
                            <li><a class="dropdown-item" href="#" onclick="validateForm('${form.id}')">Mark Valid</a></li>
                            <li><hr class="dropdown-divider"></li>
                            <li><a class="dropdown-item text-danger" href="#" onclick="deleteForm('${form.id}')">Delete</a></li>
                        </ul>
                    </div>
                </div>
            </td>
        </tr>
    `).join('');
};

// Get form status badge class
const getFormStatusBadgeClass = (status) => {
    switch (status) {
        case 'draft': return 'bg-secondary';
        case 'submitted': return 'bg-primary';
        case 'locked': return 'bg-danger';
        case 'flagged': return 'bg-warning';
        case 'invalid': return 'bg-danger';
        case 'validated': return 'bg-success';
        default: return 'bg-secondary';
    }
};

// Update forms pagination
const updateFormsPagination = (total, totalPages) => {
    const info = document.getElementById('formsPaginationInfo');
    const prevBtn = document.getElementById('formsPrevBtn');
    const nextBtn = document.getElementById('formsNextBtn');

    const start = (currentFormsPage - 1) * formsPerPage + 1;
    const end = Math.min(currentFormsPage * formsPerPage, total);

    info.textContent = `Showing ${start}-${end} of ${total} forms`;

    prevBtn.disabled = currentFormsPage <= 1;
    nextBtn.disabled = currentFormsPage >= totalPages;
};

// Previous forms page
const prevFormsPage = () => {
    if (currentFormsPage > 1) {
        currentFormsPage--;
        loadFormsData();
    }
};

// Next forms page
const nextFormsPage = () => {
    currentFormsPage++;
    loadFormsData();
};

// Clear forms filters
const clearFormsFilters = () => {
    document.getElementById('formsSearchInput').value = '';
    document.getElementById('formsStatusFilter').value = '';
    document.getElementById('formsUserFilter').value = '';
    document.getElementById('formsDateFrom').value = '';
    document.getElementById('formsDateTo').value = '';
    currentFormsPage = 1;
    loadFormsData();
};

// Export forms data
const exportFormsData = async () => {
    try {
        const accessToken = getCookie('access_token');
        const response = await fetch('/api/forms/export/', {
            headers: {
                'Authorization': `Bearer ${accessToken}`
            }
        });

        if (response.ok) {
            const blob = await response.blob();
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = 'forms_data.csv';
            document.body.appendChild(a);
            a.click();
            window.URL.revokeObjectURL(url);
            document.body.removeChild(a);
        } else {
            throw new Error('Failed to export data');
        }
    } catch (error) {
        console.error('Error exporting forms data:', error);
        alert('Failed to export data. Please try again.');
    }
};

// Individual form actions
const viewForm = (formId) => {
    console.log('Viewing form:', formId);
    // Implement view form logic
};

const editForm = (formId) => {
    console.log('Editing form:', formId);
    // Implement edit form logic
};

const lockForm = async (formId) => {
    if (confirm('Lock this form? This will prevent further edits.')) {
        try {
            const accessToken = getCookie('access_token');
            const response = await fetch(`/api/forms/${formId}/lock/`, {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${accessToken}`
                }
            });

            if (response.ok) {
                loadFormsData();
            } else {
                throw new Error('Failed to lock form');
            }
        } catch (error) {
            console.error('Error locking form:', error);
            alert('Failed to lock form. Please try again.');
        }
    }
};

const flagForm = async (formId) => {
    if (confirm('Flag this form as invalid?')) {
        try {
            const accessToken = getCookie('access_token');
            const response = await fetch(`/api/forms/${formId}/flag/`, {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${accessToken}`
                }
            });

            if (response.ok) {
                loadFormsData();
            } else {
                throw new Error('Failed to flag form');
            }
        } catch (error) {
            console.error('Error flagging form:', error);
            alert('Failed to flag form. Please try again.');
        }
    }
};

const validateForm = async (formId) => {
    if (confirm('Mark this form as valid?')) {
        try {
            const accessToken = getCookie('access_token');
            const response = await fetch(`/api/forms/${formId}/validate/`, {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${accessToken}`
                }
            });

            if (response.ok) {
                loadFormsData();
            } else {
                throw new Error('Failed to validate form');
            }
        } catch (error) {
            console.error('Error validating form:', error);
            alert('Failed to validate form. Please try again.');
        }
    }
};

const deleteForm = async (formId) => {
    if (confirm('Delete this form? This action cannot be undone.')) {
        try {
            const accessToken = getCookie('access_token');
            const response = await fetch(`/api/forms/${formId}/`, {
                method: 'DELETE',
                headers: {
                    'Authorization': `Bearer ${accessToken}`
                }
            });

            if (response.ok) {
                loadFormsData();
            } else {
                throw new Error('Failed to delete form');
            }
        } catch (error) {
            console.error('Error deleting form:', error);
            alert('Failed to delete form. Please try again.');
        }
    }
};

/*
=====================================================
    Initialization
=====================================================
*/
document.addEventListener('DOMContentLoaded', () => {
    // Initial population of data
    populateMetrics();
    renderStudentsTable();
    renderUsersTable();

    // Set up event listeners
    const searchInput = document.getElementById('patientSearchInput');
    if (searchInput) {
        searchInput.addEventListener('keyup', debounce(applyPatientFilters, 300));
    }

    // Forms section event listeners
    const formsSearchInput = document.getElementById('formsSearchInput');
    if (formsSearchInput) {
        formsSearchInput.addEventListener('keyup', debounce(loadFormsData, 300));
    }

    const formsStatusFilter = document.getElementById('formsStatusFilter');
    if (formsStatusFilter) {
        formsStatusFilter.addEventListener('change', () => {
            currentFormsPage = 1;
            loadFormsData();
        });
    }

    const formsUserFilter = document.getElementById('formsUserFilter');
    if (formsUserFilter) {
        formsUserFilter.addEventListener('change', () => {
            currentFormsPage = 1;
            loadFormsData();
        });
    }

    const formsDateFrom = document.getElementById('formsDateFrom');
    const formsDateTo = document.getElementById('formsDateTo');
    if (formsDateFrom && formsDateTo) {
        [formsDateFrom, formsDateTo].forEach(input => {
            input.addEventListener('change', () => {
                currentFormsPage = 1;
                loadFormsData();
            });
        });
    }

    // Set initial active section
    showSection('dashboard', document.getElementById('dashboard-nav'));
});

