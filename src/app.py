from flask import Flask, render_template, request
import requests
import requests_cache
import os
import math
import dotenv


# Initialization
app = Flask(__name__)
requests_cache.install_cache()
dotenv.load_dotenv()


# setlist.fm API values
API_KEY = os.getenv("API_KEY")
API_URL = "https://api.setlist.fm/rest/1.0/search/setlists"
ITEMS_PER_PAGE = 20


# Main website route
@app.route("/", methods=["GET", "POST"])
def index():

    setlists = []

    if request.method == "POST":

        # Get form data
        search_artist_name = request.form["artistname"]
        search_year = request.form["year"]
        
        # Send request
        setlists = get_result(search_artist_name, search_year)

    return render_template("index.html", setlists=setlists)
    

# Setlist object
class Setlist:
    def __init__(self, setlist_json):
        self.lat = setlist_json["venue"]["city"]["coords"]["lat"]
        self.lng = setlist_json["venue"]["city"]["coords"]["long"]
        self.artistName = setlist_json["artist"]["name"]
        self.dateRaw = setlist_json["eventDate"]
        self.venue = setlist_json["venue"]["name"]
        self.url = setlist_json["url"]


# Get response and parse
def get_result(search_artist_name, search_year, page=1) -> list[Setlist | None]:

    # Send request and get response
    response = send_api_request(search_artist_name, search_year, page)

    if response:
        response_json = response.json()

        # If successful
        if "code" not in response_json.keys():

            # Parse and return setlist data
            setlists = []

            for setlist_json in response_json["setlist"]:
                setlists.append(Setlist(setlist_json))

            # Handle more pages
            total_items = response_json["total"]
            total_pages = math.ceil(total_items / ITEMS_PER_PAGE)
            if total_pages > page:
                setlists.extend(get_result(search_artist_name, search_year, page+1))

            return setlists


# Send request to API
def send_api_request(search_artist_name, search_year, page):

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