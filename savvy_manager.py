import flet as ft
import requests
import json
import os

# 1. PRE-FLIGHT CONFIGURATION
DB_FILE = "savvy_shop_vault.json"
UPLOAD_DIR = "uploads"
os.environ["FLET_SECRET_KEY"] = "savvy_aviation_local_key"

if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

def load_vault():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r") as f:
            try: return json.load(f)
            except: return {}
    return {}

def save_to_vault(name, token, aircraft_id, registration):
    vault = load_vault()
    vault[registration] = {"nickname": name, "token": token, "id": aircraft_id}
    with open(DB_FILE, "w") as f:
        json.dump(vault, f)

def main(page: ft.Page):
    page.title = "Savvy Aircraft Data Manager"
    page.theme_mode = "dark"
    page.padding = 30
    
    selected_aircraft = ft.Ref[ft.Dropdown]()
    log_output = ft.Column(scroll="always", height=250)
    token_input = ft.TextField(label="Savvy API Token", password=True, can_reveal_password=True, expand=True)
    name_input = ft.TextField(label="Aircraft Nickname", width=200)

    def write_log(message, color=ft.colors.WHITE):
        # Basic de-duplicator: don't post the exact same message twice in a row
        if log_output.controls and log_output.controls[-1].value == f"> {message}":
            return
        log_output.controls.append(ft.Text(f"> {message}", color=color, size=12))
        page.update()

    # --- UPLOAD STAGE 2: LOCAL TO SAVVY ---
    def on_upload_complete(e: ft.FilePickerUploadEvent):
        reg = selected_aircraft.current.value
        if not reg: return
        
        client = load_vault()[reg]
        temp_path = os.path.join(os.getcwd(), UPLOAD_DIR, e.file_name)
        
        write_log(f"Pushing {e.file_name} to Savvy S3...", ft.colors.BLUE_200)
        
        try:
            req_url = f"https://apps.savvyaviation.com/request_upload_url/{client['id']}/"
            res = requests.post(req_url, data={"token": client['token'], "filename": e.file_name})
            data = res.json()

            with open(temp_path, "rb") as f:
                file_bytes = f.read()

            s3_res = requests.post(
                data["upload_url"], 
                data=data["fields"], 
                files={"file": (e.file_name, file_bytes)}
            )
            
            if s3_res.status_code in [200, 204]:
                write_log(f"SUCCESS: {e.file_name} is now at Savvy.", ft.colors.GREEN)
                if os.path.exists(temp_path): os.remove(temp_path)
            else:
                write_log(f"S3 Error: {s3_res.status_code}", ft.colors.RED)
        except Exception as ex:
            write_log(f"Upload Error: {ex}", ft.colors.RED)

    # --- UPLOAD STAGE 1: BROWSER TO LOCAL ---
    def start_upload_sequence(e: ft.FilePickerResultEvent):
        if not e.files or not selected_aircraft.current.value:
            return

        file = e.files[0]
        write_log(f"Transferring {file.name} to local processing...", ft.colors.BLUE_400)
        
        file_picker.upload(
            [ft.FilePickerUploadFile(
                file.name,
                upload_url=page.get_upload_url(file.name, 600),
            )]
        )

    # --- UI ACTIONS ---
    def handle_confirm_clear(e):
        if os.path.exists(DB_FILE): os.remove(DB_FILE)
        confirm_dialog.open = False
        write_log("VAULT ERASED.", ft.colors.RED)
        refresh_dropdown()

    confirm_dialog = ft.AlertDialog(
        title=ft.Text("Confirm Data Wipe"),
        content=ft.Text("Erase all saved aircraft and tokens?"),
        actions=[
            ft.ElevatedButton("Yes, Erase", on_click=handle_confirm_clear, bgcolor="red", color="white"),
            ft.TextButton("Cancel", on_click=lambda _: [setattr(confirm_dialog, 'open', False), page.update()]),
        ],
    )

    def add_new_client(e):
        token = token_input.value
        if not token: return
        write_log("Verifying token...")
        try:
            res = requests.post("https://apps.savvyaviation.com/get-aircraft/", data={"token": token})
            if res.status_code == 200:
                for p in res.json():
                    save_to_vault(name_input.value, token, p['id'], p['registration_no'])
                    write_log(f"Added {p['registration_no']}", ft.colors.GREEN)
                token_input.value = ""; name_input.value = ""; refresh_dropdown()
            else: write_log("Invalid Token.", ft.colors.RED)
        except Exception as ex: write_log(f"Error: {ex}", ft.colors.RED)

    def refresh_dropdown():
        vault = load_vault()
        if selected_aircraft.current:
            selected_aircraft.current.options = [ft.dropdown.Option(reg) for reg in vault.keys()]
            page.update()

    file_picker = ft.FilePicker(on_result=start_upload_sequence, on_upload=on_upload_complete)
    page.overlay.append(file_picker)

    page.add(
        ft.Row([ft.Icon(ft.icons.AIRPLANEMODE_ACTIVE, color="blue", size=30), ft.Text("Savvy Aircraft Data Manager", size=28, weight="bold")]),
        ft.Card(ft.Container(padding=20, content=ft.Column([
            ft.Text("Manage Aircraft Tokens", weight="bold"),
            ft.Row([name_input, token_input]),
            ft.Row([
                ft.ElevatedButton("Add Aircraft", icon=ft.icons.ADD, on_click=add_new_client),
                ft.ElevatedButton("Clear Vault", icon=ft.icons.DELETE_FOREVER, on_click=lambda _: [setattr(page, 'dialog', confirm_dialog), setattr(confirm_dialog, 'open', True), page.update()], color="red"),
            ])
        ]))),
        ft.Divider(height=40),
        ft.Text("Upload Engine Data Logs", size=20, weight="bold"),
        ft.Row([
            ft.Dropdown(ref=selected_aircraft, label="Select Aircraft", width=350),
            ft.ElevatedButton("Select & Upload Log", icon=ft.icons.UPLOAD_FILE, on_click=lambda _: file_picker.pick_files()),
        ]),
        ft.Container(content=log_output, bgcolor="black", padding=15, border_radius=10, border=ft.border.all(1, ft.colors.GREY_800))
    )
    refresh_dropdown()

# LAUNCH
ft.app(target=main, view=ft.AppView.WEB_BROWSER, upload_dir=UPLOAD_DIR)
