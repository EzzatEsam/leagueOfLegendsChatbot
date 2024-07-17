import os
import pickle
from .fetcher import LolDataFetcher
from .post_processor import DataPostProcessor


def data_exists(filename):
    return os.path.exists(filename)


def save_data_to_disk(data, filename):
    with open(filename, "wb") as file:
        pickle.dump(data, file)


def load_data_from_disk(filename):
    with open(filename, "rb") as file:
        return pickle.load(file)


# Initialize classes
fetcher = LolDataFetcher()
preProcessor = DataPostProcessor()

# File names
patches_file = "patches.pkl"
items_file = "items.pkl"
champions_file = "champions.pkl"

# Fetch patches
patches = fetcher.get_patches()
latest_patch = patches[-1]

# Check if data exists and if the latest patch matches
if (
    data_exists(patches_file)
    and data_exists(items_file)
    and data_exists(champions_file)
):
    saved_patches = load_data_from_disk(patches_file)
    if saved_patches[-1] == latest_patch:
        # Load data from disk
        items_processed = load_data_from_disk(items_file)
        champions_processed = load_data_from_disk(champions_file)
    else:
        # Update data and save to disk
        items_raw = fetcher.get_latest_items()
        champions_raw = fetcher.get_latest_champions()
        items_processed = preProcessor.get_items_list(items_raw)
        champions_processed = preProcessor.get_champions_list(champions_raw)

        # Save new data to disk
        save_data_to_disk(patches, patches_file)
        save_data_to_disk(items_processed, items_file)
        save_data_to_disk(champions_processed, champions_file)
else:
    # Fetch new data and save to disk
    items_raw = fetcher.get_latest_items()
    champions_raw = fetcher.get_latest_champions()
    items_processed = preProcessor.get_items_list(items_raw)
    champions_processed = preProcessor.get_champions_list(champions_raw)

    # Save data to disk
    save_data_to_disk(patches, patches_file)
    save_data_to_disk(items_processed, items_file)
    save_data_to_disk(champions_processed, champions_file)
