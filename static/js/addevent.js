document.addEventListener('DOMContentLoaded', function() {
    // Find the EventMap input field
    const eventMapInput = document.querySelector('input[name="EventMap"], textarea[name="EventMap"]');
    const helpText = document.getElementById('event-map-help');

    if (eventMapInput && helpText) {
        // Show help text on focus
        eventMapInput.addEventListener('focus', function() {
            helpText.style.display = 'block';
        });

        // Hide help text when focus is lost (blur event)
        eventMapInput.addEventListener('blur', function() {
            // Use setTimeout to allow for click events on the help text
            setTimeout(function() {
                if (document.activeElement !== helpText && !helpText.contains(document.activeElement)) {
                    helpText.style.display = 'none';
                }
            }, 100);
        });

        // Also show help text on mouseover
        eventMapInput.addEventListener('mouseover', function() {
            helpText.style.display = 'block';
        });

        // Hide help text on mouseout (with a delay to allow for movement to help text)
        eventMapInput.addEventListener('mouseout', function() {
            setTimeout(function() {
                if (!eventMapInput.matches(':hover') &&
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
                if (!eventMapInput.matches(':hover') &&
                    document.activeElement !== helpText &&
                    !helpText.contains(document.activeElement)) {
                    helpText.style.display = 'none';
                }
            }, 100);
        });
    }
});