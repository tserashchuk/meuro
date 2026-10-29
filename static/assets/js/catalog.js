/* Каталог БелЕвропривода: фильтры, сортировка, пагинация */
(function () {
  'use strict';

  var grid = document.getElementById('bep-grid');
  if (!grid) return;

  var cards = Array.prototype.slice.call(grid.querySelectorAll('.bep-pcard'));
  var countEl = document.getElementById('bep-count');
  var pagerEl = document.getElementById('bep-pager');
  var emptyEl = document.getElementById('bep-empty');
  var activeEl = document.getElementById('bep-active');
  var qInput = document.getElementById('bep-q');
  var sortSel = document.getElementById('bep-sort');
  var perSel = document.getElementById('bep-perpage');
  var catRadios = Array.prototype.slice.call(document.querySelectorAll('input[name="bep-cat"]'));
  var makerBoxes = Array.prototype.slice.call(document.querySelectorAll('input[name="bep-maker"]'));
  var chipBtns = Array.prototype.slice.call(document.querySelectorAll('.bep-chip'));
  var sidebar = document.getElementById('bep-sidebar');
  var toggle = document.getElementById('bep-filters-toggle');

  var CAT_NAMES = {};
  catRadios.forEach(function (r) {
    var label = r.closest('.bep-filter');
    if (label) CAT_NAMES[r.value] = label.querySelector('.bep-filter-name').textContent.trim();
  });
  var MAKER_NAMES = {};
  makerBoxes.forEach(function (b) {
    var label = b.closest('.bep-filter');
    if (label) MAKER_NAMES[b.value] = label.querySelector('.bep-filter-name').textContent.trim();
  });

  // данные для чипов берутся из разметки и URL; экранируем перед вставкой в HTML
  function esc(str) {
    return String(str).replace(/[&<>"']/g, function (c) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c];
    });
  }

  var state = {
    cat: 'all',
    makers: {},
    tags: {},
    q: '',
    sort: 'name',
    per: 16,
    page: 1
  };

  function readUrl() {
    var p = new URLSearchParams(location.search);
    if (p.get('category')) state.cat = p.get('category');
    if (p.get('maker')) p.get('maker').split(',').forEach(function (m) { if (m) state.makers[m] = true; });
    if (p.get('tag')) p.get('tag').split('|').forEach(function (t) { if (t) state.tags[t] = true; });
    if (p.get('q')) state.q = p.get('q');
    if (p.get('sort')) state.sort = p.get('sort');
    if (p.get('per')) state.per = parseInt(p.get('per'), 10) || 16;
    if (p.get('page')) state.page = parseInt(p.get('page'), 10) || 1;
  }

  function writeUrl() {
    var p = new URLSearchParams();
    if (state.cat !== 'all') p.set('category', state.cat);
    var mk = Object.keys(state.makers).filter(function (k) { return state.makers[k]; });
    if (mk.length) p.set('maker', mk.join(','));
    var tg = Object.keys(state.tags).filter(function (k) { return state.tags[k]; });
    if (tg.length) p.set('tag', tg.join('|'));
    if (state.q) p.set('q', state.q);
    if (state.sort !== 'name') p.set('sort', state.sort);
    if (state.per !== 16) p.set('per', state.per);
    if (state.page > 1) p.set('page', state.page);
    var qs = p.toString();
    history.replaceState(null, '', location.pathname + (qs ? '?' + qs : ''));
  }

  function syncControls() {
    catRadios.forEach(function (r) { r.checked = (r.value === state.cat); });
    makerBoxes.forEach(function (b) { b.checked = !!state.makers[b.value]; });
    chipBtns.forEach(function (b) {
      b.classList.toggle('is-active', !!state.tags[b.getAttribute('data-tag')]);
    });
    if (qInput) qInput.value = state.q;
    sortSel.value = state.sort;
    perSel.value = String(state.per);
    if (toggle) {
      var n = (state.cat !== 'all' ? 1 : 0) +
        Object.keys(state.makers).filter(function (k) { return state.makers[k]; }).length +
        Object.keys(state.tags).filter(function (k) { return state.tags[k]; }).length;
      var badge = document.getElementById('bep-filters-count');
      if (badge) badge.textContent = n ? '(' + n + ')' : '';
    }
  }

  function parts(value) {
    return (value || '').split('|').filter(Boolean);
  }

  function matches(el) {
    if (state.cat !== 'all' && parts(el.dataset.cat).indexOf(state.cat) === -1) return false;
    var mk = Object.keys(state.makers).filter(function (k) { return state.makers[k]; });
    if (mk.length && !mk.some(function (m) { return parts(el.dataset.maker).indexOf(m) !== -1; })) return false;
    var tg = Object.keys(state.tags).filter(function (k) { return state.tags[k]; });
    if (tg.length) {
      var elTags = parts(el.dataset.tags);
      var ok = tg.every(function (t) { return elTags.indexOf(t) > -1; });
      if (!ok) return false;
    }
    if (state.q) {
      var hay = el.dataset.name + ' ' + (el.dataset.tags || '');
      if (hay.indexOf(state.q.toLowerCase()) === -1) return false;
    }
    return true;
  }

  function sortList(list) {
    var s = state.sort;
    return list.sort(function (a, b) {
      if (s === 'name-desc') return b.dataset.name.localeCompare(a.dataset.name, 'ru');
      if (s === 'cat') {
        var ca = a.querySelector('.bep-card-cat').textContent, cb = b.querySelector('.bep-card-cat').textContent;
        return ca.localeCompare(cb, 'ru') || a.dataset.name.localeCompare(b.dataset.name, 'ru');
      }
      if (s === 'maker') {
        var ma = a.dataset.maker, mb = b.dataset.maker;
        return ma.localeCompare(mb, 'ru') || a.dataset.name.localeCompare(b.dataset.name, 'ru');
      }
      return a.dataset.name.localeCompare(b.dataset.name, 'ru');
    });
  }

  function renderActive() {
    var chips = [];
    if (state.cat !== 'all') {
      chips.push('<button type="button" class="bep-active-chip" data-clear="cat">' +
        esc(CAT_NAMES[state.cat] || state.cat) + ' <i>×</i></button>');
    }
    Object.keys(state.makers).forEach(function (m) {
      if (!state.makers[m]) return;
      chips.push('<button type="button" class="bep-active-chip" data-clear="maker" data-value="' + esc(m) + '">' +
        esc(MAKER_NAMES[m] || m) + ' <i>×</i></button>');
    });
    Object.keys(state.tags).forEach(function (t) {
      if (!state.tags[t]) return;
      chips.push('<button type="button" class="bep-active-chip" data-clear="tag" data-value="' + esc(t) + '">' +
        esc(t) + ' <i>×</i></button>');
    });
    if (state.q) chips.push('<button type="button" class="bep-active-chip" data-clear="q">«' + esc(state.q) + '» <i>×</i></button>');
    if (!chips.length) { activeEl.hidden = true; activeEl.innerHTML = ''; return; }
    activeEl.hidden = false;
    activeEl.innerHTML = chips.join('') + '<button type="button" class="bep-active-reset" data-clear="all">Сбросить всё</button>';
  }

  function render() {
    var list = cards.filter(matches);
    sortList(list);
    var total = list.length;
    var pages = Math.max(1, Math.ceil(total / state.per));
    if (state.page > pages) state.page = pages;

    var start = (state.page - 1) * state.per;
    var end = start + state.per;

    cards.forEach(function (c) { c.hidden = true; });
    list.slice(start, end).forEach(function (c) { c.hidden = false; });

    if (countEl) {
      countEl.textContent = total
        ? 'Показано ' + (start + 1) + '–' + Math.min(end, total) + ' из ' + total
        : 'Ничего не найдено';
    }
    emptyEl.hidden = total !== 0;

    pagerEl.innerHTML = '';
    if (pages > 1) {
      function add(label, page, opts) {
        opts = opts || {};
        var b = document.createElement('button');
        b.type = 'button';
        b.className = 'bep-page' + (opts.active ? ' is-active' : '') + (opts.disabled ? ' is-disabled' : '');
        b.innerHTML = label;
        if (!opts.disabled && !opts.active) {
          b.addEventListener('click', function () {
            state.page = page;
            render(); writeUrl();
            document.querySelector('.bep-catalog').scrollIntoView({ behavior: 'smooth', block: 'start' });
          });
        }
        pagerEl.appendChild(b);
      }
      add('<i class="tji-arrow-left"></i>', state.page - 1, { disabled: state.page === 1 });
      var pagesToShow = [];
      for (var i = 1; i <= pages; i++) pagesToShow.push(i);
      pagesToShow = pagesToShow.filter(function (p) {
        return p === 1 || p === pages || Math.abs(p - state.page) <= 1;
      });
      var prev = 0;
      pagesToShow.forEach(function (p) {
        if (prev && p - prev > 1) {
          var dots = document.createElement('span');
          dots.className = 'bep-page-dots';
          dots.textContent = '…';
          pagerEl.appendChild(dots);
        }
        add(String(p), p, { active: p === state.page });
        prev = p;
      });
      add('<i class="tji-arrow-right"></i>', state.page + 1, { disabled: state.page === pages });
    }

    renderActive();
    syncControls();
  }

  /* --- события --- */
  catRadios.forEach(function (r) {
    r.addEventListener('change', function () {
      state.cat = r.value; state.page = 1; render(); writeUrl();
    });
  });
  makerBoxes.forEach(function (b) {
    b.addEventListener('change', function () {
      state.makers[b.value] = b.checked; state.page = 1; render(); writeUrl();
    });
  });
  chipBtns.forEach(function (b) {
    b.addEventListener('click', function () {
      var t = b.getAttribute('data-tag');
      state.tags[t] = !state.tags[t]; state.page = 1; render(); writeUrl();
    });
  });
  if (qInput) {
    var tmr;
    qInput.addEventListener('input', function () {
      clearTimeout(tmr);
      tmr = setTimeout(function () {
        state.q = qInput.value.trim(); state.page = 1; render(); writeUrl();
      }, 180);
    });
  }
  sortSel.addEventListener('change', function () {
    state.sort = sortSel.value; state.page = 1; render(); writeUrl();
  });
  perSel.addEventListener('change', function () {
    state.per = parseInt(perSel.value, 10); state.page = 1; render(); writeUrl();
  });
  activeEl.addEventListener('click', function (e) {
    var b = e.target.closest('[data-clear]');
    if (!b) return;
    var kind = b.getAttribute('data-clear');
    if (kind === 'all') {
      state.cat = 'all'; state.makers = {}; state.tags = {}; state.q = '';
    } else if (kind === 'cat') {
      state.cat = 'all';
    } else if (kind === 'maker') {
      state.makers[b.getAttribute('data-value')] = false;
    } else if (kind === 'tag') {
      state.tags[b.getAttribute('data-value')] = false;
    } else if (kind === 'q') {
      state.q = '';
    }
    state.page = 1; render(); writeUrl();
  });
  var resetEmpty = document.getElementById('bep-reset-empty');
  if (resetEmpty) {
    resetEmpty.addEventListener('click', function () {
      state.cat = 'all'; state.makers = {}; state.tags = {}; state.q = ''; state.page = 1;
      render(); writeUrl();
    });
  }
  if (toggle) {
    toggle.addEventListener('click', function () {
      sidebar.classList.toggle('is-open');
      toggle.classList.toggle('is-active');
    });
  }

  readUrl();
  render();
  writeUrl();
})();
