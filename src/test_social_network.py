from collections import defaultdict
import pytest
from unittest.mock import patch

from social_network import SocialNetwork


social_network = SocialNetwork()

def test_stores_message_posted():
    social_network.messages = defaultdict(list)
    with patch('builtins.input', return_value="username -> test message"):
            social_network.input_manager()

    assert "username" in social_network.messages
    assert {"message": "test message"} in social_network.messages["username"]