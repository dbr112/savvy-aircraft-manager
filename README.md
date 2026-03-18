# Savvy Aircraft Data Manager

A lightweight Python utility designed to manage multiple Savvy Aviation aircraft tokens and streamline the process of uploading engine data logs (`.jpi`, `.csv`, etc.) directly to Savvy's servers.

This app uses a web-based interface for maximum compatibility on Linux systems, bypassing GUI rendering issues.

---

## ✈️ Features
* **Multi-Aircraft Support:** Store nicknames and API tokens for various tail numbers.
* **Secure Local Vault:** Tokens are stored locally on your machine in `savvy_shop_vault.json`.
* **S3 Direct Upload:** Handles the complex "handshake" required to push logs to Savvy’s Amazon S3 storage.
* **Linux Optimized:** Specifically tuned to run on Ubuntu/Mint/Debian environments.

## 🛠️ Prerequisites
* **Python 3.10+**
* **Operating System:** Tested on Linux Mint/Ubuntu.
* **Browser:** Chrome, Brave, or Firefox.

## 📦 Dependencies
* **Flet (v0.21.2):** Chosen for its stable `FilePicker` implementation on Linux. (Note: Newer versions of Flet may require additional system-level GTK modules).
* **Requests:** Used for API communication and data streaming.

## 🚀 Quick Start

# 1. Clone the repository
git clone https://github.com/dbr112/savvy-aircraft-manager.git
cd savvy-aircraft-manager

# 2. Create and activate a virtual environment
python3 -m venv venv
source venv/bin/activate

# 3. Install specific dependencies
pip install -r requirements.txt

# 4. Launch the manager
python3 savvy_manager.py

🔒 Security & Privacy
API Tokens: Your tokens are private. This app stores them in savvy_shop_vault.json within the root folder.

.gitignore: A .gitignore file is included to ensure your private vault and temporary upload fragments are never accidentally pushed to a public repository.

Cleanup: The app automatically deletes temporary file fragments from the uploads/ folder immediately after a successful transfer.

⚠️ Known Linux Issues
If you see the message Failed to load module "xapp-gtk3-module", you can safely ignore it. This is a Linux theme warning that does not affect the app's functionality in the browser view.
