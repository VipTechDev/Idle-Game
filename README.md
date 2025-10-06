# 🛡️ Idle-Game

A shrine-grade idle game built in 10 hours. Recruit party members, slay monsters, and upgrade your quest in a modular, flavor-coded adventure.

## 🎮 Features

- 🧙 Recruit unique characters with coin offerings  
- ⚔️ Slay monsters and earn rewards  
- 📈 Upgrade party members with multipliers  
- 🧠 Persistent slay logs and offline earnings  
- 🧱 Modular UI with shrine-style layout  
- 💾 Save and load your progress  

## 🧪 Installation

Clone the repo:

```bash
git clone https://github.com/VipTechDev/Idle-Game.git
cd Idle-Game
```

Install dependencies:

```bash
pip install pygame
```

Run the game:

```bash
python main.py
```

## 🧙‍♀️ Controls

- Click **Upgrade** buttons to level up characters  
- Click **Recruit** buttons to unlock new party members  
- Click **Multiplier** to cycle upgrade scaling  
- Use **Save/Load** buttons to preserve your progress  

## 🧭 Structure

```text
Idle-Game/
├── main.py              # Game loop and event handling
├── ui.py                # Drawing shrine-grade UI
├── economy.py           # Upgrade cost logic
├── graphics.py          # Background tiling and assets
├── characters.py        # Party member definitions
├── monsters.py          # Monster generation and rewards
├── gamestate.py         # Save/load logic
├── assets/              # PNGs and visual flavor
└── savegame.txt         # Persistent coin and character data
```

## 🧙‍♂️ Lore

> "The shrine awakens. Coins glimmer. The Rogue waits."

Each character is a modular ritual — unlocked with coins, upgraded with multipliers, and celebrated in the slay log. The shrine remembers your progress, even when you wander.

## 🛠️ To-Do

- [ ] Add hover effects and sound rituals  
- [ ] Port to Roblox Studio (Lua)    
- [ ] Add flavor-coded class icons and progress bar polish  

## 🧙‍♂️ Credits

Created by **Pete** in 10 hours of focused shrine-building.  
Documented and ritualized with help from **Copilot**, your bardic companion.
