
import os
import json
import urllib.request
import urllib.error
from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>StudyBot AI</title>
<style>
body{background:#101827;color:white;font-family:Arial;
padding:20px;margin:0}
h1{color:#66e3ff;text-align:center}
#chat{height:60vh;overflow:auto;background:#1c2940;
padding:12px;border-radius:12px}
.msg{padding:10px;margin:8px 0;border-radius:8px;
background:#293951;white-space:pre-wrap;overflow-wrap:anywhere}
input{width:70%;padding:12px;border-radius:8px;
border:0;box-sizing:border-box}
button{padding:12px;background:#66e3ff;border:0;
border-radius:8px;font-weight:bold}
</style>
</head>
<body>
<h1>🤖 StudyBot AI</h1>
<div id="chat"><div class="msg">Namaste! Main StudyBot hoon.
Mujhse kuch bhi poochho!</div></div><br>
<form id="form">
<input id="msg" placeholder="Apna sawaal likho..." required>
<button>Send</button>
</form>
<script>
const form=document.getElementById('form');
const input=document.getElementById('msg');
const chat=document.getElementById('chat');
form.onsubmit=async(e)=>{
e.preventDefault();
const message=input.value.trim();
if(!message)return;
chat.innerHTML+='<div class="msg"><b>Tum:</b> '+escapeHtml(message)+'</div>';
input.value='';
const wait=document.createElement('div');
wait.className='msg';
wait.textContent='StudyBot soch raha hai...';
chat.appendChild(wait);
chat.scrollTop=chat.scrollHeight;
try{
const r=await fetch('/chat',{method:'POST',
headers:{'Content-Type':'application/json'},
body:JSON.stringify({message})});
const d=await r.json();
wait.textContent=d.reply||d.error||'Jawab nahi mila.';
}catch(e){wait.textContent='Connection error. Dobara try karo.'}
chat.scrollTop=chat.scrollHeight;
};
function escapeHtml(s){
const d=document.createElement('div');
d.textContent=s;return d.innerHTML;
}
</script>
</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(HTML)

@app.route("/chat", methods=["POST"])
def chat():
    key = os.environ.get("GEMINI_API_KEY")
    if not key:
        return jsonify(reply="API key set nahi hai. Termux mein key check karo."), 500

    message = request.json.get("message", "").strip()
    if not message:
        return jsonify(reply="Sawaal likho.")

    data = json.dumps({
        "contents": [{
            "parts": [{"text": message}]
        }]
    }).encode()

    req = urllib.request.Request(
        
"https://generativelanguage.googleapis.com/v1beta/models/gemini-3.8-flash:generateContent",
        
        data=data,
        headers={
            "Content-Type": "application/json",
            "x-goog-api-key": key
        },
        method="POST"
    )

    try:
        with urllib.request.urlopen(req, timeout=45) as response:
            result = json.loads(response.read().decode())
        reply = result["candidates"][0]["content"]["parts"][0]["text"]
        return jsonify(reply=reply)
    except urllib.error.HTTPError as e:
        detail = e.read().decode(errors="replace")
        print("Gemini API error:", detail)
        return jsonify(reply="Gemini API error. Termux ki screen par error details check karo."), 502
    except Exception as e:
        print("Error:", str(e))
        return jsonify(reply="Connection mein problem hai. Internet check karo."), 500

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000)

