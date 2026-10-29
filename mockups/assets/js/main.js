/* БелЕвропривод — interactions for the home page mockup */
(function () {
  'use strict';

  var $ = function (sel, root) { return (root || document).querySelector(sel); };
  var $$ = function (sel, root) { return Array.prototype.slice.call((root || document).querySelectorAll(sel)); };

  /* ---------- header ---------- */
  var header = $('#site-header');
  var lastY = 0;
  function onScroll() {
    var y = window.scrollY || 0;
    if (header) header.classList.toggle('is-sticky', y > 120);
    lastY = y;
    updateProgress();
  }
  window.addEventListener('scroll', onScroll, { passive: true });

  /* ---------- scroll progress ---------- */
  var bar = $('.bep-progress .bar');
  var label = $('.bep-progress .bep-progress-label');
  var CIRC = 2 * Math.PI * 28;
  if (bar) {
    bar.style.strokeDasharray = CIRC + ' ' + CIRC;
    bar.style.strokeDashoffset = CIRC;
  }
  function updateProgress() {
    if (!bar) return;
    var h = document.documentElement.scrollHeight - window.innerHeight;
    var p = h > 0 ? Math.min(1, (window.scrollY || 0) / h) : 0;
    bar.style.strokeDashoffset = CIRC - CIRC * p;
    if (label) label.textContent = Math.round(p * 100) + '%';
  }
  var progressBtn = $('.bep-progress');
  if (progressBtn) {
    progressBtn.addEventListener('click', function () {
      window.scrollTo({ top: 0, behavior: 'smooth' });
    });
  }

  /* ---------- mobile menu ---------- */
  var panel = $('#bep-mobile');
  $$('.bep-burger').forEach(function (b) {
    b.addEventListener('click', function () { panel.classList.add('is-open'); document.body.style.overflow = 'hidden'; });
  });
  $$('.bep-mobile-close, #bep-mobile a').forEach(function (b) {
    b.addEventListener('click', function () {
      if (b.tagName === 'A') { panel.classList.remove('is-open'); document.body.style.overflow = ''; }
    });
  });
  var mClose = $('.bep-mobile-close');
  if (mClose) mClose.addEventListener('click', function () { panel.classList.remove('is-open'); document.body.style.overflow = ''; });

  /* ---------- search ---------- */
  var search = $('#bep-search');
  var searchInput = $('#bep-search-input');
  var results = $('#bep-search-results');
  var hint = $('#bep-search-hint');
  var INDEX = window.BEP_PRODUCTS || [];

  function openSearch() {
    search.classList.add('is-open');
    document.body.style.overflow = 'hidden';
    renderSearch('');
    setTimeout(function () { searchInput.focus(); }, 60);
  }
  function closeSearch() {
    search.classList.remove('is-open');
    document.body.style.overflow = '';
  }
  $$('[data-open-search]').forEach(function (b) { b.addEventListener('click', openSearch); });
  $('#bep-search').addEventListener('click', function (e) {
    if (e.target === search) closeSearch();
  });
  var searchClose = $('.bep-search-close');
  if (searchClose) searchClose.addEventListener('click', closeSearch);

  function esc(s) {
    return String(s).replace(/[&<>"]/g, function (c) {
      return ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' })[c];
    });
  }

  function renderSearch(q) {
    q = (q || '').trim().toLowerCase();
    var list;
    if (!q) {
      list = INDEX.slice(0, 6);
      hint.textContent = 'Популярные позиции · всего в базе ' + INDEX.length + ' товаров';
    } else {
      list = INDEX.filter(function (p) {
        return (p.n + ' ' + p.c).toLowerCase().indexOf(q) > -1;
      }).slice(0, 24);
      hint.textContent = list.length
        ? 'Найдено: ' + list.length + (list.length === 24 ? '+' : '') + ' · показаны первые 24'
        : '';
    }
    if (!list.length) {
      results.innerHTML = '<div class="bep-search-empty">Ничего не нашлось. Напишите нам — подберём аналог под задачу.</div>';
      return;
    }
    results.innerHTML = list.map(function (p) {
      return '<a class="bep-search-item" href="' + p.u + '" target="_blank" rel="noopener">' +
        '<img src="' + p.i + '" alt="">' +
        '<span><b>' + esc(p.n) + '</b><span>' + esc(p.c) + '</span></span>' +
        '</a>';
    }).join('');
  }
  if (searchInput) {
    searchInput.addEventListener('input', function () { renderSearch(searchInput.value); });
    searchInput.addEventListener('keydown', function (e) {
      if (e.key === 'Escape') closeSearch();
      if (e.key === 'Enter') {
        var first = results.querySelector('a');
        if (first) window.open(first.href, '_blank');
      }
    });
  }
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape') { closeSearch(); closeModal(); }
    if ((e.ctrlKey || e.metaKey) && e.key === 'k') { e.preventDefault(); openSearch(); }
  });

  /* ---------- callback modal ---------- */
  var modal = $('#bep-modal');
  function openModal() {
    modal.classList.add('is-open');
    document.body.style.overflow = 'hidden';
  }
  function closeModal() {
    modal.classList.remove('is-open');
    document.body.style.overflow = '';
  }
  $$('[data-open-modal]').forEach(function (b) {
    b.addEventListener('click', function (e) { e.preventDefault(); openModal(); });
  });
  $$('.bep-modal-close').forEach(function (b) { b.addEventListener('click', closeModal); });
  modal.addEventListener('click', function (e) { if (e.target === modal) closeModal(); });

  /* ---------- forms ---------- */
  function validatePhone(v) {
    var digits = (v || '').replace(/\D/g, '');
    return digits.length >= 11 && digits.length <= 13;
  }
  $$('form[data-bep-form]').forEach(function (form) {
    var phone = form.querySelector('input[name="phone"]');
    var name = form.querySelector('input[name="name"]');
    var err = form.querySelector('.bep-form-error');
    var ok = form.querySelector('.bep-form-ok');
    if (phone) {
      phone.addEventListener('input', function () {
        var d = phone.value.replace(/\D/g, '').slice(0, 13);
        if (d.indexOf('375') === 0) d = d.slice(3);
        var out = '+375';
        if (d.length) out += ' (' + d.slice(0, 2) + ')';
        if (d.length > 2) out += ' ' + d.slice(2, 5);
        if (d.length > 5) out += '-' + d.slice(5, 7);
        if (d.length > 7) out += '-' + d.slice(7, 9);
        if (d.length > 9) out += d.slice(9, 11);
        phone.value = out;
        phone.classList.remove('is-error');
        if (err) err.textContent = '';
      });
    }
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var problems = [];
      if (name && name.value.trim().length < 2) { name.classList.add('is-error'); problems.push('Укажите имя'); }
      if (phone && !validatePhone(phone.value)) { phone.classList.add('is-error'); problems.push('Укажите телефон'); }
      if (problems.length) {
        if (err) err.textContent = problems.join(' · ');
        return;
      }
      if (err) err.textContent = '';
      form.querySelectorAll('input, textarea, button').forEach(function (el) { el.disabled = true; });
      if (ok) ok.classList.add('is-visible');
    });
  });

  /* ---------- sliders ---------- */
  function ready(fn) {
    if (document.readyState !== 'loading') fn();
    else document.addEventListener('DOMContentLoaded', fn);
  }

  ready(function () {
    if (!window.Swiper) return;
    var thumbs = new Swiper('.hero-thumb', {
      slidesPerView: 'auto',
      spaceBetween: 10,
      watchSlidesProgress: true
    });
    new Swiper('.hero-slider', {
      effect: 'fade',
      fadeEffect: { crossFade: true },
      speed: 800,
      loop: true,
      autoplay: { delay: 6500, disableOnInteraction: false },
      navigation: { prevEl: '.hero-navigation .slider-prev', nextEl: '.hero-navigation .slider-next' },
      thumbs: { swiper: thumbs }
    });
    new Swiper('.project-slider', {
      slidesPerView: 1.15,
      spaceBetween: 18,
      freeMode: true,
      mousewheel: false,
      breakpoints: {
        576: { slidesPerView: 2.1, spaceBetween: 20 },
        992: { slidesPerView: 3.2, spaceBetween: 24 },
        1280: { slidesPerView: 4.2, spaceBetween: 24 }
      }
    });
    new Swiper('.testimonial-slider-2', {
      slidesPerView: 1,
      spaceBetween: 20,
      navigation: { prevEl: '.testimonial-nav .slider-prev', nextEl: '.testimonial-nav .slider-next' }
    });
    new Swiper('.blog-slider', {
      slidesPerView: 1,
      spaceBetween: 20,
      navigation: { prevEl: '#blog-nav .slider-prev', nextEl: '#blog-nav .slider-next' },
      breakpoints: { 768: { slidesPerView: 1.6 }, 1200: { slidesPerView: 2, spaceBetween: 24 } }
    });
    var marquee = $('.footer-marquee .marquee-slider');
    if (marquee) {
      new Swiper(marquee, {
        slidesPerView: 'auto',
        spaceBetween: 40,
        loop: true,
        speed: 6000,
        allowTouchMove: false,
        autoplay: { delay: 0, disableOnInteraction: false }
      });
    }
  });

  /* ---------- counters ---------- */
  var counters = $$('[data-count]');
  var done = false;
  function runCounters() {
    if (done) return;
    done = true;
    counters.forEach(function (el) {
      var target = parseFloat(el.getAttribute('data-count'));
      var dur = 1400;
      var t0 = performance.now();
      function step(t) {
        var p = Math.min(1, (t - t0) / dur);
        var eased = 1 - Math.pow(1 - p, 3);
        var val = Math.round(target * eased);
        el.textContent = val;
        if (p < 1) requestAnimationFrame(step);
      }
      requestAnimationFrame(step);
    });
  }

  /* ---------- reveal ---------- */
  var revealEls = $$('[data-reveal]');
  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) {
          en.target.classList.add('is-inview');
          if (en.target.hasAttribute('data-count-block')) runCounters();
          io.unobserve(en.target);
        }
      });
    }, { threshold: 0.15 });
    revealEls.forEach(function (el) { io.observe(el); });
    var countersBlock = $('[data-count-block]');
    if (countersBlock) io.observe(countersBlock);
  } else {
    revealEls.forEach(function (el) { el.classList.add('is-inview'); });
    runCounters();
  }

  onScroll();
})();
