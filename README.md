# Game Session Server

## 1. Concept Overview

A round-based **single-player** game where one player fights waves of enemies. The game runs through a FastAPI backend with state persisted in JSON files. A Vite React TypeScript frontend visualises live stats and handles all player interaction.

---

## 2. Core Game Loop

```
[Match starts — username entered]
    │
    ▼
Every turn:
  ├─ Player gains +1 mana
  └─ Player regenerates +1 HP
    │
    ▼
Every 5 turns:
  └─ Enemy auto-attacks the player
    │
    ▼
Player chooses each turn:
  ├─ Attack the current enemy (free — no mana cost)
  └─ Spend mana on stat upgrades (Health or Attack)
    │
    ▼
Kill an enemy → round += 1, new enemy spawns, player heals +5 HP
    │
    ▼
HP <= 0 → Game Over
```

---

## 3. Characters

### Player

| Stat | Field | Default |
|------|-------|---------|
| Base HP | `player_base_hp` | 10 |
| Current HP | `Player_current_hp` | 10 |
| Attack | `player_attack` | 1 |
| Mana | `mana` | 0 |

### Enemy

| Stat | Field |
|------|-------|
| Name | `enemy_name` |
| Base HP | `enemy_base_hp` |
| Current HP | `enemy_current_hp` |
| Attack | `enemy_attack` |

Enemies are picked randomly from the enemy list at the start of each round. Stats are not scaled by round number.

---

## 4. Mana & Upgrades

The player accumulates **+1 mana per turn** automatically. Mana is spent on stat upgrades only — attacking costs no mana.

| Action | Mana Cost | Effect |
|--------|-----------|--------|
| Upgrade Health | 2 | `player_base_hp + 1`, `Player_current_hp + 1` |
| Upgrade Attack | 3 | `player_attack + 1` |

---

## 5. Combat

- The **player** can choose to attack once per turn (toggled before confirming the turn). Attack is free.
- The **enemy** auto-attacks the player every **5 turns**.
- HP regeneration is **+1 per turn**, unless the enemy attacks that turn.
- On killing an enemy, the player heals **+5 HP** (capped at base HP) and a new enemy spawns.

---

## 6. Session & Username System

- On the Home screen the player enters a username to start.
- On match start, the backend checks if the saved username matches. If it does, the existing save is resumed. If not, all stats and round progress are reset and the new username is saved.
- This means only one save slot exists at a time — entering a different username wipes the previous session.

---

## 7. Data Persistence

All game state is stored in three JSON files under `json_files/`:

| File | Contents |
|------|----------|
| `player.json` | Current player stats and username |
| `enemies.json` | Full enemy list with base and current stats |
| `match_info.json` | Current round number and active enemy ID |

State is saved after every round progression and on match start.

---

## 8. API Endpoints

All endpoints are served by the FastAPI backend (`main.py`).

### Match

| Method | Path | Description |
|--------|------|-------------|
| `POST` | `/match/start?logged_username=` | Load save data; reset everything if username differs |
| `GET` | `/match/save` | Manually persist all state to JSON |

### Turn & Round

| Method | Path | Description |
|--------|------|-------------|
| `POST` | `/turn/progres?player_attacked=` | Advance one turn; apply attack, enemy attack (every 5), mana and HP regen |
| `GET` | `/round/progres` | Called internally on enemy death or player death; increments round or resets match |
| `GET` | `/round/get` | Returns current round number |

### Player

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/player/get/` | Returns current player state |
| `POST` | `/player/add` | Add / overwrite player data |
| `POST` | `/player/upgrade?stat_index=` | `1` = upgrade health (costs 2 mana), `2` = upgrade attack (costs 3 mana) |

### Enemy

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/enemy/get` | Returns the current active enemy |
| `GET` | `/enemy/getall` | Returns the full enemy list |
| `POST` | `/enemy/add` | Add an enemy to the list |

### Health Check

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/api/health` | Returns backend status |

---

## 9. Frontend

Built with **Vite + React + TypeScript**.

**Home screen (`Home.tsx`):** Username input. Navigates to `/game` with the username passed via router state.

**Game screen (`Game.tsx`):** Displays live player stats (HP, attack, mana), current round, and the active enemy via the `Round` component. Action bar exposes upgrade buttons (disabled when mana is insufficient) and the Next Turn button with the attack toggle.