
from collections import defaultdict
import datetime
import re

class SocialNetwork:
    def __init__(self):
        self.messages = defaultdict(list)
        self.following = defaultdict(list)

    def input_manager(self, get_now=datetime.datetime.now):
        command = input("> ")
        is_one_word = len(command.split()) == 1

        if "follows" in command:
            user, user_to_follow = command.split(" follows ")
            self.store_following(user, user_to_follow)

        if "wall" in command:
            username = command.split(" wall")[0]
            self.show_wall(username, get_now=datetime.datetime.now)

        if "->" not in command  and is_one_word:
            self.read_messages_by(command)
        
        if not self.isUsernamePresentBeforeArrow(command):
            return True
        
        if not self.isMessagePresentAfterArrow(command):
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

    def read_messages_by(self, username, get_now=None, show_username=False):
        if get_now is None:
            get_now = datetime.datetime.now 
        now = get_now()
        
        for message in self.messages.get(username, []):
            time_diff = now - message['timestamp']
            minutes_ago = int(time_diff.total_seconds() // 60)
            time_display = f"{minutes_ago} min ago"
            
            if show_username:
                print(f"{username} - {message['message']} ({time_display})")
            else:
                print(f"{message['message']} ({time_display})")
    
    def store_following(self, user, user_to_follow):
        self.following[user].append({
            "following": user_to_follow
        })
        return self.following[user]
    
    def show_wall(self, username, get_now=datetime.datetime.now):
        self.read_messages_by(username, get_now, True)

        followed_users = self.get_following(username)

        for followed_user in followed_users:
            self.read_messages_by(followed_user, get_now, True)

    def get_following(self, username):
        followed_users = self.following.get(username, [])
        return [entry["following"] for entry in followed_users]
    
    @staticmethod
    def isUsernamePresentBeforeArrow(command):
        return bool(re.match(r'\w+\s->', command))
    
    @staticmethod
    def isMessagePresentAfterArrow(command):
        return bool(re.match(r'\w+\s->\s\w+', command))

if __name__ == "__main__":
    manager = SocialNetwork()
    while True:
        if not manager.input_manager():
            break