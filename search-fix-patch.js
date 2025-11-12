// Stremio Hisense Search Fix Patch
// This patch fixes the search bug where pressing OK on the TV remote doesn't submit the search
// Bug: The original code uses event.target.value which is undefined when the form is submitted via remote

console.log('[SEARCH FIX] Loading search fix patch...');

// Wait for the app to load
window.addEventListener('load', function() {
    console.log('[SEARCH FIX] App loaded, applying patch...');

    // Function to find and patch search forms
    function patchSearchForms() {
        // Find all forms in the document
        const forms = document.querySelectorAll('form');
        console.log('[SEARCH FIX] Found', forms.length, 'forms');

        forms.forEach((form, index) => {
            // Check if this form contains a search input
            const searchInput = form.querySelector('input[type="text"]') ||
                              form.querySelector('input[type="search"]') ||
                              form.querySelector('input');

            if (searchInput) {
                console.log('[SEARCH FIX] Found search input in form', index);

                // Remove existing submit listeners by cloning
                const newForm = form.cloneNode(true);
                form.parentNode.replaceChild(newForm, form);

                // Add our fixed submit handler
                newForm.addEventListener('submit', function(event) {
                    event.preventDefault();
                    event.stopPropagation();

                    // Get the search input from the new form
                    const input = newForm.querySelector('input[type="text"]') ||
                                newForm.querySelector('input[type="search"]') ||
                                newForm.querySelector('input');

                    if (input && input.value) {
                        const searchValue = input.value.trim();
                        console.log('[SEARCH FIX] Search submitted:', searchValue);

                        // Navigate to search results
                        const searchUrl = `/search?search=${encodeURIComponent(searchValue)}`;
                        window.location.hash = searchUrl;

                        console.log('[SEARCH FIX] Navigated to:', searchUrl);
                    } else {
                        console.log('[SEARCH FIX] No search value found');
                    }
                }, true); // Use capture phase to run before other handlers

                console.log('[SEARCH FIX] Patched form', index);
            }
        });
    }

    // Apply patch immediately
    patchSearchForms();

    // Re-apply patch when DOM changes (in case React re-renders)
    const observer = new MutationObserver(function(mutations) {
        let shouldPatch = false;
        mutations.forEach(function(mutation) {
            if (mutation.addedNodes.length > 0) {
                mutation.addedNodes.forEach(function(node) {
                    if (node.nodeName === 'FORM' ||
                        (node.querySelectorAll && node.querySelectorAll('form').length > 0)) {
                        shouldPatch = true;
                    }
                });
            }
        });

        if (shouldPatch) {
            console.log('[SEARCH FIX] DOM changed, re-applying patch...');
            setTimeout(patchSearchForms, 100);
        }
    });

    // Start observing
    observer.observe(document.body, {
        childList: true,
        subtree: true
    });

    console.log('[SEARCH FIX] Patch applied successfully!');
});
