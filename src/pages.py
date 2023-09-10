from flask import render_template, request
import setlistapi

def index():
    """Main website route."""

    # Initialize search variables
    searched = False
    setlists = []

    # Get form data, if available
    search_artist_name = request.args.get("artistname")
    search_year = request.args.get("year")

    if search_artist_name and search_year:
        # Send request
        setlists = setlistapi.sort_setlists_by_date(setlistapi.get_result(search_artist_name, search_year))
        searched = True
    else:
        # Change empty variables from None to blank string
        search_artist_name = ""
        search_year = ""

    return render_template("index.html", search_artist_name=search_artist_name, search_year=search_year, setlists=setlists, searched=searched)
    