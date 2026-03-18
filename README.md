# savvy-aircraft-manager

This is an app that will open a web browser and allow uploading engine log data to a Savvy Aviation Maintenance account. 
It can store multiple aircraft/token combinations. This private information is stored in savvy_shop_vault.json

Prerequisites
This application is optimized for Python 3.10+ and has been tested on Linux (Mint/Ubuntu) using the Flet web-view for maximum stability.

Dependencies
Flet (v0.21.2): Used for the UI framework. Note: Version 0.21.2 is required for stable FilePicker performance on Linux systems for some unknown reason.

Requests: Handles the API communication with Savvy Aviation and the S3 file upload.

Quick Start:

# 1. Clone the repository
git clone https://github.com/your-username/savvy-aircraft-manager.git
cd savvy-aircraft-manager

# 2. Create and activate a virtual environment
python3 -m venv venv
source venv/bin/activate

# 3. Install specific dependencies
pip install -r requirements.txt

# 4. Launch the manager
python3 savvy_app_27a.py
