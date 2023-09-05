from flask import Flask
import pages


# Initialize Flask app
app = Flask(__name__)


# Main website route
app.add_url_rule("/", view_func=pages.index)