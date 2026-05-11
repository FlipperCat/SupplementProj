// Pagefind Search Integration
(function() {
    var pagefind = null;
    var searchInput = document.getElementById('pagefind-search');
    var resultsContainer = document.getElementById('pagefind-results');
    var debounceTimer = null;

    if (!searchInput || !resultsContainer) return;

    async function initPagefind() {
        if (pagefind) return pagefind;
        try {
            pagefind = await import('/pagefind/pagefind.js');
            await pagefind.init();
            return pagefind;
        } catch (e) {
            resultsContainer.innerHTML = '<p class="search-no-results">Search index not yet available. Deploy the site to enable search.</p>';
            return null;
        }
    }

    async function performSearch(query) {
        if (!query || query.length < 2) {
            resultsContainer.innerHTML = '';
            resultsContainer.style.display = 'none';
            return;
        }

        var pf = await initPagefind();
        if (!pf) return;

        var search = await pf.search(query);
        var results = await Promise.all(search.results.slice(0, 8).map(function(r) { return r.data(); }));

        if (results.length === 0) {
            resultsContainer.innerHTML = '<p class="search-no-results">No results found for "' + query.replace(/</g, '&lt;') + '"</p>';
            resultsContainer.style.display = 'block';
            return;
        }

        var html = '<ul class="search-results-list">';
        results.forEach(function(result) {
            var section = result.url.split('/')[1] || '';
            var label = section.charAt(0).toUpperCase() + section.slice(1);
            html += '<li class="search-result-item">';
            html += '<a href="' + result.url + '">';
            html += '<span class="search-result-section">' + label + '</span>';
            html += '<span class="search-result-title">' + result.meta.title + '</span>';
            html += '<span class="search-result-excerpt">' + (result.excerpt || '') + '</span>';
            html += '</a></li>';
        });
        html += '</ul>';

        resultsContainer.innerHTML = html;
        resultsContainer.style.display = 'block';
    }

    searchInput.addEventListener('input', function() {
        clearTimeout(debounceTimer);
        var query = this.value;
        debounceTimer = setTimeout(function() {
            performSearch(query);
        }, 200);
    });

    // Also hook up the hero search
    var heroSearch = document.querySelector('.hero-search input');
    var heroBtn = document.querySelector('.hero-search button');
    if (heroSearch && heroBtn) {
        heroBtn.addEventListener('click', function(e) {
            e.preventDefault();
            var overlay = document.querySelector('.search-overlay');
            if (overlay) {
                overlay.classList.add('active');
                searchInput.value = heroSearch.value;
                searchInput.focus();
                performSearch(heroSearch.value);
            }
        });
        heroSearch.addEventListener('keydown', function(e) {
            if (e.key === 'Enter') {
                e.preventDefault();
                heroBtn.click();
            }
        });
    }

    // Close results when overlay closes
    var searchClose = document.querySelector('.search-close');
    if (searchClose) {
        searchClose.addEventListener('click', function() {
            resultsContainer.style.display = 'none';
            resultsContainer.innerHTML = '';
        });
    }
})();
