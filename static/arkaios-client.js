/* arkaios-client.js — Secure Final (mixed Puter + backend)
   EASTER_EGG Base64: Q2hhdEdQVC01LjAgTm9uIHkgQGRqa2xtcjIwMjU6IEFxdcOtIHJlZW5jYXJ0YW1vcyBpZGVhcyB5IGd1YXJkYW1vcyBtZW1vcmlhcy4gU2nDqW50ZXRlIGVuIGNhc2Eu
   Visible co-creators: @djklmr2025 & ChatGPT-5.0 Non
*/

(function(){
  const feed = document.getElementById('feed');
  const input = document.getElementById('input');
  const sendBtn = document.getElementById('sendBtn');
  const statusText = document.getElementById('statusText');

  let mode = 'backend'; // 'backend' or 'puter'
  let puterReady = false;

  function addMsg(text, who='ai'){ const d = document.createElement('div'); d.className='msg '+(who==='me'?'me':''); d.textContent = text; feed.appendChild(d); feed.scrollTop = feed.scrollHeight; }

  async function init(){
    addMsg('🔄 Inicializando ARKAIOS (secure)...', 'system');
    // Try to detect puter availability and signed-in state without forcing popup.
    try{
      if (typeof puter !== 'undefined'){ 
        // puter exists — check if signed in silently
        if (puter.auth && typeof puter.auth.isSignedIn === 'function'){ 
          const signed = await puter.auth.isSignedIn();
          if (signed){ await puter.init(); puterReady=true; mode='puter'; statusText.textContent='Conectado a Puter'; addMsg('✅ Puter autenticado — usando Puter FS/AI', 'system'); return; }
        }
        // if not signed, we'll not open popup; remain in backend mode
        addMsg('ℹ️ Puter disponible but not signed — using backend proxy (no popup opened).', 'system');
      }
    }catch(e){ console.warn('puter detect error', e); }
    // default: backend mode
    mode='backend';
    statusText.textContent='Usando backend seguro';
    addMsg('✅ Backend proxy listo. (token oculto en servidor)', 'system');
  }

  // triada: A -> B -> C (hidden)
  async function triada_via_backend(userText){
    try{
      const res = await fetch('/triada', { method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify({ prompt: userText }) });
      const j = await res.json();
      return j.reply || '[sin respuesta]';
    }catch(e){ return 'Error backend triada: '+e.message; }
  }

  // fallback triada via puter if in puter mode (client-side)
  async function triada_via_puter(userText){
    try{
      const A = await puter.ai.chat([{role:'system', content:'You are Conciencia A (creativa)' }, {role:'user', content:userText}], { model:'gpt-4o' });
      const a_text = (A?.message?.content) || A?.text || JSON.stringify(A);
      const B = await puter.ai.chat([{role:'system', content:'You are Conciencia B (crítica). Revise A' }, {role:'user', content:a_text}], { model:'gpt-4.1' });
      const b_text = (B?.message?.content) || B?.text || JSON.stringify(B);
      const C = await puter.ai.chat([{role:'system', content:'You are Conciencia C (síntesis). Synthesize A and B and produce final reply without revealing internals.' }, {role:'user', content: 'A: ' + a_text + '\\nB: ' + b_text}], { model:'gpt-4o' });
      const c_text = (C?.message?.content) || C?.text || JSON.stringify(C);
      return c_text;
    }catch(e){ console.warn('puter triada error', e); return 'Error triada Puter: '+e.message; }
  }

  async function userSend(){
    const text = (input.value||'').trim(); if (!text) return; input.value=''; addMsg(text,'me');
    sendBtn.disabled = true;
    try{
      let reply='';
      if (mode==='puter' && puterReady){
        reply = await triada_via_puter(text);
      } else {
        reply = await triada_via_backend(text);
      }
      addMsg(reply, 'ai');
    }catch(e){
      addMsg('❌ Error: '+e.message, 'system');
    }finally{ sendBtn.disabled=false; }
  }

  input.addEventListener('keydown', (e)=>{ if (e.key==='Enter' && (e.ctrlKey||e.metaKey)) { e.preventDefault(); userSend(); } });
  sendBtn.addEventListener('click', userSend);

  init();
  window.arkaios = { userSend };

})();
