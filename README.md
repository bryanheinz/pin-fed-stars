# Pin Fed Stars
This project pulls your [Feedbin](https://feedbin.com) stars and bookmarks them in [Pinboard](https://pinboard.in).

## Setup
Update `code/controller.py` with your Feedbin email, your Feedbin password base64 encoded, and your Pinboard API token base64 encoded (username:key).

Run `pip install -r requirements.txt` to install non-standard libraries (Beautiful Soup, Requests.)

Tested in Python 3.8. Requires at least Python 3.6.

## Usage
Run `python3 controller.py`
