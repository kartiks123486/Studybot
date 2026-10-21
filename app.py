import os
import json
import time
from datetime import datetime, timedelta, timezone
import urllib.request
import urllib.error
from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

HTML = r'''<!DOCTYPE html>
<html lang="en">
<head>
<link rel="manifest" href="/manifest.json">
<meta name="theme-color" content="#0b1020">
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="theme-color" content="#080b16">
<title>StudyBot AI</title>
<style>
:root{--bg:#080b16;--panel:#10162a;--panel2:#151d35;--cyan:#42e8ff;--purple:#9b6dff;--text:#edf3ff;--muted:#8d9ab8;--border:rgba(129,153,220,.18)}
*{box-sizing:border-box}body{margin:0;min-height:100dvh;background:radial-gradient(ellipse at 15% 0%,#17234b 0%,transparent 42%),radial-gradient(ellipse at 100% 65%,#241346 0%,transparent 35%),var(--bg);color:var(--text);font-family:system-ui,-apple-system,Arial,sans-serif}button,textarea{font:inherit}button{cursor:pointer}.app{display:flex;min-height:100dvh;max-width:1500px;margin:auto}.sidebar{width:260px;flex-shrink:0;padding:20px 14px;background:rgba(8,11,22,.92);border-right:1px solid var(--border);display:flex;flex-direction:column;gap:17px;z-index:5}.brand{display:flex;align-items:center;gap:11px;padding:5px 7px 14px}.logo{width:43px;height:43px;border-radius:14px;display:grid;place-items:center;font-size:23px;background:linear-gradient(135deg,#173e65,#47236e);border:1px solid #42e8ff77;box-shadow:0 0 22px #42e8ff24}.brand-name{font-size:20px;font-weight:850;letter-spacing:-.5px}.brand-name span,.gradient{color:var(--cyan);text-shadow:0 0 18px #42e8ff35}.status{color:#7dfac6;font-size:10px;margin-top:3px}.new-chat{width:100%;border:1px solid #42e8ff65;background:linear-gradient(110deg,#10334a,#28204b);color:white;padding:13px;border-radius:13px;font-weight:700}.new-chat:hover{box-shadow:0 0 20px #42e8ff35}.section-label{font-size:11px;color:var(--muted);letter-spacing:1.6px;padding:4px 8px;text-transform:uppercase}.history-list{display:flex;flex-direction:column;gap:5px;overflow-y:auto}.history-item{width:100%;padding:11px;border:1px solid transparent;border-radius:10px;background:transparent;color:#c9d4ed;text-align:left;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;font-size:13px}.history-item:hover,.history-item.active{background:#18213b;border-color:var(--border);color:var(--cyan)}.side-bottom{margin-top:auto;color:var(--muted);font-size:12px;padding:12px 8px;border-top:1px solid var(--border)}.main{flex:1;min-width:0;min-height:100dvh;display:flex;flex-direction:column;padding:18px 25px 12px}.topbar{display:flex;align-items:center;gap:11px;padding-bottom:15px;border-bottom:1px solid var(--border)}.menu-btn{display:none;color:white;background:var(--panel);border:1px solid var(--border);padding:9px 12px;border-radius:10px}.top-title{font-weight:750;font-size:16px}.top-subtitle{color:var(--muted);font-size:11px;margin-top:3px}.online-dot{width:8px;height:8px;display:inline-block;background:#62ffc0;border-radius:50%;box-shadow:0 0 10px #62ffc0;margin-right:6px}.top-status{margin-left:auto;color:#a4b6d5;font-size:12px}.chat-area{flex:1;width:100%;max-width:900px;margin:0 auto;display:flex;flex-direction:column;gap:18px;padding:24px 0 20px}.welcome{text-align:center;padding:clamp(18px,6vh,65px) 10px 12px}.orb{width:78px;height:78px;margin:0 auto 19px;display:grid;place-items:center;border-radius:25px;font-size:37px;background:linear-gradient(135deg,#102d4b,#302052);border:1px solid #6d80ff77;box-shadow:0 0 25px #42e8ff25,inset 0 0 20px #9b6dff15;animation:float 3s ease-in-out infinite}@keyframes float{0%,100%{transform:translateY(0)}50%{transform:translateY(-6px)}}.welcome h1{font-size:clamp(25px,4vw,38px);margin:0 0 10px;letter-spacing:-1px}.welcome p{color:var(--muted);font-size:14px;margin:0;line-height:1.7}.suggestions{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:10px;max-width:620px;margin:24px auto 0}.suggestion{padding:14px;background:linear-gradient(140deg,#141d35,#101528);color:var(--text);border:1px solid var(--border);border-radius:15px;text-align:left;transition:.2s}.suggestion:hover{border-color:#42e8ff77;transform:translateY(-2px);box-shadow:0 0 20px #42e8ff12}.suggestion strong{display:block;font-size:13px}.suggestion small{color:var(--muted);display:block;margin-top:6px}.message{display:flex;gap:10px;align-items:flex-start;animation:appear .25s ease-out}@keyframes appear{from{opacity:0;transform:translateY(7px)}to{opacity:1;transform:translateY(0)}}.message.user{flex-direction:row-reverse}.avatar{flex-shrink:0;width:34px;height:34px;display:grid;place-items:center;border-radius:11px;background:#182541;border:1px solid var(--border);font-size:16px}.message.assistant .avatar{border-color:#42e8ff55;box-shadow:0 0 12px #42e8ff12}.bubble{max-width:min(82%,700px);padding:12px 15px;border-radius:5px 16px 16px 16px;background:#151e35;border:1px solid var(--border);color:#e7edff;font-size:14px;line-height:1.75;overflow-wrap:anywhere;white-space:pre-wrap}.user .bubble{background:linear-gradient(135deg,#173b59,#30204f);border-color:#42e8ff45;border-radius:16px 5px 16px 16px}.typing-dots{display:flex;gap:5px;padding:7px 3px}.typing-dots span{width:7px;height:7px;border-radius:50%;background:var(--cyan);animation:pulse 1s infinite ease-in-out}.typing-dots span:nth-child(2){animation-delay:.15s}.typing-dots span:nth-child(3){animation-delay:.3s}@keyframes pulse{0%,60%,100%{opacity:.35;transform:translateY(0)}30%{opacity:1;transform:translateY(-5px)}}.composer-wrap{width:100%;max-width:900px;margin:0 auto;position:sticky;bottom:0;padding:10px 0 3px;background:linear-gradient(180deg,transparent,var(--bg) 18%)}.composer{display:flex;gap:9px;align-items:flex-end;padding:9px;border:1px solid #6378b54d;background:#11172aee;border-radius:18px;box-shadow:0 0 25px #0004,0 0 20px #42e8ff08}.composer:focus-within{border-color:#42e8ff9c;box-shadow:0 0 22px #42e8ff13}#prompt{flex:1;min-width:0;max-height:145px;resize:none;border:0;outline:0;color:white;background:transparent;padding:10px 8px;font-size:14px;line-height:1.5}#prompt::placeholder{color:#8391b0}.send-btn{min-width:44px;height:44px;border:0;border-radius:13px;background:linear-gradient(135deg,#42e8ff,#8b8aff);color:#07101c;font-size:22px;font-weight:900;box-shadow:0 0 17px #42e8ff30}.send-btn:disabled{opacity:.45;cursor:not-allowed}.disclaimer{text-align:center;color:#65718e;font-size:10px;padding:9px 4px 0}
@media(min-width:1000px){.main{padding-left:40px;padding-right:40px}}@media(max-width:700px){.sidebar{position:fixed;top:0;bottom:0;left:0;width:min(285px,85vw);transform:translateX(-105%);transition:transform .25s ease;box-shadow:15px 0 40px #0006}.sidebar.open{transform:translateX(0)}.menu-btn{display:block}.main{padding:12px 12px 9px}.topbar{padding-bottom:12px}.chat-area{padding-top:12px;gap:15px}.welcome{padding-top:7vh}.orb{width:70px;height:70px;font-size:33px}.welcome h1{font-size:27px}.welcome p{font-size:13px}.suggestions{gap:8px;margin-top:20px}.suggestion{padding:12px 10px}.bubble{font-size:14px;max-width:88%;padding:11px 12px}.avatar{width:30px;height:30px;font-size:15px}.top-status{font-size:10px}}@media(max-width:360px){.suggestions{grid-template-columns:1fr}}@media(prefers-reduced-motion:reduce){*,*::before,*::after{animation-duration:.01ms!important;transition-duration:.01ms!important}}
</style>
</head>
<body>
<div class="app">
<aside class="sidebar" id="sidebar">
  <div class="brand"><div class="logo">🤖</div><div><div class="brand-name">Study<span>Bot</span> AI</div><div class="status">● NEURAL SYSTEM ONLINE</div></div></div>
  <button class="new-chat" id="newChat">＋ &nbsp; New Chat</button>
  <div class="section-label">Recent chats</div><div class="history-list" id="historyList"></div>
  <div class="side-bottom">⚡ StudyBot AI · Your AI companion</div>
</aside>
<main class="main">
<header class="topbar"><button class="menu-btn" id="menuBtn" aria-label="Open history">☰</button><div class="logo" style="width:38px;height:38px;font-size:20px">🤖</div><div><div class="top-title">StudyBot <span class="gradient">AI</span></div><div class="top-subtitle">Your personal AI assistant</div></div><div class="top-status"><span class="online-dot"></span>Ready</div></header>
<section class="chat-area" id="chatArea" aria-live="polite"></section>
<div class="composer-wrap"><form class="composer" id="chatForm"><textarea id="prompt" rows="1" maxlength="10000" placeholder="Ask StudyBot anything..." aria-label="Your message"></textarea><button type="button" id="voiceBtn" aria-label="Start voice chat" style="height:44px;padding:0 13px;border:1px solid #42e8ff66;border-radius:13px;background:#17243b;color:#fff;font-size:14px;white-space:nowrap">🎙️ Voice</button><button class="send-btn" id="sendBtn" type="submit" aria-label="Send message">↑</button></form><div id="voiceStatus" class="disclaimer">Voice chat: off</div><div class="disclaimer">StudyBot can make mistakes. Verify important information.</div></div>
</main></div>
<script>
(() => {
const $=id=>document.getElementById(id), chatArea=$('chatArea'), prompt=$('prompt'), sendBtn=$('sendBtn'), historyList=$('historyList'), sidebar=$('sidebar');
const STORAGE_KEY='studybot_neon_chats_v1'; let chats=[],activeId=null,busy=false;
try{const saved=JSON.parse(localStorage.getItem(STORAGE_KEY)||'[]');if(Array.isArray(saved))chats=saved.filter(c=>c&&typeof c.id==='string'&&Array.isArray(c.messages));}catch(e){chats=[];}
function save(){try{localStorage.setItem(STORAGE_KEY,JSON.stringify(chats));}catch(e){console.warn('Chat history could not be saved:',e);}}
function currentChat(){return chats.find(c=>c.id===activeId);}
function makeChat(){if(busy)return;const c={id:Date.now().toString()+Math.random().toString(36).slice(2,7),title:'New conversation',messages:[],updated:Date.now()};chats.unshift(c);activeId=c.id;save();renderHistory();renderChat();prompt.focus();sidebar.classList.remove('open');}
function safeTitle(s){return String(s||'').replace(/\s+/g,' ').trim().slice(0,36)||'New conversation';}
function renderHistory(){historyList.replaceChildren();chats.sort((a,b)=>(b.updated||0)-(a.updated||0));if(!chats.length){const el=document.createElement('div');el.className='history-item';el.textContent='Your chats will appear here';el.style.color='var(--muted)';historyList.appendChild(el);return;}chats.forEach(c=>{const b=document.createElement('button');b.className='history-item'+(c.id===activeId?' active':'');b.textContent='▹  '+safeTitle(c.title);b.title=c.title;b.onclick=()=>{if(busy)return;activeId=c.id;renderHistory();renderChat();sidebar.classList.remove('open');};historyList.appendChild(b);});}
function showWelcome(){const w=document.createElement('div');w.className='welcome';const orb=document.createElement('div');orb.className='orb';orb.textContent='✦';const h=document.createElement('h1');h.append('Welcome to ');const span=document.createElement('span');span.className='gradient';span.textContent='StudyBot';h.appendChild(span);const p=document.createElement('p');p.textContent='Your ideas. Your questions. One AI assistant.';const cards=document.createElement('div');cards.className='suggestions';[['📚','Study & Learn','Explain a difficult topic'],['💻','Coding Help','Build and debug code'],['💡','Creative Ideas','Brainstorm something new'],['✍️','Writing Assistant','Write, improve and create']].forEach(([ico,title,sub])=>{const b=document.createElement('button');b.className='suggestion';const strong=document.createElement('strong');strong.textContent=ico+'  '+title;const small=document.createElement('small');small.textContent=sub;b.append(strong,small);b.onclick=()=>{prompt.value=title==='Study & Learn'?'Explain a difficult topic':title==='Coding Help'?'Help me with coding':title==='Creative Ideas'?'Give me some creative ideas':'Help me write something';prompt.focus();autoSize();};cards.appendChild(b);});w.append(orb,h,p,cards);chatArea.appendChild(w);}
function addMessage(role,text){const row=document.createElement('div');row.className='message '+role;const av=document.createElement('div');av.className='avatar';av.textContent=role==='user'?'👤':'🤖';const bubble=document.createElement('div');bubble.className='bubble';bubble.textContent=text;row.append(av,bubble);chatArea.appendChild(row);return row;}
function renderChat(){chatArea.replaceChildren();const c=currentChat();if(!c||!c.messages.length){showWelcome();return;}c.messages.forEach(m=>addMessage(m.role,m.text));chatArea.scrollTop=chatArea.scrollHeight;}
function autoSize(){prompt.style.height='auto';prompt.style.height=Math.min(prompt.scrollHeight,145)+'px';}
function persistMessage(role,text){const c=currentChat();if(!c)return;c.messages.push({role,text});if(role==='user'&&c.messages.filter(m=>m.role==='user').length===1)c.title=safeTitle(text);c.updated=Date.now();save();renderHistory();}
async function sendMessage(text){if(busy||!text.trim())return;if(!currentChat())makeChat();const message=text.trim();persistMessage('user',message);const welcome=chatArea.querySelector('.welcome');if(welcome)welcome.remove();addMessage('user',message);prompt.value='';autoSize();busy=true;sendBtn.disabled=true;const row=document.createElement('div');row.className='message assistant';const av=document.createElement('div');av.className='avatar';av.textContent='🤖';const bubble=document.createElement('div');bubble.className='bubble';const dots=document.createElement('div');dots.className='typing-dots';for(let i=0;i<3;i++)dots.appendChild(document.createElement('span'));bubble.appendChild(dots);row.append(av,bubble);chatArea.appendChild(row);chatArea.scrollTop=chatArea.scrollHeight;
try{const r=await fetch('/chat',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({message})});let d;try{d=await r.json();}catch(e){throw new Error('Server se valid response nahi mila.');}const reply=d.reply||d.error||'Jawab nahi mila.';bubble.textContent=reply;persistMessage('assistant',reply);if(!r.ok&&!d.reply)bubble.textContent='Server error ('+r.status+'). Thodi der baad try karo.';}catch(e){const err='Connection error. Internet aur AI server check karke dobara try karo.';bubble.textContent=err;persistMessage('assistant',err);}finally{busy=false;sendBtn.disabled=false;prompt.focus();chatArea.scrollTop=chatArea.scrollHeight;}}
$('chatForm').addEventListener('submit',e=>{e.preventDefault();sendMessage(prompt.value);});prompt.addEventListener('input',autoSize);prompt.addEventListener('keydown',e=>{if(e.key==='Enter'&&!e.shiftKey){e.preventDefault();$('chatForm').requestSubmit();}});$('newChat').addEventListener('click',makeChat);$('menuBtn').addEventListener('click',()=>sidebar.classList.toggle('open'));
if(chats.length){activeId=chats.slice().sort((a,b)=>(b.updated||0)-(a.updated||0))[0].id;}else{const c={id:Date.now().toString(),title:'New conversation',messages:[],updated:Date.now()};chats.push(c);activeId=c.id;save();}renderHistory();renderChat();

const voiceBtn=$('voiceBtn'),voiceStatus=$('voiceStatus');
let voiceWs=null,voiceStream=null,voiceCtx=null,voiceProcessor=null,voiceReady=false,playAt=0;

function voiceStatusText(t){voiceStatus.textContent=t;}
function stopVoice(){
  voiceReady=false;
  if(voiceProcessor){voiceProcessor.disconnect();voiceProcessor.onaudioprocess=null;voiceProcessor=null;}
  if(voiceStream){voiceStream.getTracks().forEach(t=>t.stop());voiceStream=null;}
  if(voiceWs){const w=voiceWs;voiceWs=null;try{w.close();}catch(e){}}
  if(voiceCtx){const c=voiceCtx;voiceCtx=null;c.close().catch(()=>{});}
  playAt=0;
  voiceBtn.textContent='🎙️ Voice';
  voiceBtn.disabled=false;
  voiceStatusText('Voice chat: off');
}

function audioToBase64(samples){
  const pcm=new Int16Array(samples.length);
  for(let i=0;i<samples.length;i++){
    const v=Math.max(-1,Math.min(1,samples[i]));
    pcm[i]=v<0?v*32768:v*32767;
  }
  const bytes=new Uint8Array(pcm.buffer);
  let binary='';
  for(let i=0;i<bytes.length;i+=8192){
    binary+=String.fromCharCode(...bytes.subarray(i,Math.min(i+8192,bytes.length)));
  }
  return btoa(binary);
}

function resampleAudio(input,fromRate,toRate){
  if(fromRate===toRate)return input;
  const length=Math.floor(input.length*toRate/fromRate);
  const output=new Float32Array(length);
  const ratio=fromRate/toRate;
  for(let i=0;i<length;i++){
    const start=Math.floor(i*ratio);
    const end=Math.min(Math.floor((i+1)*ratio),input.length);
    let sum=0,count=0;
    for(let j=start;j<end;j++){sum+=input[j];count++;}
    output[i]=count?sum/count:input[Math.min(start,input.length-1)]||0;
  }
  return output;
}

function playLiveAudio(base64){
  if(!voiceCtx)return;
  const raw=atob(base64),samples=new Int16Array(Math.floor(raw.length/2));
  for(let i=0;i<samples.length;i++){
    const lo=raw.charCodeAt(i*2),hi=raw.charCodeAt(i*2+1);
    let n=(hi<<8)|lo;if(n>=32768)n-=65536;
    samples[i]=n/32768;
  }
  const buffer=voiceCtx.createBuffer(1,samples.length,24000);
  buffer.copyToChannel(Float32Array.from(samples),0);
  const source=voiceCtx.createBufferSource();
  source.buffer=buffer;source.connect(voiceCtx.destination);
  const start=Math.max(voiceCtx.currentTime+0.04,playAt);
  source.start(start);playAt=start+buffer.duration;
}

async function startVoice(){
  voiceBtn.disabled=true;
  voiceStatusText('Connecting to StudyBot Live…');
  try{
    const tokenResponse=await fetch('/live-token',{method:'POST'});
    const tokenData=await tokenResponse.json();
    if(!tokenResponse.ok||!tokenData.token)throw new Error(tokenData.error||'Gemini Live token nahi mila.');

    voiceStream=await navigator.mediaDevices.getUserMedia({
      audio:{channelCount:1,echoCancellation:true,noiseSuppression:true,autoGainControl:true}
    });
    voiceCtx=new(window.AudioContext||window.webkitAudioContext)({sampleRate:24000});
    await voiceCtx.resume();

    const wsUrl='wss://generativelanguage.googleapis.com/ws/google.ai.generativelanguage.v1beta.GenerativeService.BidiGenerateContentConstrained?access_token='+encodeURIComponent(tokenData.token);
    voiceWs=new WebSocket(wsUrl);

    voiceWs.onopen=()=>{
      voiceWs.send(JSON.stringify({setup:{
        model:'models/'+tokenData.model,
        generationConfig:{responseModalities:['AUDIO']}
      }}));
    };

    voiceWs.onmessage=async(event)=>{
      let data;
      try{data=JSON.parse(event.data);}catch(e){return;}
      if(data.error){
        voiceStatusText('Live API error: '+(data.error.message||'Unknown error'));
        stopVoice();return;
      }
      if(data.setupComplete){
        voiceReady=true;
        voiceBtn.disabled=false;
        voiceBtn.textContent='⏹ Stop voice';
        voiceStatusText('Listening… Bolo, StudyBot sun raha hai.');
        const source=voiceCtx.createMediaStreamSource(voiceStream);
        voiceProcessor=voiceCtx.createScriptProcessor(4096,1,1);
        const silent=voiceCtx.createGain();silent.gain.value=0;
        voiceProcessor.onaudioprocess=(e)=>{
          if(!voiceReady||!voiceWs||voiceWs.readyState!==WebSocket.OPEN)return;
          const input=e.inputBuffer.getChannelData(0);
          const pcm=resampleAudio(input,voiceCtx.sampleRate,16000);
          voiceWs.send(JSON.stringify({realtimeInput:{audio:{
            mimeType:'audio/pcm;rate=16000',data:audioToBase64(pcm)
          }}}));
        };
        source.connect(voiceProcessor);voiceProcessor.connect(silent);silent.connect(voiceCtx.destination);
      }
      const parts=data.serverContent&&data.serverContent.modelTurn&&data.serverContent.modelTurn.parts;
      if(parts)for(const part of parts){
        if(part.inlineData&&part.inlineData.data)playLiveAudio(part.inlineData.data);
      }
      if(data.serverContent&&data.serverContent.interrupted)playAt=0;
    };

    voiceWs.onerror=()=>{voiceStatusText('Voice connection error. API access aur quota check karo.');};
    voiceWs.onclose=()=>{
      if(voiceReady){stopVoice();voiceStatusText('Voice connection closed. Dobara try karo.');}
    };
  }catch(e){
    stopVoice();
    voiceStatusText('Voice start nahi hua: '+(e.message||'Permission ya API error'));
  }
  if(!voiceReady)voiceBtn.disabled=false;
}

voiceBtn.addEventListener('click',()=>{
  if(voiceWs||voiceStream){stopVoice();return;}
  if(!navigator.mediaDevices||!navigator.mediaDevices.getUserMedia){
    voiceStatusText('Mic ke liye HTTPS website aur supported browser chahiye.');return;
  }
  startVoice();
});

})();
</script>

<script>
if ("serviceWorker" in navigator) {
  window.addEventListener("load", () => {
    navigator.serviceWorker.register("/static/sw.js")
      .catch(err => console.error("Service worker error:", err));
  });
}
</script>
\n</body>
</html>'''

