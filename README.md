# The MovieBrain 

A simple movie database project with Open Movie Database API access.
CLI controlled but with a live browser view.

Install by executing `git clone https://github.com/nesmomik/MovieBrain.git` in a terminal.

Change into the directory with `cd MovieBrain`.

Install dependencies:

- with `pip`:
  Create a virtual environment with `python -m venv .venv`.
  Activate the virtual environment with `source .venv/bin/activate`.
  Install the the dependencies with `pip install -r requirements.txt`.

- with `uv`:
  Initialize `uv init`
  Add dependencies `uv add -r requirements.txt`

Get a free API key from [OMDb API](https://www.omdbapi.com/).

Create an `.env` file in the project directory with `OMDB_API_KEY=YOUR_API_KEY`.

Start the program with `python moviebrain.py` or in case of using uv with `uv run moviebrain.py`.

