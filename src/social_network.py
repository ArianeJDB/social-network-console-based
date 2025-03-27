
from collections import defaultdict
import datetime
import re

class SocialNetwork:
    def __init__(self):
        self.messages = defaultdict(list)

    def input_manager(self, get_now=datetime.datetime.now):
        command = input("> ")
        
        if "->" not in command  and len(command.split()) == 1:
            self.read_messages_by(command)
        
        if not re.match(r'\w+\s->', command):
            return True
        
        if not re.match(r'\w+\s->\s\w+', command):
            return True
        
        self.store_message(command, get_now)
        return True
    
    def store_message(self, command, get_now=datetime.datetime.now):
        username, message = command.split(" -> ")
        self.messages[username].append({
            "message": message,
            "timestamp": get_now()
        })
        return self.messages[username]

    def read_messages_by(self, username, get_now=None):
        if get_now is None:
            get_now = datetime.datetime.now 
        now = get_now()
        
        for message in self.messages.get(username):
            time_diff = now - message['timestamp']
            minutes_ago = int(time_diff.total_seconds() // 60)
            time_display = f"{minutes_ago} min ago"
            print(f"{message['message']} ({time_display})")

    
if __name__ == "__main__":
    manager = SocialNetwork()
    while True:
        if not manager.input_manager():
            break