@app.route("/")
def home():
    return render_template_string(HTML)




@app.route("/manifest.json")
def manifest():
    return {
        "id": "/",
        "name": "StudyBot AI",
        "short_name": "StudyBot",
        "description": "Your smart AI study assistant.",
        "start_url": "/",
        "scope": "/",
        "display": "standalone",
        "background_color": "#0b1020",
        "theme_color": "#0b1020",
        "icons": [
            {
                "src": "/static/icon-192.png",
                "sizes": "192x192",
                "type": "image/png",
                "purpose": "any"
            },
            {
                "src": "/static/icon-512.png",
                "sizes": "512x512",
                "type": "image/png",
                "purpose": "any maskable"
            }
        ]
    }


@app.route("/chat", methods=["POST"])
def chat():
    key = os.environ.get("GEMINI_API_KEY")
    if not key:
        return jsonify(reply="API key set nahi hai. Termux mein key check karo."), 500

    body = request.get_json(silent=True) or {}
    message = body.get("message", "")
    if not isinstance(message, str):
        return jsonify(reply="Sawaal text mein likho."), 400
    message = message.strip()
    if not message:
        return jsonify(reply="Sawaal likho.")

    data = json.dumps({"contents": [{"parts": [{"text": message}]}]}).encode()
    models = ["gemini-3.5-flash"]
    last_code = None
    for model in models:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"
        req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json", "x-goog-api-key": key}, method="POST")
        for attempt in range(4):
            try:
                with urllib.request.urlopen(req, timeout=50) as response:
                    result = json.loads(response.read().decode())
                reply = result["candidates"][0]["content"]["parts"][0]["text"]
                return jsonify(reply=reply)
            except urllib.error.HTTPError as e:
                detail = e.read().decode(errors="replace")
                print("Gemini API error:", e.code, detail)
                last_code = e.code
                if e.code == 429:
                    return jsonify(reply="Gemini API ki request limit abhi poori hai. Quota reset hone par dobara try karo."), 429
                if e.code not in (408, 500, 502, 503, 504):
                    return jsonify(reply=f"Gemini API error ({e.code}). Termux logs check karo."), 502
            except Exception as e:
                print("Connection error:", repr(e))
            if attempt < 3:
                time.sleep(2 ** attempt)
    print("Gemini request failed after retries; last HTTP code:", last_code)
    return jsonify(reply="AI server abhi busy hai. Kuch seconds baad dobara try karo."), 502


