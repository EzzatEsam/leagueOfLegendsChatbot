from lol_chatter_backend.LolGeminiClient.functions import *


def test_get_champion_data():
    # Test existing champions
    assert get_champion_data("Ahri")["name"] == "Ahri"
    assert get_champion_data("yasuo")["name"] == "Yasuo"

    # Test non-existing champion
    assert get_champion_data("unknown") is None

    # Test case insensitivity and stripping whitespace
    assert get_champion_data("   AHRI   ")["name"] == "Ahri"


def test_get_item_data():
    # Test existing items
    assert get_item_data("Infinity Edge")["name"] == "Infinity Edge"
    assert get_item_data("Rapid Firecannon")["name"] == "Rapid Firecannon"

    # Test non-existing item
    assert get_item_data("unknown_item") is None

    # Test case insensitivity and stripping whitespace
    assert get_item_data("  infinity_edge  ")["name"] == "Infinity Edge"
    
    
def test_get_champions_names():
    assert get_champ_names()
    assert "ahri" in get_champ_names()
    assert "yasuo" in get_champ_names()
    
    
