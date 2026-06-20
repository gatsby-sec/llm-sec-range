// ============ 炫酷背景：矩阵雨 + 扫描线 ============
(function(){
  // 扫描线遮罩
  const scan = document.createElement('div');
  scan.className = 'scan';
  document.body.appendChild(scan);

  // 矩阵雨
  const cv = document.createElement('canvas');
  cv.id = 'matrix';
  document.body.appendChild(cv);
  const ctx = cv.getContext('2d');
  const chars = 'アカサタナハマヤラ0123456789ABCDEF<>{}[]#$%&LLMSEC';
  let cols, drops, fs = 14;
  function resize(){
    cv.width = innerWidth; cv.height = innerHeight;
    cols = Math.floor(cv.width / fs);
    drops = Array(cols).fill(0).map(()=>Math.random()*-100);
  }
  resize(); addEventListener('resize', resize);
  function draw(){
    ctx.fillStyle = 'rgba(5,7,13,0.10)';
    ctx.fillRect(0,0,cv.width,cv.height);
    ctx.font = fs + 'px monospace';
    for(let i=0;i<cols;i++){
      const c = chars[Math.floor(Math.random()*chars.length)];
      const x = i*fs, y = drops[i]*fs;
      ctx.fillStyle = Math.random()>0.97 ? '#22d3ee' : '#00ffae';
      ctx.fillText(c, x, y);
      if(y > cv.height && Math.random() > 0.975) drops[i] = 0;
      drops[i] += 0.6;
    }
    requestAnimationFrame(draw);
  }
  draw();
})();

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
