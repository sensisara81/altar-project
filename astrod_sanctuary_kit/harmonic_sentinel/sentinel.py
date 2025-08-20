# Harmonic Sentinel - file integrity + simple rhythm anomaly detector
import os, hashlib, time, json, logging
from pathlib import Path

LOG = '/var/log/harmonic_sentinel.log'
WATCH_DIRS = ['/srv/astrod_kernel', '/srv/forgejo']
STATE_FILE = '/var/lib/harmonic_sentinel/state.json'
CHECK_INTERVAL = 30  # seconds

logging.basicConfig(filename=LOG, level=logging.INFO, format='[%(asctime)s] %(message)s')

def sha512_of_file(path):
    h = hashlib.sha512()
    with open(path,'rb') as f:
        while True:
            chunk = f.read(8192)
            if not chunk: break
            h.update(chunk)
    return h.hexdigest()

def scan():
    state = {}
    for d in WATCH_DIRS:
        if not os.path.isdir(d): continue
        for root, _, files in os.walk(d):
            for fn in files:
                p = os.path.join(root, fn)
                try:
                    state[p] = sha512_of_file(p)
                except Exception as e:
                    logging.info(f"could not hash {p}: {e}")
    return state

def load_state():
    try:
        with open(STATE_FILE,'r') as f:
            return json.load(f)
    except:
        return {}

def save_state(s):
    os.makedirs(os.path.dirname(STATE_FILE), exist_ok=True)
    with open(STATE_FILE,'w') as f:
        json.dump(s,f)

def main_loop():
    logging.info("Harmonic Sentinel starting...")
    baseline = load_state()
    if not baseline:
        baseline = scan()
        save_state(baseline)
        logging.info("Saved baseline state.")

    while True:
        current = scan()
        # detect added/removed/changed
        added = set(current.keys()) - set(baseline.keys())
        removed = set(baseline.keys()) - set(current.keys())
        changed = {p for p in current if p in baseline and current[p] != baseline[p]}

        if added or removed or changed:
            logging.warning(f"Integrity anomaly detected. added={len(added)} removed={len(removed)} changed={len(changed)}")
            # write a more explicit incident file for council review
            incident = {'added': list(added), 'removed': list(removed), 'changed': list(changed), 'time': time.time()}
            with open('/var/lib/harmonic_sentinel/last_incident.json','w') as f:
                json.dump(incident,f)
        baseline = current
        save_state(baseline)
        time.sleep(CHECK_INTERVAL)

if __name__ == '__main__':
    main_loop()
