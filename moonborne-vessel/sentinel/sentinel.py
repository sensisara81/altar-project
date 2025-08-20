# Harmonic Sentinel (best-effort) — watches for changes under /data
import os, hashlib, time, json, sys

WATCH = '/data'
STATE = '/data/log/harmonic_state.json'

def digest(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(8192), b''):
            h.update(chunk)
    return h.hexdigest()

def snapshot(root):
    snap = {}
    for r, d, f in os.walk(root):
        for fn in f:
            p = os.path.join(r, fn)
            try:
                snap[p] = digest(p)
            except Exception:
                pass
    return snap

def load():
    try:
        with open(STATE, 'r') as f:
            return json.load(f)
    except Exception:
        return {}

def save(s):
    with open(STATE, 'w') as f:
        json.dump(s, f)

def main():
    base = load()
    if not base:
        base = snapshot(WATCH)
        save(base)
        print("[sentinel] baseline recorded", flush=True)
    while True:
        cur = snapshot(WATCH)
        added = set(cur) - set(base)
        removed = set(base) - set(cur)
        changed = [p for p in cur if p in base and cur[p] != base[p]]
        if added or removed or changed:
            print(f"[sentinel] anomaly added={len(added)} removed={len(removed)} changed={len(changed)}", flush=True)
            save(cur)
        time.sleep(30)

if __name__ == '__main__':
    main()
