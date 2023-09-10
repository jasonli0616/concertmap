import requests
import requests_cache
import math
import os
from datetime import datetime
import time
import dotenv


# Initialize
requests_cache.install_cache()
dotenv.load_dotenv()


# setlist.fm API values
API_KEY = os.getenv("API_KEY")
API_URL = "https://api.setlist.fm/rest/1.0/search/setlists"
ITEMS_PER_PAGE = 20


class Setlist:
    """An object representing a setlist, with only the data required by the frontend."""

    def __init__(self, setlist_json):
        """
        Parse the data as received from the setlist.fm API.

        Data:
        latitude, longitude, artist name, date, venue name, setlist URL
        """
        self.lat = setlist_json["venue"]["city"]["coords"]["lat"]
        self.lng = setlist_json["venue"]["city"]["coords"]["long"]
        self.artist_name = setlist_json["artist"]["name"]
        self.date_string = Setlist._format_date(setlist_json["eventDate"])
        self.venue = setlist_json["venue"]["name"]
        self.url = setlist_json["url"]

    @staticmethod
    def _format_date(date_raw):
        """Convert the dd-mm-yyyy input to 'January 1 1970' format."""
        
        date_object = datetime.strptime(date_raw, "%d-%m-%Y").date()
        return date_object.strftime("%B %d, %Y")


def get_result(search_artist_name, search_year, page=1) -> list[Setlist | None]:
    """
    Send the request and parse the results.

    Return a list of Setlist object, or an empty list if no results are found.
    """

    # Send request and get response
    response = _send_api_request(search_artist_name, search_year, page)

    if response:
        response_json = response.json()

        # If successful
        if "code" not in response_json.keys():

            # Parse and return setlist data
            setlists = []

            for setlist_json in response_json["setlist"]:
                setlists.append(Setlist(setlist_json))

            # Handle more pages recursively
            total_items = response_json["total"]
            total_pages = math.ceil(total_items / ITEMS_PER_PAGE)
            if total_pages > page:
                time.sleep(0.2)
                setlists.extend(get_result(search_artist_name, search_year, page+1))

            return setlists


def _send_api_request(search_artist_name, search_year, page):
    """Send a GET request to the API."""

    # Sanitize inputs
    search_artist_name = search_artist_name.strip()
    search_year = search_year.strip()
    search_year = search_year if search_year.isdigit() else "" # ensure is int

    # Get request data
    headers = {"Accept": "application/json", "x-api-key": API_KEY}
    query = {}

    # Insert query
    query["artistName"] = search_artist_name
    query["year"] = search_year
    query["p"] = page

    # Send request
    if search_artist_name and search_year:
        return requests.get(API_URL, headers=headers, params=query)