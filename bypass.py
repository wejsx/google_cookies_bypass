import requests
import json
import subprocess
import os

from websockets.sync.client import connect


DEBUG_PORT = 9222
DEBUG_URL = f'http://localhost:{DEBUG_PORT}/json'
CHROME_PATH = rf"C:\Program Files\Google\Chrome\Application\chrome.exe"
LOCAL_APP_DATA = os.getenv('LOCALAPPDATA')
USER_DATA_DIR = rf'{LOCAL_APP_DATA}\google\chrome\User Data'


def get_debug_ws_url():
    res = requests.get(DEBUG_URL)
    data = res.json()
    return data[0]['webSocketDebuggerUrl'].strip()

def kill_chrome():
    subprocess.run('taskkill /F /IM chrome.exe', check=False, shell=False, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def start_debugged_chrome():
    subprocess.Popen([CHROME_PATH, f'--remote-debugging-port={DEBUG_PORT}', '--remote-allow-origins=*', '--headless', f'--user-data-dir={USER_DATA_DIR}'], stdout=subprocess.DEVNULL)


if __name__ == "__main__":
    kill_chrome()
    start_debugged_chrome()
    url = get_debug_ws_url()

    with connect(url) as websocket:
        websocket.send(json.dumps({'id': 1, 'method': 'Network.getAllCookies'}))
        message = websocket.recv()
        print(message)
        response = json.loads(message)
        cookies = response['result']['cookies']
        print(json.dumps(cookies, indent=4))
        websocket.close()
        kill_chrome()