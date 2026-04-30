# Game Session Server — Preliminary Design Document

> **Status:** Early draft — mechanics are still being refined.  
> **Stack:** FastAPI · Firebase (or any JSON-capable DB) · CLI/Web Dashboard

---

## 1. Concept Overview

A real-time, round-based **single-player** game where one player fights waves of enemies and increasingly tough bosses. The game runs entirely through a FastAPI backend; state is persisted in a JSON-friendly database (e.g. Firebase). A separate dashboard app (CLI or web frontend, e.g. Matplotlib-powered) visualises live stats.

---

## 2. Core Game Loop

```
[Match starts]
    │
    ▼
Every tick:
  ├─ Player gains +1 mana
  └─ Player regenerates +1 HP  (unless regen is paused — see §4)
    │
    ▼
Every 5 ticks:
  ├─ Player may attack the current enemy  (costs mana)
  └─ Current enemy auto-attacks the player
    │
    ▼
Kill an enemy → round += 1
  ├─ round % 10 == 0 → spawn Boss (see §5)
  └─ otherwise       → continue
    │
    ▼
HP <= 0 → Game Over for that player
```

---

## 3. Characters

Each character has the following base stats stored in the database:

| Stat | Field | Default |
|------|-------|---------|
| Hit Points | `hp` | TBD |
| Attack | `attack` | TBD |
| (future stats) | … | … |

Characters are created and deleted via the API (see §6). Stats can be upgraded during a match using mana.

---

## 4. Mana & Combat

### Mana
- The player accumulates **+1 mana per tick** automatically.
- Mana is spent on two actions:

| Action | Effect |
|--------|--------|
| Attack | Deal damage to the **current enemy** |
| Upgrade stat | Increase one stat by 1 (see `update_stats` in §6) |

### HP Regeneration & Regen Pause
- Base regen: **+1 HP per tick**.
- After **receiving** damage → player's regen is paused for **5 ticks**.
- After **dealing** damage → player's regen is paused for **2 ticks**.

### Attack Timing
- Both the player and the enemy can only attack **once every 5 ticks**.
- The player's attack is optional (costs mana); the enemy's attack is automatic.

---

## 5. Rounds & Boss Encounters

- The **round counter** increments by 1 each time an enemy is killed.
- When `round % 10 == 0` → a **Boss** spawns.
- Boss and enemy stat scaling:

```
enemy_stat = base_stat * (1 + 0.1 * current_round)
```

- Enemies attack autonomously; they do not require any input.

### State Saved Between Rounds

After each round (enemy killed), the following game state is persisted to the database so progress is not lost:

| Field | Description |
|-------|-------------|
| `hp` | Player's current HP carried into the next round |
| `attack` | Player's current attack stat |
| `current_round` | Round number used to scale the next enemy |
| `current_enemy` | Stats of the next enemy to be spawned (pre-calculated) |

This means the player keeps any HP and stat upgrades accumulated so far — there is no reset between rounds.

---

## 6. API Endpoints

All endpoints are served by the **Game Session Server** (FastAPI).

### Match Management

| Method | Path | Description |
|--------|------|-------------|
| `POST` | `/startMatch` | Initialise a new match session, reset round counter, spawn initial enemies. **Async.** |
| `POST` | `/updateMatch` | Process a single tick — awards mana, applies regen, triggers attacks on every 5th tick, and saves state. **Async.** |

### Character Management

| Method | Path | Description |
|--------|------|-------------|
| `POST` | `/createCharacter` | Create a new character with default stats and persist to DB. |
| `DELETE` | `/deleteCharacter` | Remove a character from the DB. |
| `PATCH` | `/updateCharacterStats` | Update a specific stat by a given integer amount. **Async.** |

#### `updateCharacterStats` — stat index convention (preliminary)

| Value passed | Stat affected |
|---|---|
| `1` | HP +1 |
| `2` | Attack +1 |
| … | … (to be extended) |

> **Note:** The exact request/response schemas (field names, auth, validation rules) are to be defined in the next iteration.

---

## 7. Data Persistence

- All game state is saved in **JSON format** to the database after every meaningful state change — including after each round ends.
- The fields persisted between rounds are: `hp`, `attack`, `current_round`, and `current_enemy` (see §5).
- Suggested DB: **Firebase Realtime Database** or Firestore — both expose a REST interface that pairs naturally with FastAPI async handlers.
- On Game Over (`hp <= 0`), the final state snapshot is preserved for the dashboard to read.

---

## 8. Game Session Dashboard

A companion app (implementation TBD) that reads from the database and visualises:

- Live player stats (HP, mana, attack)
- Round number & boss status
- Kill feed / event log

Implementation options:
- **Backend CLI** using Python + Matplotlib (quick to build, good for dev/testing)
- **Frontend web app** (React, etc.) for a richer UI

---

## 9. Open Questions / Next Steps

- [ ] Define exact mana costs per action (attack vs. upgrade)
- [ ] Define base stats for characters and NPCs
- [ ] Define boss unique mechanics (beyond stat scaling)
- [ ] Decide on auth strategy (sessions, tokens?)
- [ ] Finalise request/response schemas for all endpoints
- [ ] Choose dashboard tech (CLI vs. web)
- [ ] Define exact enemy base stats and how `current_enemy` is pre-calculated and stored