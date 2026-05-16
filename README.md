# Game Session Server — Preliminary Design Document

## 1. Concept Overview

A real-time, round-based **single-player** game where one player fights waves of enemies and increasingly tough bosses. The game runs entirely through a FastAPI backend; state is persisted in a JSON file. A separate dashboard app (Typescript React web client display) visualises live stats.

---

## 2. Core Game Loop

```
[Match starts]
    │
    ▼
Every turn:
  ├─ Player gains +1 mana
  └─ Player regenerates +1 HP  (unless regen is paused — see §4)
    │
    ▼
Every 5 turns:
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
- The player accumulates **+1 mana per turn** automatically.
- Mana is spent on two actions:

| Action | Effect |
|--------|--------|
| Attack | Deal damage to the **current enemy** |
| Upgrade stat | Increase one stat by 1 (see `update_stats` in §6) |

### HP Regeneration & Regen Pause
- Base regen: **+1 HP per turn**.
- After **receiving** damage → player's regen is paused for **1 turns**.
- After **dealing** damage → player's regen is paused for **2 turns**.

### Attack Timing
- Both the player and the enemy can only attack **once every 1 turns**.
- The player can attack anytime (attack costs mana); the enemy's attack is automatic.

---

## 1. Rounds & Boss Encounters

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

## 6. Data Management

All game data will be saved and read from **JSON** architecture. The data will be split into:

 - enemy.json: Data related to enemies and their stats(hp, dmg)
 - player.json: Data related to the player. Stores only base stats for the player(hp, dmg, mana)
 - round.json: Data related to the current round information. Base entity stats from other files are modified by the multipliers based on the current round.

---

## 7. API Endpoints

All endpoints are served by the **Game Session Server** (FastAPI).

### Match Management

| Method | Path | Description |
|--------|------|-------------|
| `POST` | `/startMatch` | Initialise a new match session, reset round counter, spawn initial enemies. **Async.** |
| `POST` | `/updateMatch` | Process a single turn — awards mana, applies regen, triggers attacks on every 5th turn, and saves state. **Async.** |

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
| `3` | Mana +1 |

> **Note:** The exact request/response schemas (field names, auth, validation rules) are to be defined in the next iteration.

---

## 8. Data Persistence

- All game state is saved in **JSON format** to the database after defeaating an enemy.
- The fields persisted between rounds are: `hp`, `attack`, `current_round`, and `current_enemy` (see §5).
- On Game Over (`hp <= 0`), the final state snapshot is preserved for the dashboard to read.

---

## 9. Game Session Dashboard

A companion app that reads from the database and connects with FastAPI that visualises:

- Live player stats (HP, mana, attack)
- Round number & boss status
- Kill feed / event log
- Player interface to interract with the game

### Implementation: **Vite React Typescript** front-end client for game logic visualisation and user interraction implementation.


