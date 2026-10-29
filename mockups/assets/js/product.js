/* Карточка товара: галерея и табы */
(function () {
  'use strict';

  var main = document.getElementById('bep-gmain');
  var thumbs = Array.prototype.slice.call(document.querySelectorAll('.bep-gthumb'));
  thumbs.forEach(function (t) {
    t.addEventListener('click', function () {
      var src = t.getAttribute('data-src');
      if (!src || !main) return;
      main.src = src;
      thumbs.forEach(function (x) { x.classList.remove('is-active'); });
      t.classList.add('is-active');
    });
  });

  var tabs = Array.prototype.slice.call(document.querySelectorAll('.bep-tab'));
  tabs.forEach(function (tab) {
    tab.addEventListener('click', function () {
      var key = tab.getAttribute('data-tab');
      tabs.forEach(function (t) { t.classList.toggle('is-active', t === tab); });
      Array.prototype.slice.call(document.querySelectorAll('.bep-tabpane')).forEach(function (p) {
        p.classList.toggle('is-active', p.id === 'pane-' + key);
      });
    });
  });
})();
