# PJM helper scripts (Claude in Chrome JavaScript tool)

Run them on a page of the customer's PJM instance (same origin, user already signed in). Paste the `H` helper block first in each JavaScript call (the page keeps no state between calls if it navigates). Endpoints and fields were verified on PJM on 16/10/2026; see `procedure-construction.md`.

## Output rules
- The tool's output is blocked when it contains `&` or `x=y` patterns: return `JSON.stringify(x).replace(/[&=]/g,' ')`, or write long output into a `<pre id="dump">` and read it with `get_page_text`.
- Every POST answers JSON `{"ErrorCode":0,…}` on success. An HTML answer means the server rejected the input (most often `<` without spaces in a formula, or an expired session).
- Always re-read the grid after a batch of writes and compare with what was expected.

## Helper block `H`

```js
const H = {
  Z: '00000000-0000-0000-0000-000000000000',
  hdr: {'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8','X-Requested-With':'XMLHttpRequest'},
  enc(o){ return Object.entries(o).map(([k,v]) => encodeURIComponent(k)+'='+encodeURIComponent(v ?? '')).join('&'); },
  async doc(url){ const t = await (await fetch(url)).text(); return new DOMParser().parseFromString(t,'text/html'); },
  // all named inputs of the first form of a page (hidden fields, token, SubscriberId…)
  async form(url, sel='form'){ const d = await H.doc(url); const f = d.querySelector(sel); const o = {};
    f.querySelectorAll('input[name],select[name],textarea[name]').forEach(e => { if((e.type==='checkbox'||e.type==='radio') && !e.checked) return; if(!(e.name in o)) o[e.name] = e.value; });
    return o; },
  async post(url, data){ const r = await fetch(url,{method:'POST',headers:H.hdr,body:H.enc(data)}); const t = await r.text(); try { return JSON.parse(t); } catch(e){ return {ErrorCode:-1, html:t.slice(0,300)}; } },
  async grid(url, extra={}){ return (await H.post(url, {sort:'',page:1,pageSize:2000,group:'',filter:'',...extra})).Data || []; },
  token(){ return document.querySelector('input[name=__RequestVerificationToken]')?.value; }
};
```

## Choices of an Options component

```js
// cid = Options component id; choices = [{name, markup}]
async function addOpts(cid, choices){
  const out = [];
  for (const [i,c] of choices.entries()){
    const f = await H.form('/productengines/addoption/' + cid);
    const r = await H.post('/productengines/saveoption', {...f, __RequestVerificationToken: f.__RequestVerificationToken, Id: cid, ComponentId: cid, cid, Sequence: i+1, CreateDate: '1/1/0001 12:00:00 AM', OptionName: c.name, Markup: c.markup ?? 0});
    out.push(c.name + ':' + r.ErrorCode);
  }
  return out;
}
// read the choice ids: links "EditOption" on /ProductEngines/ComponentEdit/{cid}
async function choiceIds(cid){
  const d = await H.doc('/ProductEngines/ComponentEdit/' + cid);
  return [...d.querySelectorAll('a[href*="ditOption"]')].map(a => ({name: a.closest('tr')?.innerText.trim().split('\t')[0], id: a.href.split('/').pop().split('?')[0]}));
}
```
If `choiceIds` returns nothing (layout differs), open the ComponentEdit page and read the EditOption links with `find` / `read_page`.

## Production line (choice of an Option, or a Calculation component)

