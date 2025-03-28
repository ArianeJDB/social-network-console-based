from collections import defaultdict
from datetime import datetime, timedelta
import pytest
from unittest.mock import Mock, patch

from social_network import SocialNetwork


social_network = SocialNetwork()

@pytest.fixture(autouse=True)
def clear_messages():
    social_network.messages.clear()

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

def test_message_is_not_stored_when_does_not_contain_an_arrow():
    fixed_time = datetime.now()
    mock_now = Mock(return_value=fixed_time)
    
    with patch.object(social_network, 'store_message') as mock_store_message, \
        patch('builtins.input', return_value="username a message"):
            social_network.input_manager(get_now=mock_now)
    
    mock_store_message.assert_not_called()

def test_message_is_not_stored_when_does_not_have_username_before_the_arrow():
    fixed_time = datetime.now()
    mock_now = Mock(return_value=fixed_time)

    with patch.object(social_network, 'store_message') as mock_store_message, \
        patch('builtins.input', return_value="-> message"):
            social_network.input_manager(get_now=mock_now)
        
    mock_store_message.assert_not_called()

def test_message_is_not_stored_when_does_not_have_message_after_the_arrow():
    fixed_time = datetime.now()
    mock_now = Mock(return_value=fixed_time)

    with patch.object(social_network, 'store_message') as mock_store_message, \
        patch('builtins.input', return_value="username ->"):
            social_network.input_manager(get_now=mock_now)
        
    mock_store_message.assert_not_called()

def test_reads_messages_by_username_when_command_does_not_have_arrow_and_is_only_one_word():
    fixed_time = datetime.now()
    mock_now = Mock(return_value=fixed_time)
    
    with patch.object(social_network, 'store_message') as mock_store_message, \
         patch.object(social_network, 'read_messages_by') as mock_read_messages, \
         patch('builtins.input', return_value="username"), \
        patch('builtins.print') as mock_print:
            social_network.input_manager(get_now=mock_now)
    
    mock_store_message.assert_not_called()
    mock_read_messages.assert_called_once_with("username")

def test_reads_messages_by_username_and_prints_message_with_time_ago():
    fixed_time = datetime.now() - timedelta(minutes = 5)

    with patch("datetime.datetime") as mock_datetime, \
        patch('builtins.print') as mock_print:
        mock_datetime.now.return_value = datetime.now() 
        
        social_network.store_message("username -> message", get_now=lambda: fixed_time)  
        social_network.read_messages_by("username", get_now=mock_datetime.now) 

    mock_print.assert_called_with("message (5 min ago)")

def test_when_username_does_not_exist_messages_dont_print(): 
    fixed_time = datetime.now()
    mock_now = Mock(return_value=fixed_time)
    
    with patch.object(social_network, 'store_message') as mock_store_message, \
         patch.object(social_network, 'read_messages_by') as mock_read_messages, \
         patch('builtins.print') as mock_print, \
         patch('builtins.input', return_value="nonexistentUsername"):
        
        social_network.input_manager(get_now=mock_now)
    
    mock_store_message.assert_not_called()
    mock_read_messages.assert_called_once_with("nonexistentUsername")
    mock_print.assert_not_called()

def test_stores_following_when_command_contains_follows():
    fixed_time = datetime.now()
    mock_now = Mock(return_value=fixed_time)
    social_network.following = defaultdict(list)

    with patch('builtins.input', return_value="username follows anotherUsername"), \
        patch.object(social_network, 'store_following') as mock_following:
            social_network.input_manager(get_now=mock_now)

    mock_following.assert_called_once()
    mock_following.assert_called_with("username", "anotherUsername")
    expected_following = social_network.store_following("username", "anotherUsername")
    assert expected_following == [{"following": "anotherUsername"}]
    assert "username" in social_network.following

def test_wall_displays_followed_users_messages():
    fixed_time = datetime.now()
    mock_now = Mock(return_value=fixed_time)
    social_network.messages = defaultdict(list)
    social_network.following = defaultdict(list)
    
    social_network.store_following("user", "user_followed")
    social_network.store_message("user_followed -> Message", mock_now)
    
    with patch('builtins.input', return_value="user wall"), \
         patch('builtins.print') as mock_print:
        social_network.input_manager(get_now=mock_now)
        
    mock_print.assert_any_call("user_followed - Message (0 min ago)")
    assert mock_print.call_count == 1

def test_wall_displays_only_own_messages_when_does_not_follows_anybody():
    fixed_time = datetime.now()
    mock_now = Mock(return_value=fixed_time)
    
    social_network.messages = defaultdict(list)
    social_network.following = defaultdict(list)
    
    social_network.store_message("user -> My own message", mock_now)
    
    with patch('builtins.input', return_value="user wall"), \
         patch('builtins.print') as mock_print:
        social_network.input_manager(get_now=mock_now)
        
    mock_print.assert_any_call("user - My own message (0 min ago)")
    assert mock_print.call_count == 1

def test_wall_displays_followed_users_messages_and_own_messages():
    fixed_time = datetime.now()
    mock_now = Mock(return_value=fixed_time)
    
    social_network.store_following("user", "user_followed")
    social_network.store_message("user_followed -> Message from user that is followed", mock_now)
    social_network.store_message("user -> My own message", mock_now)
    
    with patch('builtins.input', return_value="user wall"), \
         patch('builtins.print') as mock_print:
        social_network.input_manager(get_now=mock_now)
        
    mock_print.assert_any_call("user - My own message (0 min ago)")
    mock_print.assert_any_call("user_followed - Message from user that is followed (0 min ago)")
    assert mock_print.call_count == 2
