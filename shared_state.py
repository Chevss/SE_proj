import json
import os
from portalocker import lock, unlock, LOCK_EX
import user_logs
from datetime import datetime

void_list = []

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

def void_items(purchase_list, update_purchase_display, update_total_label):  # Access void_list from the global scope
    
    # Get current timestamp
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Move items from purchase_list to void_list, adding timestamp to each item
    for item in purchase_list:
        item['timestamp'] = timestamp
        void_list.append(item)

    # Clear purchase_list after moving items
    purchase_list.clear()

    # Update display of products being purchased and total label
    update_purchase_display()
    update_total_label()

    print("shared_state.py - void_list:", void_list)

    # Log the action of voiding the transaction
    action = "Voided transaction."
    user_logs.log_actions(current_user, action)

abouts = load_about()
