document.addEventListener('DOMContentLoaded', function () {
    // --- UTILITY & API FUNCTIONS ---
    const API_BASE_URL = 'http://127.0.0.1:8000/api';

    const showToast = (message, level = 'error', duration = 3000) => {
        // A real app would have a more sophisticated toast system.
        alert(`${level.toUpperCase()}: ${message}`);
    };

    const apiRequest = async (endpoint, options = {}) => {
        const token = localStorage.getItem('accessToken');
        if (!token) {
            window.location.href = '/login.html';
            return;
        }
        const headers = {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`,
            ...options.headers,
        };
        try {
            const response = await fetch(`${API_BASE_URL}${endpoint}`, { ...options, headers });
            if (response.status === 401) {
                localStorage.removeItem('accessToken');
                showToast('Session expired. Please log in again.');
                window.location.href = '/login.html';
                return;
            }
            if (!response.ok) {
                const errorData = await response.json().catch(() => ({ detail: 'An unknown API error occurred.' }));
                throw new Error(errorData.detail || `HTTP error! Status: ${response.status}`);
            }
            if (response.status === 204) return null;
            return await response.json();
        } catch (error) {
            console.error('API Request Failed:', error);
            showToast(error.message);
            throw error;
        }
    };

    // --- SPA NAVIGATION ---
    const sections = document.querySelectorAll('.spa-section');
    const navLinks = document.querySelectorAll('#sidebar .nav-link');
    const showSection = async (sectionId, clickedLink) => {
        sections.forEach(section => section.classList.remove('active'));
        navLinks.forEach(link => link.classList.remove('active'));
        const targetSection = document.getElementById(sectionId);
        if (targetSection) targetSection.classList.add('active');
        if (clickedLink) clickedLink.classList.add('active');

        try {
            if (sectionId === 'dashboard') await renderDashboard();
            else if (sectionId === 'patients') await renderStudents();
            else if (sectionId === 'followups') await renderFollowups();
        } catch (error) { /* Handled by apiRequest */ }
    };

    // --- RENDERING LOGIC ---
    const renderDashboard = async () => { /* ... (implementation from previous step) ... */ };
    const renderStudents = async () => { /* ... (implementation from previous step) ... */ };
    const renderFollowups = async () => {
        const followupData = await apiRequest('/user/followups/');
        const followupBody = document.getElementById('followupsTable')?.querySelector('tbody');
        if (followupData && followupBody) {
            if (followupData.length === 0) {
                followupBody.innerHTML = `<tr><td colspan="6" class="text-center text-muted py-5">No follow-ups scheduled.</td></tr>`;
            } else {
                followupBody.innerHTML = followupData.map(f => `
                    <tr>
                        <td class="ps-4">${f.student_id}</td>
                        <td>${f.student_name}</td>
                        <td>${f.school_name}</td>
                        <td>${f.last_visit_date}</td>
                        <td><span class="badge ${f.status === 'Due' ? 'bg-warning' : 'bg-danger'}">${f.status}</span></td>
                        <td class="text-end pe-4"><button class="btn btn-sm btn-primary" onclick="openNewFollowup('${f.student_id}')">Start Follow-up</button></td>
                    </tr>
                `).join('');
            }
        }
    };

    // --- FOLLOW-UP MODAL LOGIC ---
    const followupModalEl = document.getElementById('followupModal');
    const followupModal = new bootstrap.Modal(followupModalEl);
    const followupForm = document.getElementById('followupForm');
    const followupSubmitBtn = document.getElementById('followupSubmitBtn');

    const openNewFollowup = (studentId = '') => {
        followupForm.reset();
        document.getElementById('fuStudentId').value = studentId;
        followupModal.show();
    };

    const handleFollowupSubmit = async (event) => {
        event.preventDefault();
        const formData = new FormData(followupForm);
        const payload = {
            student_id: formData.get('fuStudentId'),
            visit_date: formData.get('fuVisitDate'),
            ocular: {
                uncorrectedvisual_acuity_right_eye: formData.get('ucva_re'),
                uncorrectedvisual_acuity_left_eye: formData.get('ucva_le'),
                bestcorrectedvisual_acuity_right_eye: formData.get('bcva_re'),
                bestcorrectedvisual_acuity_left_eye: formData.get('bcva_le'),
                cycloplegic_auto_refraction_right_eye: formData.get('cyclo_se_re'),
                cycloplegic_auto_refraction_left_eye: formData.get('cyclo_se_le'),
                axial_length_right_eye: formData.get('axial_length_re'),
                axial_length_left_eye: formData.get('axial_length_le'),
                corneal_curvature_right_eye: formData.get('keratometry_re'),
                corneal_curvature_left_eye: formData.get('keratometry_le'),
                central_corneal_thickness_right_eye: formData.get('cct_re'),
                central_corneal_thickness_left_eye: formData.get('cct_le'),
                anterior_segment_finding_right_eye: formData.get('anterior_segment_re'),
                anterior_segment_finding_left_eye: formData.get('anterior_segment_le'),
                fundus_examination_finding_right_eye: formData.get('fundus_findings_re'),
                fundus_examination_finding_left_eye: formData.get('fundus_findings_le'),
                amblyopia_or_strabismus: formData.get('amblyopia_or_strabismus') === 'true',
            },
            // Add other form sections (lifestyle, history etc.) if they are part of the followup form
        };

        followupSubmitBtn.disabled = true;
        followupSubmitBtn.innerHTML = `<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Submitting...`;

        try {
            await apiRequest('/forms/submit-followup/', {
                method: 'POST',
                body: JSON.stringify(payload),
            });
            followupModal.hide();
            showToast('Follow-up submitted successfully!', 'success');
            // Optionally, refresh the follow-ups list
            if (document.getElementById('followups').classList.contains('active')) {
                await renderFollowups();
            }
        } catch (error) {
            // Error is handled by apiRequest, just re-enable the button
        } finally {
            followupSubmitBtn.disabled = false;
            followupSubmitBtn.textContent = 'Submit';
        }
    };
    
    // Attach listener to the submit button
    if(followupSubmitBtn) {
        followupSubmitBtn.addEventListener('click', handleFollowupSubmit);
    }
    
    // We need a global function to be called from the dynamic follow-up list
    window.openNewFollowup = openNewFollowup;


    // --- SIDEBAR TOGGLING LOGIC ---
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


    // --- INITIALIZATION ---
    const init = () => {
        // Remove all onclick attributes and replace with modern listeners
        document.querySelectorAll('[onclick]').forEach(el => {
            const onclickValue = el.getAttribute('onclick');
            el.removeAttribute('onclick');
            
            // Re-wire specific, known functions
            if (onclickValue.includes('showSection')) {
                const sectionMatch = onclickValue.match(/showSection\('([^']+)'/);
                if(sectionMatch) {
                    const sectionId = sectionMatch[1];
                     el.addEventListener('click', e => {
                        e.preventDefault();
                        showSection(sectionId, el);
                        // Close sidebar on mobile after navigating
                        if (sidebar.classList.contains('show')) {
                            sidebar.classList.remove('show');
                            sidebarOverlay.classList.remove('show');
                        }
                    });
                }
            } else if (onclickValue.includes('submitLogout')) {
                 el.addEventListener('click', e => {
                    e.preventDefault();
                    localStorage.clear();
                    window.location.href = '/login.html';
                });
            } else if (onclickValue.includes('openNewFollowup')) {
                el.addEventListener('click', e => {
                    e.preventDefault();
                    openNewFollowup();
                });
            }
            // Other onclicks can be wired up here or get a placeholder
            else {
                el.addEventListener('click', e => {
                    e.preventDefault();
                    showToast(`Functionality for "${onclickValue}" is not yet implemented.`);
                });
            }
        });
        
        // Initial Load
        const initialLink = document.querySelector('.nav-link.active');
        showSection('dashboard', initialLink);
    };

    init();
});