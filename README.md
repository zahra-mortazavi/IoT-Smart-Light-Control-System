
# 💡 IoT Light Control System

An **IoT-based smart lighting system** that allows you to control two LED lights (Kitchen & Room) using **natural language commands**.

Commands can be sent through:

* 🤖 **Telegram Bot**
* 🌐 **Simple Web Interface**

The system uses an **ESP32 microcontroller** connected to a computer via **USB serial**. Python scripts interpret natural language commands using an **LLM** and convert them into control signals for the LEDs.

---

# 🧠 System Architecture

The project consists of three main components:

### 1️⃣ ESP32 Microcontroller

* Hosts a **Wi-Fi connection**
* Runs a **simple web server**
* Receives commands from the PC through **Serial (USB)**
* Controls LEDs via GPIO pins

### 2️⃣ Python Telegram Bot

* Listens for messages from Telegram
* Sends user commands to an **LLM (GPT-3.5)** for interpretation
* Converts the response into a **single control letter (A–H)**
* Sends the command to ESP32 through **serial**

### 3️⃣ Python Web Companion Script

* Works with the **ESP32 web interface**
* Receives natural language commands from the ESP32
* Processes them with the **LLM**
* Sends the resulting command back to the ESP32

⚠️ Only **one Python script can run at a time** because both require access to the same serial port.

---

# 🧰 Hardware Requirements

| Component    | Description                             |
| ------------ | --------------------------------------- |
| ESP32        | Development board                       |
| LEDs         | Two LEDs (or LED modules)               |
| Resistors    | Current limiting (220–330Ω recommended) |
| Jumper wires | For connections                         |
| USB cable    | ESP32 → Computer                        |

---

# 🔌 Wiring

| Light         | ESP32 Pin |
| ------------- | --------- |
| Kitchen Light | GPIO 33   |
| Room Light    | GPIO 4    |

Connect each LED with a resistor between the GPIO pin and **GND**.

---

# 💻 Software Requirements

## Python Environment

Python **3.8+** is required.

Install dependencies:

```bash
pip install pyserial langchain-openai python-telegram-bot
```

You also need an **OpenAI-compatible API key**.

The code currently uses:

```
https://api.avalai.ir/v1
```

You can replace it with your own API endpoint.

---

# ⚙️ Setup Guide

## 1️⃣ ESP32 Setup

Open the sketch:

```
ESP32/ESP32.ino
```

Configure your Wi-Fi credentials:

```cpp
const char *ssid = "your-ssid";
const char *password = "your-password";
```

Upload the code to the ESP32 using **Arduino IDE**.

After uploading:

1. Open **Serial Monitor**
2. Set baud rate to **115200**
3. Copy the **IP address** printed in the terminal

You will use this IP to access the **web interface**.

---

# 🐍 Python Setup

It is recommended to create a virtual environment.

```bash
python -m venv venv
source venv/bin/activate   # Linux / Mac
venv\Scripts\activate      # Windows
```

Install dependencies:

```bash
pip install pyserial langchain-openai python-telegram-bot
```

---

# 🤖 Telegram Bot Setup

Edit the file:

```
Telegram/main.py
```

Replace:

```python
"TELEGRAM_BOT_TOKEN"
```

with your bot token from **@BotFather**.

Also replace:

```python
api_key="YOUR_ACTUAL_API_KEY"
```

Set the correct **serial port**:

Examples:

| OS      | Example            |
| ------- | ------------------ |
| Windows | COM4               |
| Linux   | /dev/ttyUSB0       |
| Mac     | /dev/tty.usbserial |

Run the bot:

```bash
python Telegram/main.py
```

---

# 🌐 Web Interface Setup

Run the companion script:

```bash
python Web/main.py
```

Then open your browser:

```
http://<ESP32_IP>
```

Example:

```
http://192.168.1.85
```

You will see a simple input form where you can type commands like:

```
turn on the kitchen light
```

---

# 🗣 Example Commands

The system understands natural language such as:

```
turn on the kitchen light
switch off the room light
turn on both lights
room on kitchen off
```

---

# ⚡ Command Mapping

The LLM converts commands into **one of eight actions**:

| Letter | Action               |
| ------ | -------------------- |
| A      | Kitchen ON           |
| B      | Kitchen OFF          |
| C      | Room ON              |
| D      | Room OFF             |
| E      | Both ON              |
| F      | Both OFF             |
| G      | Room ON, Kitchen OFF |
| H      | Kitchen ON, Room OFF |

The Python script sends this **single letter** to the ESP32.

---

# 🔁 How It Works

### 1️⃣ Natural Language Processing

User input → sent to **LLM (GPT-3.5)** → converted to command letter.

### 2️⃣ Serial Communication

Python sends the letter via **USB serial**.

### 3️⃣ ESP32 Execution

ESP32 reads the letter and sets the appropriate **GPIO pins**.

---

# 📁 Project Structure

```
project/
│
├── Telegram/
│   └── main.py
│
├── Web/
│   └── main.py
│
└── ESP32/
    └── ESP32.ino
```

| Folder   | Description                  |
| -------- | ---------------------------- |
| Telegram | Telegram bot implementation  |
| Web      | Web interface serial handler |
| ESP32    | ESP32 firmware               |

---

# 🛠 Troubleshooting

### Serial Port Error

* Ensure the correct port is selected
* Close other programs using the port

Linux users may need:

```bash
sudo usermod -a -G dialout $USER
```

---

### LLM Not Responding

Check:

* API key
* Base URL configuration

---

### ESP32 Not Connecting to Wi-Fi

Verify:

* SSID
* Password
* Network range

---

### LEDs Not Working

Check:

* Wiring
* Resistors
* GPIO pin numbers (33 & 4)

---

# 🔧 Customization Ideas

You can extend the system by:

### ➕ Adding More Lights

Modify:

* LLM prompt
* ESP32 `SetUpLights()` function

### 🧠 Using Another LLM

Change:

```python
model="gpt-3.5-turbo"
base_url="..."
```

### 🔒 Securing the Web Interface

For production use:

* Authentication
* HTTPS

---

# 📜 License

This project is licensed under the **MIT License**.

---

باشد؛ که README پروژه را **چند سطح حرفه‌ای‌تر** می‌کند.
