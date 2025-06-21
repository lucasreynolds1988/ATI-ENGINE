# ~/Soap/rotor_overlay.py

from textual.app import App, ComposeResult
from textual.containers import Vertical
from textual.widgets import Static, Header, Footer, Button
import subprocess
import os

class RotorOverlay(App):
    CSS_PATH = None

    def compose(self) -> ComposeResult:
        yield Header()
        yield Static("🧠 FUSION ENGINE OVERLAY — LIVE", id="title")
        yield Static(f"Disk Usage: {self.get_disk_usage()}", id="disk")
        yield Static("🌀 ROTOR STATUS: RUNNING\n📦 GitHub | 🧱 MongoDB | ☁️ GCS", id="status")
        yield Button("🔁 Trigger +CODE-RED+", id="code_red")
        yield Button("💾 Restore w/ fusion_loader.py", id="restore")
        yield Footer()

    def get_disk_usage(self):
        result = subprocess.run("df -h /home", shell=True, capture_output=True, text=True)
        return result.stdout.splitlines()[-1]

    def on_button_pressed(self, event):
        button_id = event.button.id
        if button_id == "code_red":
            self.push_screen("Triggering +CODE-RED+...")
            subprocess.Popen(["python3", "rotor_fusion.py"])
        elif button_id == "restore":
            self.push_screen("Running fusion_loader.py...")
            subprocess.Popen(["python3", "fusion_loader.py"])

if __name__ == "__main__":
    RotorOverlay().run()
