import json
import os
from portalocker import lock, unlock, LOCK_EX

# Event handling mechanism
class EventDispatcher:
    def __init__(self):
        self.handlers = []

    def add_handler(self, handler):
        self.handlers.append(handler)

    def dispatch(self):
        for handler in self.handlers:
            handler()

abouts = {}
current_user = None
current_user_loa = None

ABOUT_FILE = 'abouts.json'
event_dispatcher = EventDispatcher()

def load_about():
    try:
        with open(ABOUT_FILE, 'r') as file:
            data = json.load(file)
            if isinstance(data, dict):
                return data
            return {}
    except FileNotFoundError:
        return {}

def save_about():
    with open(ABOUT_FILE, 'w') as file:
        lock(file, LOCK_EX)
        json.dump(abouts, file)
        unlock(file)
    os.chmod(ABOUT_FILE, 0o600)
    event_dispatcher.dispatch()  # Notify listeners after saving

abouts = load_about()