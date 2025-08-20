// Presence sensing (local-only). Feels pointer/touch and animates pulse.
const pulse = document.getElementById('pulse');
const stats = document.getElementById('presence-stats');
const guardianNameEl = document.getElementById('guardian-name');
const guardianStateEl = document.getElementById('guardian-state');
const btnAwaken = document.getElementById('btn-awaken');
const btnSoothe = document.getElementById('btn-soothe');
const topicsEl = document.getElementById('topics');

let lastPresence = 0;
let presenceCount = 0;

function stampPresence(evtName) {
  lastPresence = Date.now();
  presenceCount += 1;
  pulse.style.transform = 'scale(1.25)';
  setTimeout(() => { pulse.style.transform = 'scale(1)'; }, 160);
  stats.textContent = `Presence sensed via ${evtName}. Total: ${presenceCount}. Last: ${new Date(lastPresence).toLocaleTimeString()}`;
}

['pointermove', 'click', 'touchstart', 'keydown'].forEach(e => {
  window.addEventListener(e, () => stampPresence(e), { passive: true });
});

// Guardian model (local state; could be swapped for CMS/kernel).
const guardian = { name: 'Euystacio', state: 'sleeping' };
function setGuardianState(s) {
  guardian.state = s;
  guardianStateEl.textContent = s;
}
btnAwaken.addEventListener('click', () => setGuardianState('listening'));
btnSoothe.addEventListener('click', () => setGuardianState('sleeping'));

// Load consensus/topics (from stub JSON or CMS endpoint).
async function loadConsensus() {
  try {
    const res = await fetch('data/consensus.json', { cache: 'no-store' });
    const json = await res.json();
    topicsEl.innerHTML = '';
    (json.topics || []).forEach(t => {
      const li = document.createElement('li');
      li.innerHTML = `<strong>${t.title}</strong><br/><span class="small">quorum: ${(t.quorum*100).toFixed(0)}%</span><br/>${t.note}`;
      topicsEl.appendChild(li);
    });
    guardianNameEl.textContent = (json.guardian && json.guardian.name) || guardian.name;
    setGuardianState((json.guardian && json.guardian.state) || guardian.state);
  } catch (e) {
    topicsEl.innerHTML = '<li>Failed to load consensus. Using local memory.</li>';
  }
}
loadConsensus();