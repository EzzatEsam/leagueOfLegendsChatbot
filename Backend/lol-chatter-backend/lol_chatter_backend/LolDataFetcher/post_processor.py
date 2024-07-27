import copy
import pprint
import tqdm


class DataPostProcessor:
    def __init__(self, verbose: bool = True) -> None:
        self.verbose = verbose

    def get_items_list(self, items_data: dict) -> dict:
        item_id_names = {}
        for k, v in items_data.items():
            item_id_names[k] = v["name"]

        items: dict = {}
        if self.verbose:
            print(f"Preprocessing  {len(items_data.keys())} items")
            pbar = tqdm.tqdm(total=len(items_data), desc="Preprocessing items")
        for item in items_data.values():
            key = str(item["name"]).lower()
            item_processed = self._preprocess_item(item, item_id_names)
            items[key] = item_processed
            if self.verbose:

                pbar.set_description(f"Preprocessing {item['name']}")  # type: ignore
                pbar.update(1)  # type: ignore
        return items

    def get_champions_list(self, champions_data: dict) -> dict:
        champions = {}

        if self.verbose:
            print(f"Preprocessing {len(champions_data.keys())} champions")
            pbar = tqdm.tqdm(total=len(champions_data), desc="Preprocessing champions")
        for champion in champions_data.values():
            key = str(champion["name"]).lower()
            champion_processed = self._preprocess_champion(champion)
            champions[key] = champion_processed
            if self.verbose:
                pbar.set_description(f"Preprocessing {champion['name']}")  # type: ignore
                pbar.update(1)  # type: ignore
        return champions

    def _preprocess_champion(self, champion: dict) -> dict:
        new_champion = copy.deepcopy(champion)

        new_champion.pop("id", None)
        # new_champion.pop("icon", None)
        new_champion.pop("skins", None)
        new_champion.pop("key", None)

        new_champion["stats"] = self._preprocess_stats(new_champion["stats"])
        for ability_k in new_champion["abilities"].keys():
            new_champion["abilities"][ability_k] = [
                self._preprocess_ability(new_champion["abilities"][ability_k][i])
                for i in range(len(new_champion["abilities"][ability_k]))
            ]

        return new_champion

    def _preprocess_ability(self, ability: dict) -> dict:

        new_ability = copy.deepcopy(ability)
        # new_ability.pop("icon", None)

        def process_modifier_recurs(input_dict: dict) -> None:
            for k, v in input_dict.items():
                if k == "modifiers":
                    input_dict[k] = [
                        self._preprocess_modifier(modifier) for modifier in v
                    ]
                elif isinstance(v, dict):
                    process_modifier_recurs(v)
                elif isinstance(v, list):
                    for item in v:
                        if isinstance(item, dict):
                            process_modifier_recurs(item)

        process_modifier_recurs(new_ability)
        return new_ability

    def _preprocess_modifier(self, modifier: dict) -> dict:
        new_modifer = {}
        new_modifer["valuePerLevel"] = []
        for i in range(len(modifier["values"])):
            new_modifer["valuePerLevel"].append(
                f"{modifier['values'][i] :.3f}  {modifier['units'][i]}"
            )
        return new_modifer

    def _preprocess_item(self, item: dict, item_id_names: dict) -> dict:
        new_item = copy.deepcopy(item)

        # remove unecessary fields
        new_item.pop("id", None)
        new_item.pop("noEffects", None)
        new_item.pop("removed", None)
        new_item.pop("requiredAlly", None)
        # new_item.pop("icon", None)
        new_item.pop("specialRecipe", None)
        new_item.pop("iconOverlay", None)

        # remove stats with 0 values
        new_item["stats"] = self._preprocess_stats(new_item["stats"])

        # convert item ids to item names

        builds_from_names = [
            item_id_names[str(id)]
            for id in new_item["buildsFrom"]
            if str(id) in item_id_names
        ]
        builds_into_names = [
            item_id_names[str(id)]
            for id in new_item["buildsInto"]
            if str(id) in item_id_names
        ]

        new_item["buildsFrom"] = builds_from_names
        new_item["buildsInto"] = builds_into_names

        #
        for passive in new_item["passives"]:
            if "stats" in passive:
                passive["stats"] = self._preprocess_stats(passive["stats"])

        for active in new_item["active"]:
            if "stats" in active:
                active["stats"] = self._preprocess_stats(active["stats"])

        return new_item

    def _preprocess_stats(self, stats: dict) -> dict:
        stats_new = copy.deepcopy(stats)
        for k, v in list(stats_new.items()):
            for stat_key, stat_value in list(v.items()):
                if stat_value == 0:
                    stats_new[k].pop(stat_key)

            if len(stats_new[k]) == 0:
                stats_new.pop(k)
        return stats_new


def dict2str(dct: dict) -> str:
    name = dct["name"]
    champ_string = ""
    for k in dct.keys():
        v = copy.deepcopy(dct[k])
        if isinstance(v, dict):
            for k2 in v.copy().keys():
                v[f"{name} {k2}"] = v.pop(k2)
        champ_string += f"{name} {k}: {v if v  else None}\n"

    champ_string = champ_string.replace("'", "").replace('"', "")
    return champ_string
