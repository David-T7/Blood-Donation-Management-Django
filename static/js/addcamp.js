document.addEventListener('DOMContentLoaded', function() {
    // Find the Location input field
    const locationInput = document.querySelector('input[name="Location"], textarea[name="Location"]');
    const helpText = document.getElementById('location-help');

    if (locationInput && helpText) {
        // Show help text on focus
        locationInput.addEventListener('focus', function() {
            helpText.style.display = 'block';
        });

        // Hide help text when focus is lost (blur event)
        locationInput.addEventListener('blur', function() {
            // Use setTimeout to allow for click events on the help text
            setTimeout(function() {
                if (document.activeElement !== helpText && !helpText.contains(document.activeElement)) {
                    helpText.style.display = 'none';
                }
            }, 100);
        });

        // Also show help text on mouseover
        locationInput.addEventListener('mouseover', function() {
            helpText.style.display = 'block';
        });

        // Hide help text on mouseout (with a delay to allow for movement to help text)
        locationInput.addEventListener('mouseout', function() {
            setTimeout(function() {
                if (!locationInput.matches(':hover') &&
                    document.activeElement !== helpText &&
                    !helpText.contains(document.activeElement)) {
                    helpText.style.display = 'none';
                }
            }, 100);
        });

        // Handle clicks on the help text to keep it visible
        helpText.addEventListener('mouseover', function() {
            helpText.style.display = 'block';
        });

        helpText.addEventListener('mouseout', function() {
            setTimeout(function() {
                if (!locationInput.matches(':hover') &&
                    document.activeElement !== helpText &&
                    !helpText.contains(document.activeElement)) {
                    helpText.style.display = 'none';
                }
            }, 100);
        });
    }
});