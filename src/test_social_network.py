from collections import defaultdict
import pytest
from unittest.mock import patch

from social_network import SocialNetwork


social_network = SocialNetwork()

def test_stores_message_posted():
    social_network.messages = defaultdict(list)
    with patch('builtins.input', return_value="username -> test message"), \
        patch.object(social_network, 'store_message') as mock_store_message:
            social_network.input_manager()

    mock_store_message.assert_called_once_with("username -> test message")
    expected_message = social_network.store_message("username -> test message")
    assert expected_message == [{"message": "test message"}]
    assert "username" in social_network.messages
    assert {"message": "test message"} in social_network.messages["username"]
