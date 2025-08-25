// Basic chat UI logic
const messages = document.getElementById('messages');
const input = document.getElementById('textInput');
const sendBtn = document.getElementById('sendBtn');
const recBtn = document.getElementById('recBtn');

function addMessage(text, who='bot', audioUrl=null){
  const div = document.createElement('div');
  div.className = 'msg ' + who;
  div.textContent = text;
  messages.appendChild(div);
  if(audioUrl){
    const audio = document.createElement('audio');
    audio.controls = true;
    audio.src = audioUrl;
    messages.appendChild(audio);
  }
  messages.scrollTop = messages.scrollHeight;
}

async function sendText(){
  const text = input.value.trim();
  if(!text) return;
  addMessage(text, 'user');
  input.value = '';
  sendBtn.disabled = true;
  try{
    const resp = await fetch('/api/text', {
      method: 'POST',
      headers: {'Content-Type':'application/json'},
      body: JSON.stringify({message: text})
    });
    const data = await resp.json();
    if(data.error){ addMessage('Erro: ' + data.error); }
    else{
      addMessage(data.reply, 'bot', data.audio_url);
    }
  }catch(e){
    addMessage('Falha: ' + e.message);
  }finally{
    sendBtn.disabled = false;
  }
}

sendBtn.addEventListener('click', sendText);
input.addEventListener('keydown', (e)=>{
  if(e.key === 'Enter'){ sendText(); }
});

// Recording via MediaRecorder
let mediaRecorder;
let chunks = [];
let recording = false;

async function toggleRecord(){
  if(!recording){
    try{
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      mediaRecorder = new MediaRecorder(stream);
      mediaRecorder.ondataavailable = e => chunks.push(e.data);
      mediaRecorder.onstop = onStopRecording;
      chunks = [];
      mediaRecorder.start();
      recording = true;
      recBtn.textContent = '⏹️ Parar';
    }catch(e){
      addMessage('Permissão de microfone negada ou não disponível.');
    }
  }else{
    mediaRecorder.stop();
  }
}

async function onStopRecording(){
  recording = false;
  recBtn.textContent = '🎙️ Gravar';
  const blob = new Blob(chunks, { type: 'audio/webm' });
  chunks = [];
  addMessage('(enviando áudio...)', 'user');
  const form = new FormData();
  form.append('audio', blob, 'recording.webm');
  try{
    const resp = await fetch('/api/voice', { method: 'POST', body: form });
    const data = await resp.json();
    if(data.error){ addMessage('Erro: ' + data.error); }
    else{
      addMessage('Você (transcrito): ' + data.transcript, 'user');
      addMessage(data.reply, 'bot', data.audio_url);
    }
  }catch(e){
    addMessage('Falha: ' + e.message);
  }
}

recBtn.addEventListener('click', toggleRecord);
