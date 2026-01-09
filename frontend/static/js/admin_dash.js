document.addEventListener('DOMContentLoaded', function () {
    // Utility function to get CSRF token from cookie
    function getCookie(name) {
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

    const getStatusBadgeClass = (status) => {
        switch (status) {
            case 'active':
                return 'bg-success';
            case 'locked':
                return 'bg-danger';
            case 'flagged':
                return 'bg-warning';
            case 'inactive':
                return 'bg-secondary';
            default:
                return 'bg-primary';
        }
    };

    const showToast = (message, level = 'info') => {
        const toastContainer = document.getElementById('toast-container');
        if (!toastContainer) {
            console.error('Toast container not found');
            alert(`${level.toUpperCase()}: ${message}`);
            return;
        }

        const toast = document.createElement('div');
        toast.className = `toast align-items-center text-white bg-${level} border-0 show`;
        toast.role = 'alert';
        toast.ariaLive = 'assertive';
        toast.ariaAtomic = 'true';

        const toastBody = document.createElement('div');
        toastBody.className = 'd-flex';
        toastBody.innerHTML = `
            <div class="toast-body">
                ${message}
            </div>
            <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast" aria-label="Close"></button>
        `;
        toast.appendChild(toastBody);
        toastContainer.appendChild(toast);

        const bsToast = new bootstrap.Toast(toast);
        bsToast.show();

        toast.addEventListener('hidden.bs.toast', () => {
            toast.remove();
        });
    };

    // --- API Helper Function ---
    const makeApiRequest = async (url, options = {}) => {
        const token = localStorage.getItem('access_token');
        if (!token) {
            showToast('Authentication token not found. Please log in again.', 'danger');
            window.location.href = 'login.html';
            return;
        }

        const headers = {
            'Authorization': `Bearer ${token}`,
            'X-CSRFToken': getCookie('csrftoken'),
            ...options.headers,
        };

        const config = {
            ...options,
            headers,
        };

        try {
            const response = await fetch(url, config);

            if (!response.ok) {
                if (response.status === 401) {
                    showToast('Session expired. Please log in again.', 'danger');
                    window.location.href = 'login.html';
                }
                const errorData = await response.json();
                throw new Error(errorData.detail || `API request failed with status ${response.status}`);
            }

            return await response.json();
        } catch (error) {
            console.error('API Request Error:', error);
            showToast(error.message, 'danger');
            throw error; // Re-throw to allow specific error handling if needed
        }
    };


    // --- SPA Navigation ---
    const sections = document.querySelectorAll('.spa-section');
    const navLinks = document.querySelectorAll('#sidebar .nav-link');

    const showSection = (sectionId, clickedLink) => {
        console.log('showSection called for:', sectionId, clickedLink ? clickedLink.id : 'N/A');
        sections.forEach(section => section.classList.remove('active'));
        navLinks.forEach(link => link.classList.remove('active'));

        const targetSection = document.getElementById(sectionId);
        if (targetSection) {
            targetSection.classList.add('active');
            console.log(`Section '${sectionId}' activated.`);
            } else if (sectionId === 'patients') {
                console.log('--- showSection: Entering "patients" section, calling fetchStudents() ---');
                fetchStudents(1, studentSearchQuery, studentGenderFilter, studentSchoolFilter, studentStatusFilter);
            } else if (sectionId === 'dashboard') { // Call fetchDashboardSummary when dashboard is active
                console.log('--- showSection: Entering "dashboard" section, calling fetchDashboardSummary() ---');
                fetchDashboardSummary();
                console.log('--- showSection: Entering "dashboard" section, calling fetchRecentActivity() ---');
                fetchRecentActivity();
            } else if (sectionId === 'users') { // Call fetchUsers when users section is active
                console.log('--- showSection: Entering "users" section, calling fetchUsers() ---');
                fetchUsers();
                console.log('--- showSection: Entering "users" section, calling fetchUserSummary() ---'); // Call fetchUserSummary for user statistics
                fetchUserSummary();
            } else if (sectionId === 'forms') { // Call fetchForms when forms section is active
                console.log('--- showSection: Entering "forms" section, calling fetchForms() ---');
                fetchForms();
            } else if (sectionId === 'followups') { // Call fetchFollowups when followups section is active
                console.log('--- showSection: Entering "followups" section, calling fetchFollowups() ---');
                fetchFollowups(1, followupSearchQuery, followupClinicianFilter, followupDateFrom, followupDateTo, followupStatusFilter, followupSchoolFilter);


        } else {
            console.warn(`Section with ID '${sectionId}' not found.`);
        }
        if (clickedLink) {
            clickedLink.classList.add('active');
            console.log(`Nav link '${clickedLink.id}' activated.`);
        }
    };

    navLinks.forEach(link => {
        const sectionId = link.id.replace('nav-', '').replace('-link', '');
        if (document.getElementById(sectionId)) {
            link.addEventListener('click', (e) => {
                e.preventDefault();
                showSection(sectionId, link);
            });
        }
    });

    const DJANGO_API_BASE_URL = 'http://127.0.0.1:8000/api';

    // --- User Management ---
    const fetchUsers = async () => {
        try {
            console.log('Fetching users data...');
            const data = await makeApiRequest(`${DJANGO_API_BASE_URL}/admin/users/`);
            console.log('Fetched users data:', data);

            const users = data.results; // Extract the actual users array
            const usersTableBody = document.getElementById('usersTableBody');
            usersTableBody.innerHTML = '';
            users.forEach(user => {
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td class="ps-4"><input type="checkbox" class="user-checkbox" value="${user.id}"></td>
                    <td class="ps-4 fw-medium">${user.username}</td>
                    <td>${user.full_name}</td>
                    <td><span class="badge bg-primary bg-opacity-10 text-primary">${user.role}</span></td>
                    <td><span class="badge bg-${user.is_active ? 'success' : 'secondary'}">${user.is_active ? 'Active' : 'Inactive'}</span></td>
                    <td class="small text-muted">${new Date(user.date_joined).toLocaleDateString()}</td>
                    <td class="small text-muted">${user.last_login ? new Date(user.last_login).toLocaleString() : 'Never'}</td>
                    <td class="text-end pe-4">
                        <div class="dropdown">
                            <button class="btn btn-sm btn-outline-secondary dropdown-toggle" type="button" data-bs-toggle="dropdown">Actions</button>
                            <ul class="dropdown-menu">
                                <li><a class="dropdown-item" href="#" onclick="viewUserDetails(${user.id})"><i class="bi bi-eye me-2"></i>View Details</a></li>
                                <li><a class="dropdown-item" href="#" onclick="editUser(${user.id})"><i class="bi bi-pencil me-2"></i>Edit User</a></li>
                                <li><a class="dropdown-item" href="#" onclick="resetUserPassword(${user.id})"><i class="bi bi-key me-2"></i>Reset Password</a></li>
                                <li><hr class="dropdown-divider"></li>
                                <li><a class="dropdown-item text-warning" href="#" onclick="deactivateUser(${user.id})"><i class="bi bi-pause-circle me-2"></i>Deactivate</a></li>
                                <li><a class="dropdown-item text-danger" href="#" onclick="blockUser(${user.id})"><i class="bi bi-x-circle me-2"></i>Block Account</a></li>
                                <li><a class="dropdown-item text-danger" href="#" onclick="deleteUser(${user.id})"><i class="bi bi-trash me-2"></i>Delete User</a></li>
                                <li><a class="dropdown-item text-danger" href="#" onclick="forceLogoutUser(${user.id})"><i class="bi bi-box-arrow-right me-2"></i>Force Logout</a></li>
                            </ul>
                        </div>
                    </td>
                `;
                usersTableBody.appendChild(row);
            });
        } catch (error) {
            // makeApiRequest already handles showing toasts for API errors
            console.error('Error in fetchUsers:', error);
        }
    };

    window.handleCreateUser = async (event) => {
        event.preventDefault();
        const form = event.target;
        const formData = new FormData(form);
        const data = Object.fromEntries(formData.entries());

        try {
            // API call to create a new user
            await makeApiRequest(`${DJANGO_API_BASE_URL}/admin/users/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data),
            });

            showToast('User created successfully!', 'success');
            form.reset();
            const modal = bootstrap.Modal.getInstance(document.getElementById('addUserModal'));
            modal.hide();
            fetchUsers();
        } catch (error) {
            console.error('Error creating user:', error);
            // makeApiRequest already shows a toast, so no need to show another one here
        }
    };

    // --- User Action Implementations ---
    window.viewUserDetails = (userId) => {
        showToast(`Viewing details for user ID: ${userId}`, 'info');
        // In a real application, this would open a modal or navigate to a user detail page
    };

    window.editUser = (userId) => {
        showToast(`Editing user ID: ${userId}`, 'info');
        // In a real application, this would open a modal to edit user details
    };

    window.resetUserPassword = async (userId) => {
        if (!confirm(`Are you sure you want to reset the password for user ID: ${userId}?`)) {
            return;
        }
        try {
            await makeApiRequest(`${DJANGO_API_BASE_URL}/admin/user/${userId}/reset-password/`, {
                method: 'POST', // Or PUT, depending on API design
                headers: {
                    'Content-Type': 'application/json',
                },
                // Body might contain new password or a flag for auto-generation
                body: JSON.stringify({}) 
            });

            showToast(`Password for user ID: ${userId} reset successfully.`, 'success');
            fetchUsers(); // Refresh the user list
        } catch (error) {
            console.error('Error in resetUserPassword:', error);
            // makeApiRequest already handles showing toasts for API errors
        }
    };

    window.deactivateUser = async (userId) => {
        if (!confirm(`Are you sure you want to deactivate user ID: ${userId}?`)) {
            return;
        }
        try {
            await makeApiRequest(`${DJANGO_API_BASE_URL}/admin/users/${userId}/`, {
                method: 'PATCH', // Assuming PATCH for partial update (setting is_active to false)
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ is_active: false })
            });

            showToast(`User ID: ${userId} deactivated successfully.`, 'success');
            fetchUsers(); // Refresh the user list
            fetchUserSummary(); // Refresh user summary statistics
        } catch (error) {
            console.error('Error in deactivateUser:', error);
            // makeApiRequest already handles showing toasts for API errors
        }
    };

    window.blockUser = async (userId) => {
        if (!confirm(`Are you sure you want to block user ID: ${userId}? This will prevent them from logging in.`)) {
            return;
        }
        try {
            await makeApiRequest(`${DJANGO_API_BASE_URL}/admin/users/${userId}/`, {
                method: 'PATCH', // Assuming PATCH for partial update (setting is_blocked to true)
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ is_blocked: true }) // Assuming an 'is_blocked' field
            });

            showToast(`User ID: ${userId} blocked successfully.`, 'success');
            fetchUsers(); // Refresh the user list
            fetchUserSummary(); // Refresh user summary statistics
        } catch (error) {
            console.error('Error in blockUser:', error);
            // makeApiRequest already handles showing toasts for API errors
        }
    };

    window.forceLogoutUser = async (userId) => {
        if (!confirm(`Are you sure you want to force logout user ID: ${userId}? This will invalidate all their active sessions.`)) {
            return;
        }
        try {
            await makeApiRequest(`${DJANGO_API_BASE_URL}/admin/user/${userId}/force-logout/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({})
            });

            showToast(`User ID: ${userId} force logged out successfully.`, 'success');
        } catch (error) {
            console.error('Error in forceLogoutUser:', error);
            // makeApiRequest already handles showing toasts for API errors
        }
    };

    window.deleteUser = async (userId) => {
        if (!confirm('Are you sure you want to delete this user? This action cannot be undone.')) {
            return;
        }

        try {
            await makeApiRequest(`${DJANGO_API_BASE_URL}/admin/users/${userId}/`, {
                method: 'DELETE',
            });

            showToast('User deleted successfully!', 'success');
            fetchUsers();
        } catch (error) {
            console.error('Error in deleteUser:', error);
            // makeApiRequest already handles showing toasts for API errors
        }
    };
    



    


    // API call to fetch dashboard summary data
    const fetchDashboardSummary = async () => {
        try {
            console.log('Fetching dashboard summary...');
            const summaryData = await makeApiRequest(`${DJANGO_API_BASE_URL}/admin/overview/`);
            console.log('Fetched dashboard summary data:', summaryData);

            // Update DOM elements with fetched data
            document.getElementById('totalUsers').textContent = summaryData.total_users || '0';
            document.getElementById('totalStudents').textContent = summaryData.total_students || '0';
            document.getElementById('activeClinicians').textContent = summaryData.active_users_today || '0';
            document.getElementById('formsSubmittedToday').textContent = summaryData.forms_submitted_today || '0';

        } catch (error) {
            console.error('Error in fetchDashboardSummary:', error);
            // makeApiRequest already handles showing toasts for API errors
        }
    };

    // API call to fetch user statistics for User & Admin section
    const fetchUserSummary = async () => {
        try {
            console.log('Fetching user summary...');
            const userSummaryData = await makeApiRequest(`${DJANGO_API_BASE_URL}/admin/users/summary/`);
            console.log('Fetched user summary data:', userSummaryData);

            // Update DOM elements with fetched data
            document.getElementById('totalUsersCount').textContent = userSummaryData.total_users || '0';
            document.getElementById('activeUsersCount').textContent = userSummaryData.active_users || '0';
            document.getElementById('inactiveUsersCount').textContent = userSummaryData.inactive_users || '0';
            document.getElementById('blockedUsersCount').textContent = userSummaryData.blocked_users || '0';

        } catch (error) {
            console.error('Error in fetchUserSummary:', error);
            // makeApiRequest already handles showing toasts for API errors
        }
    };

    const fetchRecentActivity = async () => {
        try {
            console.log('Fetching recent activity...');
            const activities = await makeApiRequest(`${DJANGO_API_BASE_URL}/admin/recent-activity/`);
            console.log('Fetched recent activity data:', activities);

            const recentActivityBody = document.getElementById('recentActivityBody');
            recentActivityBody.innerHTML = '';

            if (activities.length === 0) {
                recentActivityBody.innerHTML = `<tr><td colspan="6" class="text-center py-4 text-muted">No recent activity found.</td></tr>`;
            } else {
                activities.forEach(activity => {
                    const row = document.createElement('tr');
                    const activityType = activity.type || 'N/A';
                    let badgeClass = 'bg-info';
                    let iconClass = 'bi-info-circle';

                    if (activityType.includes('Created')) {
                        badgeClass = 'bg-success';
                        iconClass = 'bi-person-plus-fill';
                    } else if (activityType.includes('Submitted')) {
                        badgeClass = 'bg-primary';
                        iconClass = 'bi-file-earmark-check-fill';
                    } else if (activityType.includes('Updated')) {
                        badgeClass = 'bg-warning';
                        iconClass = 'bi-pencil-square';
                    }

                    row.innerHTML = `
                        <td class="ps-4">
                            <div class="badge ${badgeClass} bg-opacity-75">
                                <i class="bi ${iconClass}"></i>
                            </div>
                        </td>
                        <td class="small text-muted">${new Date(activity.timestamp).toLocaleString()}</td>
                        <td class="fw-medium">${activity.user}</td>
                        <td class="fw-medium">${activity.type}</td>
                        <td class="small text-muted">${activity.details}</td>
                        <td class="text-end pe-4">
                            <span class="badge bg-success">${activity.status}</span>
                        </td>
                    `;
                    recentActivityBody.appendChild(row);
                });
            }
        } catch (error) {
            console.error('Error in fetchRecentActivity:', error);
        }
    };


        let currentStudentPage = 1;
        let studentSearchQuery = '';
        let studentGenderFilter = '';
        let studentSchoolFilter = '';
        let studentStatusFilter = '';

        let currentFollowupPage = 1;
        let followupSearchQuery = '';
        let followupClinicianFilter = '';
        let followupDateFrom = '';
        let followupDateTo = '';
        let followupStatusFilter = '';
        let followupSchoolFilter = '';



        const fetchStudents = async (page = 1, searchQuery = '', gender = '', school = '', status = '') => {
            try {
                console.log('Fetching students...');

                let url = `${DJANGO_API_BASE_URL}/admin/students/?page=${page}`;
                if (searchQuery) url += `&q=${searchQuery}`;
                if (gender) url += `&gender=${gender}`;
                if (school) url += `&school=${school}`;
                if (status) url += `&status=${status}`;

                console.log('API URL:', url);
                
                const data = await makeApiRequest(url);

                console.log('Fetched student data:', data);

                const students = data.results;
                const studentsTableBody = document.getElementById('studentsTableBody');
                studentsTableBody.innerHTML = ''; // Clear existing rows

                if (students.length === 0) {
                    studentsTableBody.innerHTML = `<tr><td colspan="9" class="text-center py-4 text-muted">No student data found.</td></tr>`;
                } else {
                    students.forEach(student => {
                        const row = document.createElement('tr');
                        row.innerHTML = `
                            <td class="ps-4"><input type="checkbox" class="student-checkbox" value="${student.student_id}"></td>
                            <td class="ps-4 fw-medium">${student.student_id}</td>
                            <td>${student.name}</td>
                            <td>${student.school_name || 'N/A'}</td>
                            <td>${student.age} / ${student.gender}</td>
                            <td>${new Date(student.created_at).toLocaleDateString()}</td>
                            <td><span class="badge ${getStatusBadgeClass(student.status)}">${student.status || 'Active'}</span></td>
                            <td>${student.last_visit ? new Date(student.last_visit).toLocaleDateString() : 'N/A'}</td>
                            <td class="text-end pe-4">
                                <div class="dropdown">
                                    <button class="btn btn-sm btn-icon btn-light" type="button" data-bs-toggle="dropdown">
                                        <i class="bi bi-three-dots-vertical"></i>
                                    </button>
                                    <ul class="dropdown-menu">
                                        <li><a class="dropdown-item" href="#" onclick="viewStudentDetails('${student.student_id}')"><i class="bi bi-eye me-2"></i>View Details</a></li>
                                        <li><a class="dropdown-item" href="#" onclick="editStudent('${student.student_id}')"><i class="bi bi-pencil me-2"></i>Edit Student</a></li>
                                        <li><a class="dropdown-item text-danger" href="#" onclick="deleteStudent('${student.student_id}')"><i class="bi bi-trash me-2"></i>Delete Student</a></li>
                                    </ul>
                                </div>
                            </td>
                        `;
                        studentsTableBody.appendChild(row);
                    });
                }

                // Update pagination info
                document.getElementById('patientPaginationInfo').textContent =
                    `Showing ${data.count > 0 ? (page - 1) * data.page_size + 1 : 0}-${Math.min(page * data.page_size, data.count)} of ${data.count} entries`;

                // Update pagination buttons
                document.getElementById('patientPrevBtn').disabled = !data.previous;
                document.getElementById('patientNextBtn').disabled = !data.next;

                currentStudentPage = page;

            } catch (error) {
                console.error('Error in fetchStudents:', error);
                // makeApiRequest already handles showing toasts for API errors
            }
        };

        // Pagination functions
        window.prevPatientPage = () => {
            if (currentStudentPage > 1) {
                fetchStudents(currentStudentPage - 1, studentSearchQuery, studentGenderFilter, studentSchoolFilter, studentStatusFilter);
            }
        };

        window.nextPatientPage = () => {
            fetchStudents(currentStudentPage + 1, studentSearchQuery, studentGenderFilter, studentSchoolFilter, studentStatusFilter);
        };

        // Search and Filter functions
        document.getElementById('patientSearchInput').addEventListener('input', debounce(function() {
            studentSearchQuery = this.value;
            fetchStudents(1, studentSearchQuery, studentGenderFilter, studentSchoolFilter, studentStatusFilter);
        }, 300));

        document.getElementById('genderFilter').addEventListener('change', function() {
            studentGenderFilter = this.value;
            fetchStudents(1, studentSearchQuery, studentGenderFilter, studentSchoolFilter, studentStatusFilter);
        });

        document.getElementById('schoolFilter').addEventListener('change', function() {
            studentSchoolFilter = this.value;
            fetchStudents(1, studentSearchQuery, studentGenderFilter, studentSchoolFilter, studentStatusFilter);
        });

        document.getElementById('statusFilter').addEventListener('change', function() {
            studentStatusFilter = this.value;
            fetchStudents(1, studentSearchQuery, studentGenderFilter, studentSchoolFilter, studentStatusFilter);
        });

        window.clearPatientFilters = () => {
            document.getElementById('patientSearchInput').value = '';
            document.getElementById('genderFilter').value = '';
            document.getElementById('schoolFilter').value = '';
            document.getElementById('statusFilter').value = '';
            studentSearchQuery = '';
            studentGenderFilter = '';
            studentSchoolFilter = '';
            studentStatusFilter = '';
            fetchStudents(1);
        };

        window.applyPatientFilters = () => {
            fetchStudents(1, studentSearchQuery, studentGenderFilter, studentSchoolFilter, studentStatusFilter);
        };

        window.showFlaggedStudents = () => {
            document.getElementById('statusFilter').value = 'flagged';
            studentStatusFilter = 'flagged';
            fetchStudents(1, studentSearchQuery, studentGenderFilter, studentSchoolFilter, studentStatusFilter);
        };

        window.showLockedStudents = () => {
            document.getElementById('statusFilter').value = 'locked';
            studentStatusFilter = 'locked';
            fetchStudents(1, studentSearchQuery, studentGenderFilter, studentSchoolFilter, studentStatusFilter);
        };

        // Search and Filter functions for Follow-Ups
        document.getElementById('followupSearchInput').addEventListener('input', debounce(function() {
            followupSearchQuery = this.value;
            fetchFollowups(1, followupSearchQuery, followupClinicianFilter, followupDateFrom, followupDateTo, followupStatusFilter, followupSchoolFilter);
        }, 300));

        document.getElementById('followupClinicianFilter').addEventListener('change', function() {
            followupClinicianFilter = this.value;
            fetchFollowups(1, followupSearchQuery, followupClinicianFilter, followupDateFrom, followupDateTo, followupStatusFilter, followupSchoolFilter);
        });

        document.getElementById('followupDateFromFilter').addEventListener('change', function() {
            followupDateFrom = this.value;
            fetchFollowups(1, followupSearchQuery, followupClinicianFilter, followupDateFrom, followupDateTo, followupStatusFilter, followupSchoolFilter);
        });

        document.getElementById('followupDateToFilter').addEventListener('change', function() {
            followupDateTo = this.value;
            fetchFollowups(1, followupSearchQuery, followupClinicianFilter, followupDateFrom, followupDateTo, followupStatusFilter, followupSchoolFilter);
        });

        document.getElementById('followupStatusFilter').addEventListener('change', function() {
            followupStatusFilter = this.value;
            fetchFollowups(1, followupSearchQuery, followupClinicianFilter, followupDateFrom, followupDateTo, followupStatusFilter, followupSchoolFilter);
        });

        document.getElementById('followupSchoolFilter').addEventListener('change', function() { // Assuming this filter exists in HTML
            followupSchoolFilter = this.value;
            fetchFollowups(1, followupSearchQuery, followupClinicianFilter, followupDateFrom, followupDateTo, followupStatusFilter, followupSchoolFilter);
        });

        window.clearFollowupFilters = () => {
            document.getElementById('followupSearchInput').value = '';
            document.getElementById('followupClinicianFilter').value = '';
            document.getElementById('followupDateFromFilter').value = '';
            document.getElementById('followupDateToFilter').value = '';
            document.getElementById('followupStatusFilter').value = '';
            document.getElementById('followupSchoolFilter').value = '';
            followupSearchQuery = '';
            followupClinicianFilter = '';
            followupDateFrom = '';
            followupDateTo = '';
            followupStatusFilter = '';
            followupSchoolFilter = '';
            fetchFollowups(1);
        };


        window.deleteStudent = async (studentId) => {
            if (!confirm(`Are you sure you want to delete student ${studentId}? This action cannot be undone.`)) {
                return;
            }
            try {
                await makeApiRequest(`${DJANGO_API_BASE_URL}/admin/students/${studentId}/`, {
                    method: 'DELETE',
                });
                showToast(`Student ${studentId} deleted successfully.`, 'success');
                fetchStudents(currentStudentPage, studentSearchQuery, studentGenderFilter, studentSchoolFilter, studentStatusFilter); // Refresh list
            } catch (error) {
                console.error('Error in deleteStudent:', error);
                // makeApiRequest already handles showing toasts for API errors
            }
        };


    


        // --- Forms Management ---


        let currentFormsPage = 1;


        let formsSearchQuery = '';


        let formsStatusFilter = '';


        let formsUserFilter = '';


        let formsDateFrom = '';


        let formsDateTo = '';


    


        const fetchForms = async (page = 1, searchQuery = '', status = '', user = '', dateFrom = '', dateTo = '') => {


            try {


                console.log('Fetching forms...');


    


                let url = `${DJANGO_API_BASE_URL}/admin/forms/?page=${page}`;


                if (searchQuery) url += `&q=${searchQuery}`;


                if (status) url += `&status=${status}`;


                if (user) url += `&user=${user}`;


                if (dateFrom) url += `&from_date=${dateFrom}`;


                if (dateTo) url += `&to_date=${dateTo}`;


    


                console.log('API URL for forms:', url);


    


                const data = await makeApiRequest(url);


    


                console.log('Fetched forms data:', data);


    


                const forms = data.results;


                const formsDataBody = document.getElementById('formsDataBody');


                formsDataBody.innerHTML = '';


                const formsEmptyState = document.getElementById('formsEmptyState');


    


                if (forms.length === 0) {


                    formsEmptyState.style.display = 'block';


                } else {


                    formsEmptyState.style.display = 'none';


                    forms.forEach(form => {


                        const row = document.createElement('tr');


                        row.innerHTML = `


                            <td class="ps-4"><input type="checkbox" class="form-check-input forms-checkbox" value="${form.id}"></td>


                            <td>${form.id}</td>


                            <td>${new Date(form.date_submitted).toLocaleDateString()}</td>


                            <td>${form.student_name || 'N/A'}</td>


                            <td>${form.school_name || 'N/A'}</td>


                            <td><span class="badge bg-secondary">${form.status}</span></td>


                            <td>${form.submitted_by_username || 'N/A'}</td>


                            <td class="text-end pe-4">


                                <button class="btn btn-sm btn-outline-info" onclick="viewFormDetails('${form.id}')">


                                    <i class="bi bi-eye"></i> View


                                </button>


                                <button class="btn btn-sm btn-outline-danger" onclick="deleteForm('${form.id}')">


                                    <i class="bi bi-trash"></i> Delete


                                </button>


                            </td>


                        `;


                        formsDataBody.appendChild(row);


                    });


                }


    


                // Update pagination info


                document.getElementById('formsPaginationInfo').textContent =


                    `Showing ${data.count > 0 ? (page - 1) * data.page_size + 1 : 0}-${Math.min(page * data.page_size, data.count)} of ${data.count} forms`;


    


                // Update pagination buttons


                document.getElementById('formsPrevBtn').disabled = !data.previous;


                document.getElementById('formsNextBtn').disabled = !data.next;


    


                            currentFormsPage = page;


    


                


    


                


    


                            } catch (error) {


    


                


    


                


    


                                console.error('Error in fetchForms:', error);


    


                


    


                


    


                                // makeApiRequest already handles showing toasts for API errors


    


                


    


                


    


                            }


    


                


    


                


    


                        };


    


                


    


                


    


                        // Pagination functions for forms


    


                


    


                


    


                        window.prevFormsPage = () => {


    


                


    


                


    


                            if (currentFormsPage > 1) {


    


                


    


                


    


                                fetchForms(currentFormsPage - 1, formsSearchQuery, formsStatusFilter, formsUserFilter, formsDateFrom, formsDateTo);


    


                


    


                


    


                            }


    


                


    


                


    


                        };


    


                


    


                


    


                        window.nextFormsPage = () => {


    


                


    


                


    


                            fetchForms(currentFormsPage + 1, formsSearchQuery, formsStatusFilter, formsUserFilter, formsDateFrom, formsDateTo);


    


                


    


                


    


                        };


    


                


    


                


    


                        // Search and Filter event listeners for forms


    


                


    


                


    


                        document.getElementById('formsSearchInput').addEventListener('input', debounce(function() {


    


                


    


                


    


                            formsSearchQuery = this.value;


    


                


    


                


    


                            fetchForms(1, formsSearchQuery, formsStatusFilter, formsUserFilter, formsDateFrom, formsDateTo);


    


                


    


                


    


                        }, 300));


    


                


    


                


    


                        document.getElementById('formsStatusFilter').addEventListener('change', function() {


    


                


    


                


    


                            formsStatusFilter = this.value;


    


                


    


                


    


                            fetchForms(1, formsSearchQuery, formsStatusFilter, formsUserFilter, formsDateFrom, formsDateTo);


    


                


    


                


    


                        });


    


                


    


                


    


                        document.getElementById('formsUserFilter').addEventListener('change', function() {


    


                


    


                


    


                            formsUserFilter = this.value; // This would need to be populated dynamically with users


    


                


    


                


    


                            fetchForms(1, formsSearchQuery, formsStatusFilter, formsUserFilter, formsDateFrom, formsDateTo);


    


                


    


                


    


                        });


    


                


    


                


    


                        document.getElementById('formsDateFrom').addEventListener('change', function() {


    


                


    


                


    


                            formsDateFrom = this.value;


    


                


    


                


    


                            fetchForms(1, formsSearchQuery, formsStatusFilter, formsUserFilter, formsDateFrom, formsDateTo);


    


                


    


                


    


                        });


    


                


    


                


    


                        document.getElementById('formsDateTo').addEventListener('change', function() {


    


                


    


                


    


                            formsDateTo = this.value;


    


                


    


                


    


                            fetchForms(1, formsSearchQuery, formsStatusFilter, formsUserFilter, formsDateFrom, formsDateTo);


    


                


    


                


    


                        });


    


                


    


                


    


                                window.clearFormsFilters = () => {


    


                


    


                


    


                                    document.getElementById('formsSearchInput').value = '';


    


                


    


                


    


                                    document.getElementById('formsStatusFilter').value = '';


    


                


    


                


    


                                    document.getElementById('formsUserFilter').value = '';


    


                


    


                


    


                                    document.getElementById('formsDateFrom').value = '';


    


                


    


                


    


                                    document.getElementById('formsDateTo').value = '';


    


                


    


                


    


                                    formsSearchQuery = '';


    


                


    


                


    


                                    formsStatusFilter = '';


    


                


    


                


    


                                    formsUserFilter = '';


    


                


    


                


    


                                    formsDateFrom = '';


    


                


    


                


    


                                    formsDateTo = '';


    


                


    


                


    


                                    fetchForms(1);


    


                


    


                


    


                                };


    


                


    


                


    


                        


    


                


    


                


    


                                // --- Follow-up Management ---


    


                


    


                


    


                                const fetchFollowups = async (page = 1, searchQuery = '', clinician = '', dateFrom = '', dateTo = '', status = '', school = '') => {


    


                


    


                


    


                                    try {


    


                


    


                


    


                                        console.log('Fetching follow-ups...');


    


                


    


                


    


                                        let url = `${DJANGO_API_BASE_URL}/admin/followups/?page=${page}`;


    


                


    


                


    


                                        if (searchQuery) url += `&q=${searchQuery}`;


    


                


    


                


    


                                        if (clinician) url += `&clinician=${clinician}`;


    


                


    


                


    


                                        if (dateFrom) url += `&from_date=${dateFrom}`;


    


                


    


                


    


                                        if (dateTo) url += `&to_date=${dateTo}`;


    


                


    


                


    


                                        if (status) url += `&status=${status}`;


    


                


    


                


    


                                        if (school) url += `&school=${school}`; // Assuming API supports school filter for followups


    


                


    


                


    


                        


    


                


    


                


    


                                        console.log('API URL for followups:', url);


    


                


    


                


    


                                        


    


                


    


                


    


                                        const data = await makeApiRequest(url);


    


                


    


                


    


                                        console.log('Fetched followup data:', data);


    


                


    


                


    


                        


    


                


    


                


    


                                        const followups = data.results;


    


                


    


                


    


                                        const followupsTableBody = document.querySelector('#followupsTable tbody');


    


                


    


                


    


                                        followupsTableBody.innerHTML = ''; // Clear existing rows


    


                


    


                


    


                        


    


                


    


                


    


                                        if (followups.length === 0) {


    


                


    


                


    


                                            followupsTableBody.innerHTML = `<tr><td colspan="6" class="text-center py-4 text-muted">No follow-up data found.</td></tr>`;


    


                


    


                


    


                                        } else {


    


                


    


                


    


                                            followups.forEach(followup => {


    


                


    


                


    


                                                const row = document.createElement('tr');


    


                


    


                


    


                                                row.innerHTML = `


    


                


    


                


    


                                                    <td class="ps-4">${followup.id}</td>


    


                


    


                


    


                                                    <td>${followup.student_name || 'N/A'}</td>


    


                


    


                


    


                                                    <td>${followup.school_name || 'N/A'}</td>


    


                


    


                


    


                                                    <td>${new Date(followup.last_visit_date).toLocaleDateString()}</td>


    


                


    


                


    


                                                    <td><span class="badge ${getStatusBadgeClass(followup.status)}">${followup.status || 'Scheduled'}</span></td>


    


                


    


                


    


                                                    <td class="text-end pe-4">


    


                


    


                


    


                                                        <div class="dropdown">


    


                


    


                


    


                                                            <button class="btn btn-sm btn-icon btn-light" type="button" data-bs-toggle="dropdown">


    


                


    


                


    


                                                                <i class="bi bi-three-dots-vertical"></i>


    


                


    


                


    


                                                            </button>


    


                


    


                


    


                                                            <ul class="dropdown-menu">


    


                


    


                


    


                                                                <li><a class="dropdown-item" href="#" onclick="viewFollowupDetails(${followup.id})"><i class="bi bi-eye me-2"></i>View Details</a></li>


    


                


    


                


    


                                                                <li><a class="dropdown-item" href="#" onclick="editFollowup(${followup.id})"><i class="bi bi-pencil me-2"></i>Edit Follow-up</a></li>


    


                


    


                


    


                                                                <li><a class="dropdown-item text-danger" href="#" onclick="deleteFollowup(${followup.id})"><i class="bi bi-trash me-2"></i>Delete Follow-up</a></li>


    


                


    


                


    


                                                            </ul>


    


                


    


                


    


                                                        </div>


    


                


    


                


    


                                                    </td>


    


                


    


                


    


                                                `;


    


                


    


                


    


                                                followupsTableBody.appendChild(row);


    


                


    


                


    


                                            });


    


                


    


                


    


                                        }


    


                


    


                


    


                        


    


                


    


                


    


                                        // Update pagination info


    


                


    


                


    


                                        document.getElementById('followupPaginationInfo').textContent =


    


                


    


                


    


                                            `Showing ${data.count > 0 ? (page - 1) * data.page_size + 1 : 0}-${Math.min(page * data.page_size, data.count)} of ${data.count} follow-ups`;


    


                


    


                


    


                        


    


                


    


                


    


                                        // Update pagination buttons


    


                


    


                


    


                                        document.getElementById('followupPrevBtn').disabled = !data.previous;


    


                


    


                


    


                                        document.getElementById('followupNextBtn').disabled = !data.next;


    


                


    


                


    


                        


    


                


    


                


    


                                        currentFollowupPage = page;


    


                


    


                


    


                        


    


                


    


                


    


                                    } catch (error) {


    


                


    


                


    


                                        console.error('Error in fetchFollowups:', error);


    


                


    


                


    


                                    }


    


                


    


                


    


                                };


    


                


    


                


    


                        


    


                


    


                


    


                                window.prevFollowupPage = () => {


    


                


    


                


    


                                    if (currentFollowupPage > 1) {


    


                


    


                


    


                                        fetchFollowups(currentFollowupPage - 1, followupSearchQuery, followupClinicianFilter, followupDateFrom, followupDateTo, followupStatusFilter, followupSchoolFilter);


    


                


    


                


    


                                    }


    


                


    


                


    


                                };


    


                


    


                


    


                        


    


                


    


                


    


                                window.nextFollowupPage = () => {


    


                


    


                


    


                                    fetchFollowups(currentFollowupPage + 1, followupSearchQuery, followupClinicianFilter, followupDateFrom, followupDateTo, followupStatusFilter, followupSchoolFilter);


    


                


    


                


    


                                };


    


                


    


                


    


                        


    


                


    


                


    


                                window.applyFollowupFilters = () => {


    


                


    


                


    


                                    // Re-fetch filters from DOM elements in admin_dash.html before applying


    


                


    


                


    


                                    followupSearchQuery = document.getElementById('followupSearchInput').value;


    


                


    


                


    


                                    followupClinicianFilter = document.getElementById('followupClinicianFilter').value;


    


                


    


                


    


                                    // Assuming date and status filters are also present and their values can be retrieved


    


                


    


                


    


                                    // For now, these are not directly in the new HTML, but if added, would be fetched here


    


                


    


                


    


                                    // followupDateFrom = document.getElementById('followupDateFromFilter').value;


    


                


    


                


    


                                    // followupDateTo = document.getElementById('followupDateToFilter').value;


    


                


    


                


    


                                    // followupStatusFilter = document.getElementById('followupStatusFilter').value;


    


                


    


                


    


                                    // followupSchoolFilter = document.getElementById('followupSchoolFilter').value;


    


                


    


                


    


                        


    


                


    


                


    


                                    fetchFollowups(1, followupSearchQuery, followupClinicianFilter, followupDateFrom, followupDateTo, followupStatusFilter, followupSchoolFilter);


    


                


    


                


    


                                };


    


                


    


                


    


                        


    


                


    


                


    


                                window.openNewFollowup = () => {


    


                


    


                


    


                                    // Logic to open the new follow-up modal


    


                


    


                


    


                                    const followupModal = new bootstrap.Modal(document.getElementById('followupModal'));


    


                


    


                


    


                                    followupModal.show();


    


                


    


                


    


                                    console.log('Opening new follow-up form');


    


                


    


                


    


                                };


    


                


    


                


    


                        


    


                


    


                


    


                                window.viewFollowupDetails = (followupId) => {


    


                


    


                


    


                                    showToast(`Viewing details for follow-up ID: ${followupId}`, 'info');


    


                


    


                


    


                                    // Implement fetching and displaying details in a modal or new view


    


                


    


                


    


                                };


    


                


    


                


    


                        


    


                


    


                


    


                                window.editFollowup = (followupId) => {


    


                


    


                


    


                                    showToast(`Editing follow-up ID: ${followupId}`, 'info');


    


                


    


                


    


                                    // Implement fetching data and populating edit modal


    


                


    


                


    


                                };


    


                


    


                


    


                        


    


                


    


                


    


                                window.deleteFollowup = async (followupId) => {


    


                


    


                


    


                                    if (!confirm(`Are you sure you want to delete follow-up ${followupId}? This action cannot be undone.`)) {


    


                


    


                


    


                                        return;


    


                


    


                


    


                                    }


    


                


    


                


    


                                    try {


    


                


    


                


    


                                        await makeApiRequest(`${DJANGO_API_BASE_URL}/admin/followups/${followupId}/`, {


    


                


    


                


    


                                            method: 'DELETE',


    


                


    


                


    


                                        });


    


                


    


                


    


                                        showToast(`Follow-up ${followupId} deleted successfully.`, 'success');


    


                


    


                


    


                                        fetchFollowups(currentFollowupPage, followupSearchQuery, followupClinicianFilter, followupDateFrom, followupDateTo, followupStatusFilter, followupSchoolFilter);


    


                


    


                


    


                                    } catch (error) {


    


                


    


                


    


                                        console.error('Error in deleteFollowup:', error);


    


                


    


                


    


                                    }


    


                


    


                


    


                                };


    


                


    


                


    


                        // Placeholder for forms action functions


    


                


    


                


    


                        window.viewFormDetails = (formId) => {


    


                


    


                


    


                            showToast(`Viewing details for form ID: ${formId}`, 'info');


    


                


    


                


    


                            // Implement navigation to a form detail page or modal


    


                


    


                


    


                        };


    


                


    


                


    


                        window.deleteForm = async (formId) => {


    


                


    


                


    


                            if (!confirm(`Are you sure you want to delete form ${formId}? This action cannot be undone.`)) {


    


                


    


                


    


                                return;


    


                


    


                


    


                            }


    


                


    


                


    


                            try {


    


                


    


                


    


                                await makeApiRequest(`${DJANGO_API_BASE_URL}/admin/forms/${formId}/`, {


    


                


    


                


    


                                    method: 'DELETE',


    


                


    


                


    


                                });


    


                


    


                


    


                                showToast(`Form ${formId} deleted successfully.`, 'success');


    


                


    


                


    


                                fetchForms(currentFormsPage, formsSearchQuery, formsStatusFilter, formsUserFilter, formsDateFrom, formsDateTo);


    


                


    


                


    


                            } catch (error) {


    


                


    


                


    


                                console.error('Error in deleteForm:', error);


    


                


    


                


    


                                // makeApiRequest already handles showing toasts for API errors


    


                


    


                


    


                            }


    


                


    


                


    


                        };


    


                


    


                        


    
        // Debounce utility function
        function debounce(func, delay) {
            let timeout;
            return function(...args) {
                const context = this;
                clearTimeout(timeout);
                timeout = setTimeout(() => func.apply(context, args), delay);
            };
        }

    // --- Sidebar Toggle Functionality ---
    const sidebar = document.getElementById('sidebar');
    const mobileToggle = document.getElementById('mobileSidebarToggle');
    const desktopToggle = document.getElementById('desktopSidebarToggle');
    const closeBtn = document.querySelector('.btn-close-sidebar');
    const overlay = document.querySelector('.sidebar-overlay');

    const openSidebar = () => {
        sidebar.classList.add('show');
        overlay.classList.add('show');
    };

    const closeSidebar = () => {
        sidebar.classList.remove('show');
        overlay.classList.remove('show');
    };

    if (mobileToggle) {
        mobileToggle.addEventListener('click', openSidebar);
    }

    if (desktopToggle) {
        desktopToggle.addEventListener('click', openSidebar);
    }

    if (closeBtn) {
        closeBtn.addEventListener('click', closeSidebar);
    }

    if (overlay) {
        overlay.addEventListener('click', closeSidebar);
    }

    // Initial load
    const init = () => {
        // Show dashboard by default
        showSection('dashboard', document.getElementById('nav-dashboard-link'));
    }; // Correctly closes init function

            init(); // Call init
    
            // Event listener for when the 'Follow-Ups' tab is shown
                                
                    // Event listener for when the 'Reports / Export' tab is shown
                    const reportsExportTabTrigger = document.getElementById('reports-export-tab');
                    if (reportsExportTabTrigger) {
                        reportsExportTabTrigger.addEventListener('shown.bs.tab', event => {
                            console.log('Reports / Export tab shown.');
                            // Add any specific initialization or data loading for reports here if needed
                            // For example, if there's a dynamic list of reports to load
                        });
                    }
                
                    const logout = () => {        localStorage.removeItem('access_token');
        window.location.href = 'login.html';
    };

    document.getElementById('logout-button').addEventListener('click', logout);
    document.getElementById('logout-link').addEventListener('click', logout);

});   // Correctly closes DOMContentLoaded event listener