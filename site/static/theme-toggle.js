// theme-toggle.js
function toggleTheme() {
    const root = document.documentElement;
    const lightSpan = document.querySelector('#theme-toggle .light');
    const darkSpan = document.querySelector('#theme-toggle .dark');

    // Toggle the theme
    if (root.classList.contains('dark-theme')) {
        root.classList.remove('dark-theme');
        localStorage.setItem('theme', 'light');
    } else {
        root.classList.add('dark-theme');
        localStorage.setItem('theme', 'dark');
    }

    // Update the button's active span
    updateActiveSpan();
}

function updateActiveSpan() {
    const root = document.documentElement;
    const lightSpan = document.querySelector('#theme-toggle .light');
    const darkSpan = document.querySelector('#theme-toggle .dark');

    if (root.classList.contains('dark-theme')) {
        lightSpan.classList.remove('active');
        darkSpan.classList.add('active');
    } else {
        darkSpan.classList.remove('active');
        lightSpan.classList.add('active');
    }
}

document.addEventListener('DOMContentLoaded', () => {
    // Update the spans to reflect the current state
    updateActiveSpan();

    // Add the click event listener for toggling the theme
    const themeToggleButton = document.getElementById('theme-toggle');
    themeToggleButton.addEventListener('click', toggleTheme);
});
