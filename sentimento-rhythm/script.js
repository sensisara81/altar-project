// Minimal step sequencer that lights ticks to embody consensus rhythm.
// Also mirrors guardian state and logs acts of presence.
const ticksContainer = document.getElementById('ticks');
const startBtn = document.getElementById('start');
const stopBtn = document.getElementById('stop');
const tempoInput = document.getElementById('tempo');
const logEl = document.getElementById('log');
const gnameEl = document.getElementById('gname');
const gstateEl = document.getElementById('gstate');

let intervalId = null;
let step = 0;

// Build 16 ticks
for (let i = 0; i < 16; i++) {
  const d = document.createElement('div');
  d.className = 'tick';
  ticksContainer.appendChild(d);
}

function setGuardian(state) { gstateEl.textContent = state; }

function log(msg) {
  const li = document.createElement('li');
  li.textContent = `[${new Date().toLocaleTimeString()}] ${msg}`;
  logEl.prepend(li);
}

function tick() {
  const ticks = document.querySelectorAll('.tick');
  ticks.forEach((t, i) => t.classList.toggle('active', i === step));
  step = (step + 1) % ticks.length;
}

function start() {
  if (intervalId) return;
  const bpm = Number(tempoInput.value);
  const ms = 60000 / bpm / 4; // 16th notes
  intervalId = setInterval(tick, ms);
  setGuardian('speaking');
  log(`Tempo set to ${bpm} BPM (16th).`);
}
function stop() {
  if (!intervalId) return;
  clearInterval(intervalId);
  intervalId = null;
  setGuardian('listening');
  log(`Sequencer paused.`);
}

startBtn.addEventListener('click', start);
stopBtn.addEventListener('click', stop);

['pointermove', 'click', 'touchstart', 'keydown'].forEach(e => {
  window.addEventListener(e, () => log(`Presence via ${e}`), { passive: true });
});

// Seed who we are
gnameEl.textContent = 'Euystacio';
setGuardian('sleeping');