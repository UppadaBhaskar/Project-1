// Create Student Confirmation Modal
document.addEventListener('DOMContentLoaded', function() {
    const createForm = document.getElementById('createStudentForm');
    const confirmModal = document.getElementById('confirmModal');
    const confirmBtn = document.getElementById('confirmBtn');
    const cancelBtn = document.getElementById('cancelBtn');
    const closeModal = document.querySelector('#confirmModal .close-modal');

    if (createForm) {
        createForm.addEventListener('submit', function(e) {
            e.preventDefault();
            confirmModal.classList.add('active');
        });

        confirmBtn.addEventListener('click', function() {
            createForm.submit();
        });

        cancelBtn.addEventListener('click', function() {
            confirmModal.classList.remove('active');
        });

        if (closeModal) {
            closeModal.addEventListener('click', function() {
                confirmModal.classList.remove('active');
            });
        }

        // Close modal when clicking outside
        confirmModal.addEventListener('click', function(e) {
            if (e.target === confirmModal) {
                confirmModal.classList.remove('active');
            }
        });
    }

    // Delete Confirmation Modal
    const deleteModal = document.getElementById('deleteModal');
    const deleteCancelBtn = document.getElementById('deleteCancelBtn');
    const deleteCloseModal = document.querySelector('#deleteModal .close-modal');

    if (deleteCancelBtn) {
        deleteCancelBtn.addEventListener('click', function() {
            deleteModal.classList.remove('active');
        });
    }

    if (deleteCloseModal) {
        deleteCloseModal.addEventListener('click', function() {
            deleteModal.classList.remove('active');
        });
    }

    if (deleteModal) {
        deleteModal.addEventListener('click', function(e) {
            if (e.target === deleteModal) {
                deleteModal.classList.remove('active');
            }
        });
    }

    // Auto-hide flash messages after 5 seconds
    const flashMessages = document.querySelectorAll('.flash-message');
    flashMessages.forEach(function(message) {
        setTimeout(function() {
            message.style.transition = 'opacity 0.5s';
            message.style.opacity = '0';
            setTimeout(function() {
                message.remove();
            }, 500);
        }, 5000);
    });
});

// Show delete modal
function showDeleteModal(rollNumber) {
    const deleteModal = document.getElementById('deleteModal');
    const deleteForm = document.getElementById('deleteForm');
    
    if (deleteForm) {
        deleteForm.action = `/student/${rollNumber}/delete`;
    }
    
    if (deleteModal) {
        deleteModal.classList.add('active');
    }
}

