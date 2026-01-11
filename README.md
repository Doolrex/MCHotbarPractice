# doolrex's Hotbar Practice

![Python](https://img.shields.io/badge/Made%20with-Python-blue?style=for-the-badge&logo=python) ![Release](https://img.shields.io/badge/Release-v1.0-green?style=for-the-badge) ![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)

This is a lightweight minigame designed to help you **master your Minecraft hotbar keybinds**.

I originally created this tool to help me get used to a new keybinds I was trying out, keeping it as simple and fast as possible to hop in and practice at any time. Whether you are learning a new layout or just want to improve your reaction speed with your current setup, this tool is for you.

## 🚀 Features

* **Minecraft Logic:** Runs on a faithful **20 TPS (Ticks Per Second)** loop.
* **Tick-Block System:** Simulates the "priority" input handling of the real game.
* **Lightweight:** Instant startup, no unnecessary bloat.
* **Highly Customizable:** Change keys, textures, and sounds.

## 🎮 How to Play

1.  Download the latest `.zip` file from the **[Releases](https://github.com/Doolrex/MCHotbarPractice/releases)** section on the right.
2.  Extract the folder.
3.  Run `doolrex's Hotbar Practice.exe`.
4.  An item will appear in a random slot. **Press the key corresponding to that slot** to score a point!

## ⚙️ Customization

### 🛠️ Editor Mode (F3)
1.  Press **`F3`** while in-game to toggle **Editor Mode**.
2.  Key overlays will appear over the slots.
3.  **Click** on any slot with your mouse.
4.  **Press the new key** you want to assign.
5.  Press **`F3`** again to return to play mode.

### 🎨 Custom Assets
Want to practice with a sword, an apple, or a different hotbar style?
You can replace the files in the `assets` folder. **You must keep the original filenames**:
* `hotbar.png`
* `selector.png`
* `item.png`
* `success.wav` / `fail.wav`

### 📝 Configuration File (`config.json`)
The game automatically generates a `config.json` file. You can edit this file to modify keybinds manually or adjust advanced settings.

### ⚡ Advanced Setting: Reaction Timer

By default, the game gives you infinite time to react. Want to simulate high-pressure PvP or PvE situations?

Open `config.json` and look for:

```json
"reaction_limit_ticks": -1
```
* **-1**: Infinite time (Default).
* **Positive Number**: The item will disappear and change position if you don't hit the key within this amount of ticks.
    * *Example:* Set it to `10` to force yourself to react in less than 0.5 seconds

---

## 🔮 Future Plans & Roadmap

I am planning to add several advanced features to make this tool even more useful for speedrunners and PvP players. Here is what is coming next:

* **⚡ Attribute Swapping Practice:**
    A dedicated game mode to practice the precise timing required for **Attribute Swapping**, helping you master the rhythm of switching items to maximize damage or specific attributes during combat.

* **⚔️ Slot-Specific Custom Items:**
    Currently, the item texture is generic. I plan to add a system where the item displayed matches the specific slot, simulating your real inventory layout.
    * *Example:* If you always carry your **Sword in Slot 1** and your **Axe in Slot 3**, the game will show a sword texture when targeting Slot 1 and an axe texture when targeting Slot 3. This will help build stronger visual muscle memory.

* **✋ Inventory Management Mode (Offhand Swapping):**
    A new mode designed to practice the "hotbar fix" technique used by speedrunners to organize items instantly without opening the inventory GUI.
    * *The Mechanic:* You will practice using the Offhand Swap key to cycle items.
    * *Example:* Your Sword is wrongly placed in Slot 3. You will practice hovering over it, swapping it to your offhand, moving to Slot 1, and swapping again to place it correctly.

### Happy Practicing!
This is my very first project using Python! I built this primarily for my own practice, so while the code might not be the most optimized in the world, it works exactly as intended for training muscle memory.

I hope you find it as useful as I do!

## ⚖️ License & Legal Disclaimer

**Source Code:**
The source code of this project is licensed under the **MIT License**. You are free to modify and distribute the code logic.

**Assets (Art & Audio):**
This project uses textures and sounds from **Minecraft**, which are the intellectual property of **Mojang Studios / Microsoft**. These assets are used for educational and fan-practice purposes only.
* **Textures & Sounds:** © Mojang Studios.
* **Font:** "Minecraftia" is a fan-made font, designed by JDGrapichs. © 2017 by Jacob Debono.

**Disclaimer:**
This application is **NOT** an official Minecraft product. It is not approved by or associated with Mojang or Microsoft.