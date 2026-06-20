// 通用工具
async function postJSON(url, body){
  const r = await fetch(url, {method:'POST', headers:{'Content-Type':'application/json'},
    body: JSON.stringify(body)});
  return r.json();
}
function el(tag, cls, text){
  const e = document.createElement(tag);
  if(cls) e.className = cls;
  if(text!=null) e.textContent = text;
  return e;
}
function addMsg(box, cls, text){
  const m = el('div', 'msg '+cls, text);
  box.appendChild(m);
  box.scrollTop = box.scrollHeight;
  return m;
}
