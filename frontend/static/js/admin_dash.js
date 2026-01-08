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
            const response = await fetch(`${DJANGO_API_BASE_URL}/admin/users/`);
            if (!response.ok) {
                throw new Error('Failed to fetch users');
            }
            const users = await response.json();
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
            console.error('Error fetching users:', error);
            showToast('Could not load user data.', 'danger');
        }
    };

    window.handleCreateUser = async (event) => {
        event.preventDefault();
        const form = event.target;
        const formData = new FormData(form);
        const data = Object.fromEntries(formData.entries());

        try {
            const response = await fetch(`${DJANGO_API_BASE_URL}/admin/users/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    // Django's CSRF token needs to be included. Assuming it's in a cookie.
                    'X-CSRFToken': getCookie('csrftoken'),
                },
                body: JSON.stringify(data),
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.detail || 'Failed to create user');
            }

            showToast('User created successfully!', 'success');
            form.reset();
            const modal = bootstrap.Modal.getInstance(document.getElementById('addUserModal'));
            modal.hide();
            fetchUsers();
        } catch (error) {
            console.error('Error creating user:', error);
            showToast(error.message, 'danger');
        }
    };

    window.deleteUser = async (userId) => {
        if (!confirm('Are you sure you want to delete this user? This action cannot be undone.')) {
            return;
        }

        try {
            const response = await fetch(`${DJANGO_API_BASE_URL}/admin/users/${userId}/`, {
                method: 'DELETE',
                headers: {
                    'X-CSRFToken': getCookie('csrftoken'),
                },
            });

            if (!response.ok) {
                throw new Error('Failed to delete user');
            }

            showToast('User deleted successfully.', 'success');
            fetchUsers();
        } catch (error) {
            console.error('Error deleting user:', error);
            showToast(error.message, 'danger');
        }
    };
    // Placeholder for other functions to avoid breaking the UI
    ['viewUserDetails', 'editUser', 'resetUserPassword', 'deactivateUser', 'blockUser', 'forceLogoutUser'].forEach(funcName => {
        window[funcName] = (id) => {
            showToast(`Functionality for "${funcName}" with ID ${id} is not yet implemented.`, 'info');
        }
    });


    


        let currentStudentPage = 1;


        let studentSearchQuery = '';


        let studentGenderFilter = '';


        let studentSchoolFilter = '';


    


    


        const fetchStudents = async (page = 1, searchQuery = '', gender = '', school = '') => {


            try {


                const token = localStorage.getItem('access_token');


                if (!token) {


                    showToast('Authentication token not found. Please log in again.', 'danger');


                    window.location.href = '/login.html';


                    return;


                }


    


                


    


                            console.log('Fetching students...');


    


                let url = `${DJANGO_API_BASE_URL}/admin/students/?page=${page}`;


    


                            if (searchQuery) url += `&q=${searchQuery}`;


    


                            if (gender) url += `&gender=${gender}`;


    


                            if (school) url += `&school=${school}`;


    


                            console.log('API URL:', url);


                // Add from_date and to_date filters if needed in the future


    


                const response = await fetch(url, {


                    headers: {


                        'Authorization': `Bearer ${token}`


                    }


                });


    


                if (!response.ok) {


                    if (response.status === 401) {


                        showToast('Session expired. Please log in again.', 'danger');


                        window.location.href = '/login.html';


                    }


                    throw new Error('Failed to fetch students');


                }


    


                            console.log('API response status:', response.status);


    


                            const data = await response.json();


    


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


                            <td><span class="badge bg-success">Active</span></td>


                            <td>${student.last_visit || 'N/A'}</td>


                            <td class="text-end pe-4">


                                <div class="dropdown">


                                    <button class="btn btn-sm btn-outline-secondary dropdown-toggle" type="button" data-bs-toggle="dropdown">Actions</button>


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


                console.error('Error fetching students:', error);


                showToast('Could not load student data.', 'danger');


            }


        };


    


        // Pagination functions


        window.prevPatientPage = () => {


            if (currentStudentPage > 1) {


                fetchStudents(currentStudentPage - 1, studentSearchQuery, studentGenderFilter, studentSchoolFilter);


            }


        };


    


        window.nextPatientPage = () => {


            // Assuming the API provides 'next' URL or we can infer it


            // For simplicity, directly incrementing page for now,


            // but robust implementation would parse 'next' URL


            fetchStudents(currentStudentPage + 1, studentSearchQuery, studentGenderFilter, studentSchoolFilter);


        };


    


        // Search and Filter functions


        document.getElementById('patientSearchInput').addEventListener('input', debounce(function() {


            studentSearchQuery = this.value;


            fetchStudents(1, studentSearchQuery, studentGenderFilter, studentSchoolFilter);


        }, 300));


    


        document.getElementById('genderFilter').addEventListener('change', function() {


            studentGenderFilter = this.value;


            fetchStudents(1, studentSearchQuery, studentGenderFilter, studentSchoolFilter);


        });


    


        document.getElementById('schoolFilter').addEventListener('change', function() {


            studentSchoolFilter = this.value;


            fetchStudents(1, studentSearchQuery, studentGenderFilter, studentSchoolFilter);


        });


    


        window.clearPatientFilters = () => {


            document.getElementById('patientSearchInput').value = '';


            document.getElementById('genderFilter').value = '';


            document.getElementById('schoolFilter').value = '';


            studentSearchQuery = '';


            studentGenderFilter = '';


            studentSchoolFilter = '';


            fetchStudents(1);


        };


    


        window.applyPatientFilters = () => {


            // Filters are applied on change, but this button can trigger a fresh fetch if needed.


            fetchStudents(1, studentSearchQuery, studentGenderFilter, studentSchoolFilter);


        };


    


        // Placeholder for student action functions


        window.viewStudentDetails = (studentId) => {


            showToast(`Viewing details for student ID: ${studentId}`, 'info');


            // Implement navigation to a student detail page or modal


        };


    


        window.editStudent = (studentId) => {


            showToast(`Editing student ID: ${studentId}`, 'info');


            // Implement editing functionality


        };


    


        window.deleteStudent = async (studentId) => {


            if (!confirm(`Are you sure you want to delete student ${studentId}? This action cannot be undone.`)) {


                return;


            }


            try {


                const token = localStorage.getItem('access_token');


                const response = await fetch(`${DJANGO_API_BASE_URL}/admin/student/${studentId}/`, {


                    method: 'DELETE',


                    headers: {


                        'Authorization': `Bearer ${token}`,


                        'X-CSRFToken': getCookie('csrftoken'),


                    },


                });


    


                if (!response.ok) {


                    if (response.status === 401) {


                        showToast('Session expired. Please log in again.', 'danger');


                        window.location.href = '/login.html';


                    }


                    throw new Error('Failed to delete student');


                }


    


                showToast(`Student ${studentId} deleted successfully.`, 'success');


                fetchStudents(currentStudentPage, studentSearchQuery, studentGenderFilter, studentSchoolFilter); // Refresh list


            } catch (error) {


                console.error('Error deleting student:', error);


                showToast(error.message, 'danger');


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


    


        // --- User Management (existing functions, modified to add getCookie for CSRF) ---


        // ... (existing fetchUsers, handleCreateUser, deleteUser, and placeholders)


    


        // Initial load


        const init = () => {


            // Show dashboard by default


            showSection('dashboard', document.getElementById('nav-dashboard-link'));


            


            // Add event listener for students navigation link


            const navPatientsLink = document.getElementById('nav-patients-link');


            if (navPatientsLink) {


                navPatientsLink.addEventListener('click', (e) => {


                    e.preventDefault();


                    showSection('patients', navPatientsLink);


                    fetchStudents(); // Fetch students when navigating to the students section


                });


            }


        


                        // Fetch users if we are on the users page


        


                        if(document.getElementById('usersTableBody')) {


        


                            fetchUsers();


        


                        }


        


            


        


                        // Fetch students initially if the 'patients' section is active on load


        


                        if (document.getElementById('patients').classList.contains('active')) {


        


                            fetchStudents();


        


                        }


        


                    }; // Correctly closes init function


        


            


        


                    init(); // Call init


        


            


        


                }); // Correctly closes DOMContentLoaded event listener


        


            


    