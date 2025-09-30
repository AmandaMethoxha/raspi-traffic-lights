# Raspberry Pi Traffic Lights (with Pedestrian Button)

Finite-state traffic lights using a Raspberry Pi: **Red → Red+Amber → Green → Amber → Red** with a **pedestrian request button** that shortens green and holds red safely. Built with Python and `gpiozero`.

> Demo video + wiring photo recommended here 👇  
> ![Demo](images/demo.gif)  
> ![Wiring](images/wiring.jpg)

---

## ✨ What this shows 
- Clear **finite-state machine** design (timed phases + input handling)
- **Debounced** button input via internal pull-ups (no external resistors)
- Safe **GPIO** practices (per-LED series resistors)
- Clean code structure, comments, and readme
- Easy stretch goals (web UI, config, tests) listed below

---

## 🧰 Hardware

| Item | Qty | Notes |
|---|---:|---|
| Raspberry Pi (40-pin header) | 1 | Pi 3/4/5 works |
| LEDs: Red, Amber, Green | 3 | Any 3mm/5mm |
| Resistors 220–330 Ω | 3 | One per LED (series) |
| 6×6 mm tactile push button | 1 | 4-leg, momentary |
| Breadboard + male–male jumpers | – | — |

### Pin map (BCM numbering)

| Function | GPIO | Pi pin |
|---|---:|---:|
| Red LED | **17** | 11 |
| Amber LED | **27** | 13 |
| Green LED | **22** | 15 |
| Button | **23** | 16 |
| Ground | — | 6 (any GND) |

> LED wiring: **GPIO → resistor → LED anode (long leg)**, then LED **cathode (short leg) → GND**.  
> Button wiring: **GPIO23 ↔ one side**, **GND ↔ the other side**, button **straddles** the breadboard center gap.

---

## 🧪 Software setup & run

```bash
# On the Pi
sudo apt update
sudo apt install -y python3-gpiozero

# Clone this repo
git clone https://github.com/AmandaMethoxha/raspi-traffic-lights.git
cd raspi-traffic-lights

# Run
python3 traffic_lights.py
```

Stop with **Ctrl+C**.

---

## 🧠 How the logic works

**Normal cycle**  
`RED (6s) → RED+AMBER (2s) → GREEN (6s) → AMBER (2s) → RED…`

**Pedestrian button (GPIO23)**  
- If pressed during **GREEN** → finish green early → **AMBER → RED** and **hold** red briefly for crossing, then continue.
- If pressed during **RED** → **extend RED** slightly once.
- Presses during **AMBER/RED+AMBER** are effectively served at the next **RED**.

### Mini state diagram

```
 [RED] --2s--> [RED+AMBER] --→ [GREEN] --2s--> [AMBER] --→ [RED]
    ^                             | (button)          |
    |--------(serve/extend)-------'-------------------'
```

---

## 📄 Main script

`traffic_lights.py`:

---

## 🔍 Quick diagnostics (optional)

**Test LEDs (5s each):**
```python
from gpiozero import LED; from time import sleep
for name,p in (("RED",17),("AMBER",27),("GREEN",22)):
    led = LED(p); print("ON", name); led.on(); sleep(5); led.off()
```

**Test button:**
```python
from gpiozero import Button; from time import sleep
btn = Button(23, pull_up=True, bounce_time=0.05)
print("Press the button…")
prev=None
while True:
    now=btn.is_pressed
    if now!=prev: print("pressed" if now else "released"); prev=now
    sleep(0.05)
```

---

## 🧯 Safety & common gotchas
- **Always** put a **220–330 Ω resistor in series** with each LED.  
- LED polarity matters: **long leg = anode (+)**.  
- Breadboard **center gap**: the button must **straddle** it; LEDs/resistors must be in **different rows** (not shorted).  
- Many breadboards have **split power rails**—bridge the halves or keep all GND wires on the same half.

---

## 📦 Repo structure

```
raspi-traffic-lights/
├─ traffic_lights.py
├─ README.md
├─ requirements.txt
├─ images/
│  ├─ wiring.jpg
│  └─ demo.gif
└─ LICENSE
```

`requirements.txt`:
```
gpiozero
```

---

## 🚀 Run on boot (optional)

Create a systemd service so it starts automatically:

```bash
sudo nano /etc/systemd/system/traffic-lights.service
```

Paste:
```
[Unit]
Description=Raspberry Pi Traffic Lights
After=network.target

[Service]
ExecStart=/usr/bin/python3 /home/pi/raspi-traffic-lights/traffic_lights.py
WorkingDirectory=/home/pi/raspi-traffic-lights
Restart=on-failure
User=pi

[Install]
WantedBy=multi-user.target
```

Enable:
```bash
sudo systemctl daemon-reload
sudo systemctl enable --now traffic-lights.service
```

Stop later with:
```bash
sudo systemctl stop traffic-lights.service
```

---

## 🔮 Stretch goals (nice CV boosters)
- **Pedestrian “WALK” LED/buzzer** that blinks during the red hold
- **Config file** (`config.yaml`) for timings and pins
- **CLI options** (`--speed 2x`, `--demo`)
- **Unit tests** (mock `gpiozero`), linting, pre-commit hooks
- **Web panel** (Flask) showing the current phase + a “request crossing” button
- **Metrics** (cycle counts, button presses) written to a log or CSV

---

## 📜 License
MIT 

