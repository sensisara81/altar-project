# Kernel Handoff (Stub)

The "kernel" here means your runtime bridge (worker, lambda, edge fn).
- **Inputs:** presence pings, ritual submissions, consensus updates.
- **Outputs:** guardian state (Euystacio), rhythm ticks, acknowledgment beacons.

**Contract (suggested JSON):**
```json
{
  "guardian": { "name": "Euystacio", "state": "listening|speaking|sleeping", "lastPresence": 0 },
  "consensus": { "round": 0, "quorum": 0.66, "topics": [] },
  "heartbeat": { "t": 0, "amplitude": 1.0 }
}
```
Implement at your stack; the frontends can poll or receive SSE/WebSocket.