import pytest
from src.main import User, get_user_info

def test_get_user_info():
    """Test get_user_info function."""
    user = User("John Doe", "Operations Manager")
    assert get_user_info(user) == {"name": "John Doe", "role": "Operations Manager"}

def test_get_user_info_edge_case():
    """Test get_user_info function with edge case."""
    user = User("", "Operations Manager")
    assert get_user_info(user) == {"name": "", "role": "Operations Manager"}

def test_get_user_info_invalid_role():
    """Test get_user_info function with invalid role."""
    with pytest.raises(AttributeError):
        User("John Doe", "Invalid Role")