```js
// wf = item of #ddlworkflowComponents: {Id, Name:"Process (resource)", Group:resource}
async function addProd(ownerId, wf, qtyFormula, nupFormula='', seq=1, from=0, to=0, instr=''){
  return H.post('/PECompWorkflows/SaveComponentProduction', {
    __RequestVerificationToken: H.token(), ComponentProductionId: H.Z, ComponentId: ownerId, cid: ownerId, OptionId: ownerId,
    FromQty: from, ToQty: to, WorkflowComponentId: wf.Id, WorkflowComponentId_input: wf.Name, Seq: seq,
    Instructions: instr, QuantityCalculation: qtyFormula, NumberUpExpression: nupFormula });
}
// list of processes, on a page where the production form is open (ComponentEdit / EditOption → Production → Ajouter)
function workflows(){ return jQuery('#ddlworkflowComponents').data('kendoComboBox').dataSource.data().map(x => ({Id:x.Id, Name:x.Name, Group:x.Group})); }
```
For « Travail manuel » resources the list holds the resource entry first and then its processes: pick the PROCESS entry (e.g. « Oeuillets (oeuillets) »). Saving the resource entry answers OK but creates nothing.

## Material line in a choice

```js
async function addMat(ownerId, mat, qtyFormula, nupFormula='', weightFormula='', lineId=null, from=0, to=0, pos=0, instr=''){
  return H.post('/PECompMaterials/SaveComponentMaterial', {
    __RequestVerificationToken: H.token(), Id: lineId || H.Z, ComponentId: ownerId, cid: ownerId, OptionId: ownerId,
    FromQty: from, ToQty: to, MaterialId: mat.Id, MaterialId_input: mat.Name, ReportPosition: pos, Instructions: instr,
    QuantityCalculation: qtyFormula, NumberUpExpression: nupFormula, WeightCalculation: weightFormula });
}
// material ids by exact name
async function matIds(names){
  const all = await H.grid('/Materials/_Index');
  return names.map(n => { const m = all.find(x => x.Name.trim() === n.trim() && !x.IsDeleted); return m ? {Id:m.Id, Name:m.Name} : {Name:n, missing:true}; });
}
```
ErrorCode 437 = same material twice in one choice, or a formula over 1400 characters.

## Suppression (hide component X when component Y = value)

```js
async function values(X, Y){ return H.post('/PECompSuppressions/GetOptionValues', {cid: X, oid: Y}); } // "--Sélectionner--" = select_one_id
async function supp(E, X, xName, Y, yName, value, valueName, subscriberId){
  return H.post('/PECompSuppressions/Save?compId=' + X + '&engineId=' + E, {
    __RequestVerificationToken: H.token(), Id: H.Z, EngineId: E, ComponentId: X, SubscriberId: subscriberId,
    SuppressedComponentId: Y, Name: yName, Value: value, ComponentName: xName, SuppressedValueName: valueName,
    SuppressedComponentType: 0, MaterialId: H.Z });
}
```
`subscriberId`: read it once from `H.form('/productengines/addoption/' + anyOptionCid)`.
Rule: if the hiding condition is the first choice of a forced option, add the same suppression with `select_one_id`.

## Reading an engine (import / update) – validated 17/10/2026
All reads are POST grids (body `page 1`, `pageSize 500`), same origin:
- components: ids in the `ComponentEdit/{cid}` links of `/ProductEngines/Edit/{E}`; fields (Name, Prompt, ComponentType, IsRequired, HideFromPublicView, MinQty, MaxQty, DefaultQty) = named inputs of the form on `/ProductEngines/ComponentEdit/{cid}` (fetch + DOMParser);
- choices: `/PEOptions/_Index?cid={cid}` → Id, OptionName, Markup, Sequence;
- production lines: `/PECompWorkflows/_Index?cid={choiceId or calcId}` → Id, WorkflowComponentName (« Process (unit) », the parenthesis is the UNIT, not the resource), QtyFrom, QtyTo, Seq, QuantityCalculation, NumberUpExpression; resource = `WorkflowComponent.Equipment.Name`;
- material lines: `/PECompMaterials/_Index?cid={choiceId}` → Id, MaterialName, MaterialId, QuantityCalculation, NumberUpExpression, WeightCalculation, FromQty, ToQty;
- suppressions: `/PECompSuppressions/_Index?compId={cid}&compType={Options|Quantity|…}&engineId={E}` → Id, SuppressedComponentId, Name, Value (choice id in UPPER case, or select_one_id), SuppressedValueName.
Engine fields: form of `/ProductEngines/Edit/{E}` (Name, ProductEngineTypeId = category, MinPrice, MaxPrice, IsMultipleQuantityApplicable).

