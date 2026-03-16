<!-- Google Analytics 4 Setup -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-XXXXXXXXXX"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());

  gtag('config', 'G-XXXXXXXXXX', {
    'page_path': window.location.pathname,
    'page_title': document.title,
    'send_page_view': true
  });

  // Track custom events
  function trackEvent(eventName, eventParams) {
    gtag('event', eventName, eventParams);
  }

  // Track supplement clicks
  document.addEventListener('click', function(e) {
    if (e.target.closest('a[href*="amway"], a[href*="amazon"]')) {
      trackEvent('affiliate_click', {
        'link_url': e.target.closest('a').href,
        'link_text': e.target.textContent
      });
    }
  });

  // Track scroll depth
  let maxScroll = 0;
  window.addEventListener('scroll', function() {
    const scrollPercent = (window.scrollY / (document.documentElement.scrollHeight - window.innerHeight)) * 100;
    if (scrollPercent > maxScroll) {
      maxScroll = scrollPercent;
      if (maxScroll >= 25 && maxScroll < 50) {
        trackEvent('scroll_25');
      } else if (maxScroll >= 50 && maxScroll < 75) {
        trackEvent('scroll_50');
      } else if (maxScroll >= 75) {
        trackEvent('scroll_75');
      }
    }
  });
</script>
