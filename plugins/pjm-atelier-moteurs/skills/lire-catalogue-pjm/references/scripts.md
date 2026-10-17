# Catalog scripts (run with the Claude in Chrome JavaScript tool)

Both scripts replace the page body with a `<pre id="dump">` containing the JSON. Read it with `get_page_text`, then reload the page.

## Resources (page `{pjmUrl}/Production`)

```js
const ds = jQuery('[data-role=grid]').data('kendoGrid').dataSource;
await new Promise(r => { ds.one('change', r); ds.pageSize(500); });
const res = [];
for (const x of ds.data()) {
  if (x.IsDeleted) continue;
  const r = await fetch('/Processes/Steps/' + x.Id, {method:'POST', headers:{'Content-Type':'application/x-www-form-urlencoded','X-Requested-With':'XMLHttpRequest'}, body:'sort=&page=1&pageSize=500&group=&filter='});
  const j = await r.json();
  res.push({name: x.Name.trim(), dept: x.DepartmentName, kind: x.ProductionType, processes: j.Data.filter(p => !p.IsDeleted).map(p => p.Name)});
}
const doc = {resources: res, source: location.origin, readAt: new Date().toISOString().slice(0,10)};
document.body.innerHTML = '<pre id="dump"></pre>';
document.getElementById('dump').textContent = JSON.stringify(doc);
res.length
```

If `ds.one('change')` never resolves (page size already 500), call `ds.read()` instead.

## Materials (page `{pjmUrl}/Materials`)

```js
const r = await fetch('/Materials/_Index', {method:'POST', headers:{'Content-Type':'application/x-www-form-urlencoded','X-Requested-With':'XMLHttpRequest'}, body:'sort=&page=1&pageSize=5000&group=&filter='});
const j = await r.json();
const mats = j.Data.filter(x => !x.IsDeleted);
const cats = {};
for (const x of mats) {
  const k = x.MaterialCategory + (x.MaterialSubCategory ? ' > ' + x.MaterialSubCategory : '');
  (cats[k] = cats[k] || []).push(x.Name);
}
const categories = Object.entries(cats).sort((a,b) => a[0].localeCompare(b[0])).map(([category, items]) => ({category, count: items.length, items: items.length <= 120 ? [...new Set(items)].sort() : []}));
const doc = {categories, total: mats.length, source: location.origin, readAt: new Date().toISOString().slice(0,10)};
document.body.innerHTML = '<pre id="dump"></pre>';
document.getElementById('dump').textContent = JSON.stringify(doc);
mats.length + ' materials, ' + categories.length + ' categories'
```