@app.route("/live-token", methods=["POST"])
def live_token():
    key = os.environ.get("GEMINI_API_KEY")
    if not key:
        return jsonify(error="Server API key is not configured."), 500

    now = datetime.now(timezone.utc)
    iso = lambda value: value.isoformat(timespec="seconds").replace("+00:00", "Z")

    payload = {
        "uses": 1,
        "expireTime": iso(now + timedelta(minutes=30)),
        "newSessionExpireTime": iso(now + timedelta(minutes=1)),
        "liveConnectConstraints": {
            "model": "models/gemini-3.8-live",
            "config": {
                "sessionResumption": {},
                "responseModalities": ["AUDIO"]
            }
        }
    }

    req = urllib.request.Request(
        "https://generativelanguage.googleapis.com/v1beta/auth_tokens",
        data=json.dumps(payload).encode(),
        headers={
            "Content-Type": "application/json",
            "x-goog-api-key": key
        },
        method="POST"
    )

    try:
        with urllib.request.urlopen(req, timeout=20) as response:
            result = json.loads(response.read().decode())
        token = result.get("name")
        if not token:
            return jsonify(error="No token returned by Gemini."), 502
        return jsonify(token=token, model="gemini-3.8-live")
    except urllib.error.HTTPError as e:
        print("Gemini Live token error:", e.code, e.read().decode(errors="replace")[:1000])
        return jsonify(error=f"Live API token creation failed ({e.code}). Check server logs and model access."), 502
    except Exception as e:
        print("Gemini Live connection error:", repr(e))
        return jsonify(error="Could not connect to Gemini Live API."), 502

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000)
