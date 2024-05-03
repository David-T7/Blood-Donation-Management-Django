function validateForm() {
    console.log("Form submission triggered.");

    const form = document.getElementById('registration-form');
    console.log("Form:", form);

    const requiredFields = form.querySelectorAll('[required]');
    console.log("Required fields:", requiredFields);

    let isValid = true;

    requiredFields.forEach(function(field) {
        console.log("Checking field:", field);

        // Remove any existing error messages
        const existingErrorMessage = field.parentNode.querySelector('.required-message');
        if (existingErrorMessage) {
            existingErrorMessage.remove();
        }

        if (!field.value.trim()) {
            isValid = false;
            console.log("Field is empty:", field);
            
            const errorMessage = document.createElement('span');
            errorMessage.textContent = 'This field is required';
            errorMessage.style.color = 'red';
            errorMessage.classList.add('required-message');
            console.log("Error message created:", errorMessage);

            field.parentNode.appendChild(errorMessage);
            console.log("Error message appended to field.");
        }
    });

    if (!isValid) {
        console.log("Form submission prevented due to empty required fields.");
        return false; // Prevent form submission if any required field is empty
    } else {
        console.log("Form submission allowed.");
        return true; // Allow form submission if all required fields are filled
    }
}