/* Временная обёртка: рендер страницы в iframe нужной ширины и отчёт о переполнении */
var W = parseInt(location.hash.slice(1) || '390', 10);
var H = 12000;
document.addEventListener('DOMContentLoaded', function () {
  var wrap = document.createElement('div');
  wrap.style.cssText = 'margin:0;width:' + W + 'px;overflow:hidden';
  var f = document.createElement('iframe');
  f.src = 'PAGE';
  f.style.cssText = 'width:' + W + 'px;height:' + H + 'px;border:0;display:block';
  f.addEventListener('load', function () {
    try {
      var doc = f.contentDocument, win = f.contentWindow;
      var vw = doc.documentElement.clientWidth;
      var bad = [];
      doc.querySelectorAll('body *').forEach(function (el) {
        var r = el.getBoundingClientRect();
        if (r.width > 0 && (r.right > vw + 1 || r.left < -1)) {
          var cs = win.getComputedStyle(el);
          if (cs.position === 'fixed' && r.left < 0) return;
          if (el.closest('.marquee-slider, .swiper')) return;
          bad.push(el.tagName.toLowerCase() + '.' + (el.className || '').toString().slice(0, 44) +
                   ' [' + Math.round(r.left) + '..' + Math.round(r.right) + ']');
        }
      });
      var pre = document.createElement('pre');
      pre.id = 'ovf';
      pre.textContent = 'VW=' + vw + ' scrollW=' + doc.documentElement.scrollWidth +
        ' scrollH=' + doc.documentElement.scrollHeight + '\n' + bad.slice(0, 30).join('\n');
      document.body.appendChild(pre);
      var h = doc.documentElement.scrollHeight;
      f.style.height = h + 'px';
    } catch (e) {
      var p = document.createElement('pre');
      p.id = 'ovf';
      p.textContent = 'ERR ' + e;
      document.body.appendChild(p);
    }
  });
  wrap.appendChild(f);
  document.body.appendChild(wrap);
});
