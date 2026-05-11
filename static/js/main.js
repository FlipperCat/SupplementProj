// Supplement Guide - Main JavaScript

// Dark Mode - runs before DOMContentLoaded to prevent flash
(function() {
    const saved = localStorage.getItem('theme');
    if (saved === 'dark' || (!saved && window.matchMedia('(prefers-color-scheme: dark)').matches)) {
        document.documentElement.setAttribute('data-theme', 'dark');
    }
})();

document.addEventListener('DOMContentLoaded', function() {

    // Dark Mode Toggle
    const themeToggle = document.getElementById('theme-toggle');
    if (themeToggle) {
        themeToggle.addEventListener('click', function() {
            const current = document.documentElement.getAttribute('data-theme');
            const next = current === 'dark' ? 'light' : 'dark';
            document.documentElement.setAttribute('data-theme', next);
            localStorage.setItem('theme', next);
        });
    }

    // Mobile Dropdown Toggles
    document.querySelectorAll('.mobile-dropdown-toggle').forEach(function(btn) {
        btn.addEventListener('click', function() {
            const items = this.nextElementSibling;
            items.classList.toggle('active');
            this.classList.toggle('active');
        });
    });
    // Mobile Menu Toggle
    const mobileMenuToggle = document.querySelector('.mobile-menu-toggle');
    const mobileNav = document.querySelector('.mobile-nav');

    if (mobileMenuToggle && mobileNav) {
        mobileMenuToggle.addEventListener('click', function() {
            mobileNav.classList.toggle('active');
            mobileMenuToggle.classList.toggle('active');
        });
    }

    // Search Toggle
    const searchToggle = document.querySelector('.search-toggle');
    const searchOverlay = document.querySelector('.search-overlay');
    const searchClose = document.querySelector('.search-close');
    const searchInput = document.querySelector('.search-input');

    if (searchToggle && searchOverlay) {
        searchToggle.addEventListener('click', function() {
            searchOverlay.classList.add('active');
            setTimeout(() => searchInput?.focus(), 100);
        });

        searchClose?.addEventListener('click', function() {
            searchOverlay.classList.remove('active');
        });

        searchOverlay.addEventListener('click', function(e) {
            if (e.target === searchOverlay) {
                searchOverlay.classList.remove('active');
            }
        });

        document.addEventListener('keydown', function(e) {
            if (e.key === 'Escape' && searchOverlay.classList.contains('active')) {
                searchOverlay.classList.remove('active');
            }
        });
    }

    // Smooth scroll for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });

    // Add active class to current nav item based on URL
    const currentPath = window.location.pathname;
    document.querySelectorAll('.nav-link').forEach(link => {
        if (link.getAttribute('href') === currentPath ||
            (currentPath.startsWith(link.getAttribute('href')) && link.getAttribute('href') !== '/')) {
            link.classList.add('active');
        }
    });

    // Table of Contents - Generate from headings
    const articleContent = document.querySelector('.article-content');
    const tocContainer = document.querySelector('.toc-list');

    if (articleContent && tocContainer) {
        const headings = articleContent.querySelectorAll('h2, h3');

        headings.forEach((heading, index) => {
            // Add ID to heading if it doesn't have one
            if (!heading.id) {
                heading.id = `section-${index}`;
            }

            const li = document.createElement('li');
            li.className = heading.tagName === 'H3' ? 'toc-h3' : 'toc-h2';

            const a = document.createElement('a');
            a.href = `#${heading.id}`;
            a.textContent = heading.textContent;

            li.appendChild(a);
            tocContainer.appendChild(li);
        });
    }

    // Scroll progress indicator
    const progressBar = document.querySelector('.reading-progress');
    if (progressBar) {
        window.addEventListener('scroll', function() {
            const docHeight = document.documentElement.scrollHeight - window.innerHeight;
            const scrolled = (window.scrollY / docHeight) * 100;
            progressBar.style.width = scrolled + '%';
        });
    }

    // Lazy load images
    const lazyImages = document.querySelectorAll('img[data-src]');
    if ('IntersectionObserver' in window) {
        const imageObserver = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    img.src = img.dataset.src;
                    img.removeAttribute('data-src');
                    observer.unobserve(img);
                }
            });
        });

        lazyImages.forEach(img => imageObserver.observe(img));
    } else {
        // Fallback for browsers without IntersectionObserver
        lazyImages.forEach(img => {
            img.src = img.dataset.src;
        });
    }

    // Copy affiliate link functionality
    document.querySelectorAll('.copy-link').forEach(button => {
        button.addEventListener('click', function() {
            const link = this.dataset.link;
            navigator.clipboard.writeText(link).then(() => {
                const originalText = this.textContent;
                this.textContent = 'Copied!';
                setTimeout(() => {
                    this.textContent = originalText;
                }, 2000);
            });
        });
    });

    // Accordion functionality for FAQ sections
    document.querySelectorAll('.accordion-header').forEach(header => {
        header.addEventListener('click', function() {
            const accordion = this.parentElement;
            const content = this.nextElementSibling;

            accordion.classList.toggle('active');

            if (accordion.classList.contains('active')) {
                content.style.maxHeight = content.scrollHeight + 'px';
            } else {
                content.style.maxHeight = null;
            }
        });
    });

    // Enhanced Affiliate Tracking
    document.querySelectorAll('a[data-affiliate]').forEach(link => {
        link.addEventListener('click', function() {
            const affiliateData = {
                product: this.dataset.product || 'unknown',
                affiliate: this.dataset.affiliate,
                url: this.href,
                page: window.location.pathname,
                pageTitle: document.title
            };

            // Log for debugging
            console.log('Affiliate click:', affiliateData);

            // Google Analytics tracking
            if (typeof gtag !== 'undefined') {
                gtag('event', 'affiliate_click', {
                    'event_category': 'Monetization',
                    'event_label': affiliateData.product,
                    'affiliate_program': affiliateData.affiliate,
                    'source_page': affiliateData.page,
                    'value': 1
                });
            }
        });
    });

    // ============================================
    // ENHANCED ANALYTICS & TRACKING
    // ============================================

    // Scroll Depth Tracking
    let scrollDepthTracked = { 25: false, 50: false, 75: false, 100: false };

    window.addEventListener('scroll', function() {
        if (typeof gtag === 'undefined') return;

        const scrollHeight = document.documentElement.scrollHeight - window.innerHeight;
        const scrollPercent = Math.round((window.scrollY / scrollHeight) * 100);

        [25, 50, 75, 100].forEach(threshold => {
            if (scrollPercent >= threshold && !scrollDepthTracked[threshold]) {
                scrollDepthTracked[threshold] = true;
                gtag('event', 'scroll_depth', {
                    'event_category': 'Engagement',
                    'event_label': threshold + '%',
                    'value': threshold
                });
            }
        });
    });

    // Time on Page Tracking
    const pageStartTime = Date.now();

    window.addEventListener('beforeunload', function() {
        if (typeof gtag === 'undefined') return;

        const timeOnPage = Math.round((Date.now() - pageStartTime) / 1000);
        gtag('event', 'time_on_page', {
            'event_category': 'Engagement',
            'event_label': window.location.pathname,
            'value': timeOnPage
        });
    });

    // Share Button Tracking
    document.querySelectorAll('[data-share]').forEach(btn => {
        btn.addEventListener('click', function(e) {
            const platform = this.dataset.share;

            // Copy link functionality
            if (platform === 'copy') {
                e.preventDefault();
                const url = this.dataset.url || window.location.href;
                navigator.clipboard.writeText(url).then(() => {
                    this.classList.add('copied');
                    setTimeout(() => this.classList.remove('copied'), 2000);
                });
            }

            // Track share
            if (typeof gtag !== 'undefined') {
                gtag('event', 'share', {
                    'event_category': 'Social',
                    'event_label': platform,
                    'content_type': 'article',
                    'item_id': window.location.pathname
                });
            }
        });
    });

    // ============================================
    // EXIT INTENT POPUP
    // ============================================

    const exitPopup = document.getElementById('exitPopup');
    const exitIntentShown = localStorage.getItem('exitIntentShown');

    if (exitPopup && !exitIntentShown) {
        // Exit intent detection
        document.addEventListener('mouseout', function(e) {
            if (e.clientY < 10 && e.relatedTarget === null) {
                showExitPopup();
            }
        });

        // Also show after 60 seconds of inactivity
        let inactivityTimer;
        const resetInactivityTimer = () => {
            clearTimeout(inactivityTimer);
            inactivityTimer = setTimeout(() => {
                if (!exitIntentShown) showExitPopup();
            }, 60000);
        };

        ['mousemove', 'keydown', 'scroll', 'click'].forEach(event => {
            document.addEventListener(event, resetInactivityTimer);
        });
        resetInactivityTimer();
    }

    function showExitPopup() {
        if (localStorage.getItem('exitIntentShown')) return;

        exitPopup.style.display = 'flex';
        localStorage.setItem('exitIntentShown', 'true');

        if (typeof gtag !== 'undefined') {
            gtag('event', 'exit_intent_shown', {
                'event_category': 'Lead Generation',
                'event_label': window.location.pathname
            });
        }
    }

    // Close popup handlers
    document.querySelectorAll('[data-close-popup]').forEach(el => {
        el.addEventListener('click', function() {
            exitPopup.style.display = 'none';
        });
    });

    // Close on Escape key
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape' && exitPopup && exitPopup.style.display === 'flex') {
            exitPopup.style.display = 'none';
        }
    });

    // ============================================
    // FORM HANDLING
    // ============================================

    document.querySelectorAll('form[data-form]').forEach(form => {
        form.addEventListener('submit', function(e) {
            e.preventDefault();

            const formType = this.dataset.form;
            const email = this.querySelector('input[type="email"]').value;
            const leadMagnet = this.dataset.magnet || '';
            const button = this.querySelector('button[type="submit"]');
            const originalText = button.textContent;

            button.textContent = 'Sending...';
            button.disabled = true;

            // Submit to Netlify Forms
            const formData = new FormData(this);
            fetch('/', {
                method: 'POST',
                headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
                body: new URLSearchParams(formData).toString()
            })
            .then(function(response) {
                if (!response.ok) throw new Error('Form submission failed');

                // Track form submission
                if (typeof gtag !== 'undefined') {
                    gtag('event', 'form_submit', {
                        'event_category': 'Lead Generation',
                        'event_label': formType,
                        'lead_magnet': leadMagnet
                    });
                }

                button.textContent = 'Thank you!';

                // If exit popup, close it
                if (formType === 'exit-intent') {
                    setTimeout(function() {
                        exitPopup.style.display = 'none';
                    }, 1500);
                }

                // Reset form
                setTimeout(function() {
                    form.reset();
                    button.textContent = originalText;
                    button.disabled = false;
                }, 3000);
            })
            .catch(function() {
                button.textContent = 'Error - Try Again';
                button.disabled = false;
                setTimeout(function() {
                    button.textContent = originalText;
                }, 3000);
            });
        });
    });

    // ============================================
    // ANALYZER TOOL TRACKING
    // ============================================

    // Track when supplements are added to analyzer
    document.querySelectorAll('.add-to-analyzer').forEach(btn => {
        btn.addEventListener('click', function() {
            const supplement = this.dataset.supplement;

            if (typeof gtag !== 'undefined') {
                gtag('event', 'analyzer_add', {
                    'event_category': 'Tool Usage',
                    'event_label': supplement
                });
            }
        });
    });

    // Track analyzer interactions
    document.querySelectorAll('.analyzer-action').forEach(btn => {
        btn.addEventListener('click', function() {
            const action = this.dataset.action;
            const supplementCount = document.querySelectorAll('.selected-supplement').length;

            if (typeof gtag !== 'undefined') {
                gtag('event', 'analyzer_interaction', {
                    'event_category': 'Tool Usage',
                    'event_label': action,
                    'supplements_count': supplementCount
                });
            }
        });
    });
});

// Sticky sidebar functionality
function initStickySidebar() {
    const sidebar = document.querySelector('.supplement-sidebar');
    if (!sidebar || window.innerWidth < 1024) return;

    const sidebarTop = sidebar.offsetTop;
    const headerHeight = 80;

    window.addEventListener('scroll', function() {
        if (window.scrollY > sidebarTop - headerHeight) {
            sidebar.classList.add('is-sticky');
        } else {
            sidebar.classList.remove('is-sticky');
        }
    });
}

// Initialize on load
window.addEventListener('load', initStickySidebar);
window.addEventListener('resize', initStickySidebar);
