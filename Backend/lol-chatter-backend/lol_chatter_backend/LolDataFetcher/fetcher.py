import json
import time 
import http.client
import tqdm


class LolDataFetcher:

    def __init__(self):
        """
        Initializes the connection to 'cdn.merakianalytics.com'.
        """
        self.conn = http.client.HTTPSConnection("cdn.merakianalytics.com")

    def get_patches(self) -> list[str]:
        """
        Retrieves a list of patch names from the cdn.merakianalytics.com API.

        Returns:
            list[str]: A list of patch names.

        Raises:
            None.

        Side Effects:
            Prints the time it takes to receive the patches and the number of patches received.

        Notes:
            This function sends a GET request to the "/riot/lol/resources/patches.json" endpoint of the cdn.merakianalytics.com API.
            It then reads the response, decodes it from UTF-8, and extracts the list of patches from the JSON data.
            Finally, it prints the time it takes to receive the patches and the number of patches received.
        """
        print(f"Requesting patches from cdn.merakianalytics.com")
        t = time.time()
        self.conn.request("GET", "/riot/lol/resources/patches.json")
        response = self.conn.getresponse()
        data = response.read()
        data = json.loads(data.decode("utf-8"))["patches"]

        print(f"Received {len(data)} patches in {time.time() - t:.2f} seconds")
        patch_names = [patch["name"] for patch in data]

        return patch_names

    def get_latest_items(self) -> dict:
        """
        Retrieves the latest items from the cdn.merakianalytics.com API.

        Returns:
            dict: A dictionary containing the latest items.

        Raises:
            None.

        Side Effects:
            Prints the time it takes to receive the items and the number of items received.

        Notes:
            This function sends a GET request to the "/riot/lol/resources/latest/en-US/items.json" endpoint of the cdn.merakianalytics.com API.
            It then reads the response, decodes it from UTF-8, and extracts the latest items from the JSON data.
            Finally, it prints the time it takes to receive the items and the number of items received.
        """
        print(f"Requesting latest items from cdn.merakianalytics.com")
        t = time.time()
        endpoint = "/riot/lol/resources/latest/en-US/items.json"
        self.conn.request("GET", endpoint)
        response = self.conn.getresponse()
        data = response.read()
        data = json.loads(data.decode("utf-8"))
        print(f"Received {len(data.keys())} items in {time.time() - t:.2f} seconds")
        return data

    def get_latest_champions(self) -> dict:
        """
        Retrieves the latest champions from the cdn.merakianalytics.com API.
        Returns:
            dict: A dictionary containing the latest champions.
        """
        print(f"Requesting latest champions from cdn.merakianalytics.com")
        t = time.time()
        endpoint = "/riot/lol/resources/latest/en-US/champions.json"
        self.conn.request("GET", endpoint)
        response = self.conn.getresponse()
        data = response.read()
        data = json.loads(data.decode("utf-8"))
        print(f"Received {len(data.keys())} champions in {time.time() - t:.2f} seconds")
        return data
