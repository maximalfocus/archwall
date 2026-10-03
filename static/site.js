(function () {
  var K = 'dl-lang', d = document.documentElement, b = document.getElementById('lang-toggle');
  var q = document.getElementById('q');

  function setLang(l, save) {
    d.setAttribute('data-lang', l);
    d.lang = l === 'en' ? 'en' : 'zh-CN';
    var t = d.getAttribute('data-title-' + l); if (t) document.title = t;
    document.querySelectorAll('img[data-alt-' + l + ']').forEach(function (im) { im.alt = im.getAttribute('data-alt-' + l); });
    if (q) q.placeholder = q.getAttribute('data-ph-' + l);
    if (b) b.textContent = l === 'en' ? '中' : 'EN';
    if (save) { try { localStorage.setItem(K, l); } catch (e) {} }
  }
  setLang(d.getAttribute('data-lang') === 'en' ? 'en' : 'zh', false);
  if (b) b.addEventListener('click', function () { setLang(d.getAttribute('data-lang') === 'en' ? 'zh' : 'en', true); });

  if (!q) return;
  var grid = document.getElementById('grid'), hits = document.getElementById('hits');
  var pager = document.querySelector('.pager'), original = grid.innerHTML, root = q.getAttribute('data-root');
  var index = null, loading = null;

  function load() {
    if (!loading) loading = fetch(q.getAttribute('data-index')).then(function (r) { return r.json(); })
      .then(function (j) { index = j; });
    return loading;
  }
  function e(s) { return String(s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }
  function card(p) {
    var u = root + 'p/' + p.s + '/';
    return '<a class="card" href="' + u + '"><figure><img src="' + u + e(p.f) + '" alt="' + e(d.getAttribute('data-lang') === 'en' ? p.ae : p.az) +
      '" data-alt-zh="' + e(p.az) + '" data-alt-en="' + e(p.ae) + '" loading="lazy"></figure><div class="cap">' +
      '<span class="i18n-zh" lang="zh-CN">' + e(p.tz) + '</span><span class="i18n-en" lang="en">' + e(p.te) + '</span>' +
      '<time>' + e(p.d) + '</time></div></a>';
  }
  function run() {
    var v = q.value.trim().toLowerCase();
    var url = new URL(location.href);
    if (v) url.searchParams.set('q', q.value.trim()); else url.searchParams.delete('q');
    history.replaceState(null, '', url);
    if (!v) { grid.innerHTML = original; hits.hidden = true; if (pager) pager.hidden = false; return; }
    load().then(function () {
      if (q.value.trim().toLowerCase() !== v) return;
      var terms = v.split(/\s+/);
      var res = index.filter(function (p) {
        var hay = (p.tz + ' ' + p.te + ' ' + p.t.join(' ') + ' ' + p.x).toLowerCase();
        return terms.every(function (t) { return hay.indexOf(t) >= 0; });
      });
      grid.innerHTML = res.map(card).join('');
      hits.hidden = false;
      hits.innerHTML = '<span class="i18n-zh">' + res.length + ' 篇匹配</span><span class="i18n-en">' + res.length + ' match' + (res.length === 1 ? '' : 'es') + '</span>';
      if (pager) pager.hidden = true;
    });
  }
  var timer;
  q.addEventListener('input', function () { clearTimeout(timer); timer = setTimeout(run, 120); });
  q.addEventListener('focus', load, { once: true });
  q.addEventListener('keydown', function (ev) { if (ev.key === 'Escape') { q.value = ''; run(); } });
  var init = new URLSearchParams(location.search).get('q');
  if (init) { q.value = init; run(); }
})();
