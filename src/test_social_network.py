from collections import defaultdict
from datetime import datetime
import pytest
from unittest.mock import Mock, patch

from social_network import SocialNetwork


social_network = SocialNetwork()

def test_stores_message_posted_with_timestamp():
    fixed_time = datetime.now()
    mock_now = Mock(return_value=fixed_time)
    social_network.messages = defaultdict(list)

    with patch('builtins.input', return_value="username -> test message"), \
        patch.object(social_network, 'store_message') as mock_store_message:
            social_network.input_manager(get_now=mock_now)

    mock_store_message.assert_called_once_with("username -> test message", mock_now)
    expected_message = social_network.store_message("username -> test message", mock_now)
    assert expected_message == [{"message": "test message", "timestamp": fixed_time}]
    assert "username" in social_network.messages
    assert {"message": "test message", "timestamp": fixed_time} in social_network.messages["username"]
