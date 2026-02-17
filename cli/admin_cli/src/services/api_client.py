import requests
import json
import os
from rich.console import Console
from config.settings import TOKENS_FILE
from rich.panel import Panel

console = Console()

class APIClient:
    def __init__(self, base_url):
        self.base_url = base_url.rstrip('/')
        self.token = self._load_token()
        self.headers = {
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        if self.token:
            self.headers["Authorization"] = f"Bearer {self.token}"

    def is_authenticated(self):
        return self.token is not None

    def _extract_access_token(self, data):
        # Handle { "access": "..." } or { "tokens": { "access": "..." } }
        if "access" in data:
            return data["access"]
        if "tokens" in data and "access" in data["tokens"]:
            return data["tokens"]["access"]
        return None

    def _load_token(self):
        if os.path.exists(TOKENS_FILE):
             try:
                 with open(TOKENS_FILE, 'r') as f:
                     data = json.load(f)
                     return self._extract_access_token(data)
             except:
                 return None
        return None

    def _save_token(self, token_data):
        with open(TOKENS_FILE, 'w') as f:
            json.dump(token_data, f)
        self.token = self._extract_access_token(token_data)
        if self.token:
            self.headers["Authorization"] = f"Bearer {self.token}"

    def login(self, username, password, login_url):
        try:
            resp = requests.post(login_url, json={"username": username, "password": password})
            if resp.status_code == 200:
                data = resp.json()
                self._save_token(data)
                return True, "Login Successful"
            else:
                return False, f"Login Failed: {resp.text}"
        except Exception as e:
            return False, str(e)

    def get(self, endpoint, params=None):
        try:
            resp = requests.get(f"{self.base_url}/{endpoint.lstrip('/')}", headers=self.headers, params=params)
            if resp.status_code == 401:
                console.print(Panel("Session Expired. Please login again.", style="bold red"))
                return None
            return resp
        except Exception as e:
            console.print(f"[bold red]Connection Error:[/bold red] {e}")
            return None

    def post(self, endpoint, data=None):
        try:
            resp = requests.post(f"{self.base_url}/{endpoint.lstrip('/')}", headers=self.headers, json=data)
            if resp.status_code == 401:
                console.print(Panel("Session Expired. Please login again.", style="bold red"))
                return None
            return resp
        except Exception as e:
            console.print(f"[bold red]Connection Error:[/bold red] {e}")
            return None
