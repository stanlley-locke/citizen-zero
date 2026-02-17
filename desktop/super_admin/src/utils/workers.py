from PyQt6.QtCore import QThread, pyqtSignal
import requests

class ApiWorker(QThread):
    """
    Generic worker thread for making API calls without freezing the UI.
    """
    finished = pyqtSignal(dict)
    error = pyqtSignal(str)

    def __init__(self, url, method='GET', data=None, params=None):
        super().__init__()
        self.url = url
        self.method = method
        self.data = data
        self.params = params

    def run(self):
        try:
            if self.method == 'GET':
                response = requests.get(self.url, params=self.params)
            elif self.method == 'POST':
                response = requests.post(self.url, json=self.data)
            elif self.method == 'PUT':
                response = requests.put(self.url, json=self.data)
            elif self.method == 'DELETE':
                response = requests.delete(self.url)
            else:
                self.error.emit(f"Unsupported method: {self.method}")
                return

            # Check status
            if response.status_code >= 400:
                self.error.emit(f"API Error {response.status_code}: {response.text}")
            else:
                try:
                    self.finished.emit(response.json())
                except ValueError:
                    self.finished.emit({"status": "success", "data": response.text})

        except requests.exceptions.RequestException as e:
            self.error.emit(str(e))
