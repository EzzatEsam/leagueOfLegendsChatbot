# from lol_chatter_backend.LolDataFetcher import (
#     items_processed,
#     champions_processed,
#     patches,
# )
# import difflib


# def get_latest_patch() -> str:
#     """
#     Retrieves the latest patch name from the patches list.

#     Returns:
#         str: The latest patch.
#     """
#     print("Model requested latest patch")
#     return patches[-1]


# def get_champion_data(champion_names: list[str]) -> list:
#     """
#     Retrieves the data for a list of champions based on the given champion names.

#     Args:
#         champion_names (list[str]): A list of champion names.

#     Returns:
#         list: A list of dictionaries containing the data for each champion.
#     """
#     results = []
#     for champion_name in champion_names:
#         print(f"Model requested data for {champion_name}")
#         champion_name = champion_name.strip().lower()
#         champ = champions_processed.get(champion_name, None)
#         if champ is None:
#             closest_match = difflib.get_close_matches(
#                 champion_name, list(champions_processed.keys())
#             )
#             if closest_match:
#                 champ = get_champion_data([closest_match[0]])[0]
#         results.append(champ)
#     return results


# def get_item_data(item_names: list[str]) -> list:
#     """
#     Retrieves the data for a list of items based on the given item names.

#     Args:
#         item_names (list[str]): A list of item names.

#     Returns:
#         list: A list of dictionaries containing the data for each item.
#     """
#     results = []
#     for item_name in item_names:
#         print(f"Model requested data for {item_name}")
#         item_name = item_name.strip().lower()
#         item = items_processed.get(item_name, None)
#         if item is None:
#             closest_match = difflib.get_close_matches(
#                 item_name, list(items_processed.keys())
#             )
#             if closest_match:
#                 item = get_item_data([closest_match[0]])[0]
#         results.append(item)
#     return results


# def get_item_names() -> list[str]:
#     """
#     Retrieves the names of items stored in the items_processed dictionary.

#     Returns:
#         list[str]: A list of item names.
#     """
    
#     print("Model requested item names")
#     return list(items_processed.keys())


# def get_champ_names() -> list[str]:
#     """
#     Returns a list of all the keys in the `champions_processed` dictionary.

#     :return: A list of strings representing the names of all champions.
#     :rtype: list[str]
#     """
    
#     print("Model requested champion names")
#     return list(champions_processed.keys())


# helper_functions = [
#     get_latest_patch,
#     get_champ_names,
#     get_champion_data,
#     get_item_data,
#     get_item_names,
# ]
