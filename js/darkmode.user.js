// ==UserScript==
// @name         darkmode
// @version      1.0
// @description  本地HTML黑暗模式
// @match        file:///*
// @grant        none
// ==/UserScript==

(function() {
    'use strict';

    // Create a style element for dark mode
    var darkModeStyle = document.createElement('style');
    darkModeStyle.type = 'text/css';
    darkModeStyle.innerHTML = `
        body, header, footer, nav, section, article, aside, div, p, span, ul, ol, li, table, tr, th, td {
            background-color: #121212 !important;
            color: #cdcdcd !important;
        }
        a {
            color: #bb86fc !important;
        }
        img {
            filter: invert(1) hue-rotate(180deg);
        }
    `;

    // Create a style element for font settings
    var fontStyle = document.createElement('style');
    fontStyle.type = 'text/css';
    fontStyle.innerHTML = `
        body, header, footer, nav, section, article, aside, div, p, span, ul, ol, li, table, tr, th, td {
            font-family: 'PingFang SC', serif !important;
            font-weight: 400 !important;
            -webkit-font-smoothing: antialiased !important;
            -moz-osx-font-smoothing: grayscale !important;
        }
        h1, h2, h3, h4, h5, h6 {
            font-weight: 600 !important;
        }
    `;

    // Append the font style element to the head
    document.head.appendChild(fontStyle);

    // Function to apply or remove dark mode based on user preference or system preference
    function applyDarkMode(apply) {
        if (apply) {
            document.head.appendChild(darkModeStyle);
        } else if (darkModeStyle.parentNode) {
            darkModeStyle.parentNode.removeChild(darkModeStyle);
        }
    }

    // Detect system dark mode preference
    var systemPrefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;

    // Initial application of dark mode based on system preference
    applyDarkMode(systemPrefersDark);

    // Create the toggle button
    var toggleButton = document.createElement('button');
    toggleButton.innerHTML = 'Toggle Dark Mode';
    toggleButton.style.position = 'fixed';
    toggleButton.style.bottom = '10px';
    toggleButton.style.right = '10px';
    toggleButton.style.zIndex = '10000';
    toggleButton.style.padding = '10px';
    toggleButton.style.backgroundColor = '#444';
    toggleButton.style.color = '#fff';
    toggleButton.style.border = 'none';
    toggleButton.style.borderRadius = '5px';
    toggleButton.style.cursor = 'pointer';

    // Append the button to the body
    document.body.appendChild(toggleButton);

    // Add event listener to toggle dark mode
    toggleButton.addEventListener('click', function() {
        var darkModeEnabled = darkModeStyle.parentNode;
        applyDarkMode(!darkModeEnabled);
    });
})();