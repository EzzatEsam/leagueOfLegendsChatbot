from lol_chatter_backend.LolDataFetcher import (
    items_processed,
    champions_processed,
    patches,
)
import difflib


def get_latest_patch() -> str:
    """
    Retrieves the latest patch name from the patches list.

    Returns:
        str: The latest patch.
    """
    return patches[-1]


def get_champion_data(champion_name: str) -> dict:
    """
    Retrieves the data for a champion based on the given champion name.

    Args:
        champion_name (str): The name of the champion.

    Returns:
        dict: The data for the champion if found, None otherwise.
    """
    champion_name = champion_name.strip().lower()
    champ = champions_processed.get(champion_name, None)
    if champ is None:
        closest_match = difflib.get_close_matches(
            champion_name, list(champions_processed.keys())
        )
        if closest_match:
            return get_champion_data(closest_match[0])

    return champ


def get_item_data(item_name: str) -> dict:
    """
    Retrieves the data for an item based on the given item name.

    Args:
        item_name (str): The name of the item.

    Returns:
        dict: The data for the item if found, None otherwise.
    """
    item_name = item_name.strip().lower()
    item = items_processed.get(item_name, None)
    if item is None:
        closest_match = difflib.get_close_matches(
            item_name, list(items_processed.keys())
        )
        if closest_match:
            return get_item_data(closest_match[0])
    return item


def get_item_names() -> list[str]:
    """
    Retrieves the names of items stored in the items_processed dictionary.

    Returns:
        list[str]: A list of item names.
    """
    return list(items_processed.keys())


def get_champ_names() -> list[str]:
    """
    Returns a list of all the keys in the `champions_processed` dictionary.

    :return: A list of strings representing the names of all champions.
    :rtype: list[str]
    """
    return list(champions_processed.keys())


helper_functions = [
    get_latest_patch,
    get_champ_names,
    get_champion_data,
    get_item_data,
    get_item_names,
]