Transfer to the Atelier without errors: build the whole sheet in the page (`window.SHEET`), show it in a `<pre>`, read it with `get_page_text`, rebuild it locally, then compare a SHA-256 fingerprint computed in the page and locally before writing with ArtifactData. Formulas longer than ~400 characters can stay in PJM (`"[PJM]"` in the sheet) to keep the sheet small.

## Report position of production lines (Seq) and form order – validated 17/10/2026

```js
// position of a production line in the report (see « Conventions » in procedure-construction.md)
function seqOf(name){ // name = WorkflowComponentName « Process (unit) »
  if (/pré-?presse|fichier|CTP|plan(ch|que)/i.test(name)) return 1;
  if (/pellic|lamin|vernis|actimail/i.test(name)) return 3;
  if (/impres|couleur|N&B|quadri|recto|offset/i.test(name)) return 2;
  if (/massicot|coupe|cortes|guillotin|découp|cut/i.test(name)) return 4;
  if (/rain|hendid|perfor|coins/i.test(name)) return 5;
  if (/pli|plis|plega|d[ií]ptic|tr[ií]ptic/i.test(name)) return 6;
  if (/agraf|piq|reliure|dos carré|wire|spiral|cosedora|grapad/i.test(name)) return 7;
  if (/oeillet|œillet|ourlet|fourreau|soudure|couture/i.test(name)) return 8;
  return 9;
} // keep only the families present: renumber 1..n in this order before saving
// fix existing lines: resend every field with ComponentProductionId = line Id
async function setSeq(ownerId, line, seq){
  return H.post('/PECompWorkflows/SaveComponentProduction', {__RequestVerificationToken: H.token(), ComponentProductionId: line.Id,
    ComponentId: ownerId, cid: ownerId, OptionId: ownerId, FromQty: line.QtyFrom, ToQty: line.QtyTo, WorkflowComponentId: line.WorkflowComponentId,
    WorkflowComponentId_input: line.WorkflowComponentName, Seq: seq, Instructions: line.Instructions || '',
    QuantityCalculation: line.QuantityCalculation || '', NumberUpExpression: line.NumberUpExpression || ''});
}
// form order (same call as PJM drag and drop); ids = every component id, in the wanted order
async function orderComponents(ids){
  const r = await fetch('/ProductEngines/UpdateCompSequence/', {method:'POST', headers:{'Content-Type':'application/json; charset=utf-8','X-Requested-With':'XMLHttpRequest'}, body: JSON.stringify({newSettings: ids})});
  return r.text(); // {"message":"Success"}
}
```
Use `H.token()` on a page that has a token, or read it from `H.form('/productengines/addoption/' + anyOptionCid)`.

## Running a test case
Open the engine's Test page (button « Test » of the engine), fill the quantities and choices of the case, click « Calculer le plan de production », then read the total (HT) with `get_page_text`.
Filling by script (validated 17/10/2026): each field is `#component-{componentId with _ instead of -}` (Kendo DropDownList; materials by Id, choices by text).
```js
function setC(cid, text, matId){ const e = document.getElementById('component-' + cid.replace(/-/g,'_')); const w = jQuery(e).data('kendoDropDownList');
  const it = w.dataSource.data().find(x => matId ? x[w.options.dataValueField] === matId : (x[w.options.dataTextField]||'').trim() === text);
  w.value(it[w.options.dataValueField]); w.trigger('change'); jQuery(e).trigger('change'); } // jQuery change = recompute hidden questions
```
Set Format / Grammage first, wait ~0.7 s between choices, then quantities (`kendoNumericTextBox` if present), then click the button (an `input`/`button` whose text is « Calculer le plan de production ») and wait ~5 s. Results: « Prix hors taxes » line, material blocks (`numberup`, `qty`) and equipment blocks (process / resource). The Test page shows every component (suppressions are not visible there) but the calculation respects them.
