
from collections import defaultdict


class SocialNetwork:
    def __init__(self):
        self.messages = defaultdict(list)

    def input_manager(self):
        command = input("> ")

        self.store_message(command)
        return True
    
    def store_message(self, command):
        username, message = command.split(" -> ")
        self.messages[username].append({
            "message": message
        })

if __name__ == "__main__":
    manager = SocialNetwork()
    while True:
        if not manager.input_manager():
            break