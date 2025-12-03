import threading
import logging
from livereload import Server


HTML_TEMPLATE_FILE = "html_display/template.html"
HTML_OUTPUT_FILENAME = "html_display/index.html"
CSS_FILENAME = "html_display/style.css"
HTML_LOCAL_URL = "http://localhost:8080/html_display/index.html"


def start_livereload():
    """configures and starts the http livereload"""
    # disable logging, so it does not clutter the cli
    logging.disable(logging.CRITICAL)

    local_server = Server()
    local_server.watch(HTML_OUTPUT_FILENAME)
    local_server.watch(CSS_FILENAME)
    # local address http://localhost:8080
    local_server.serve(root=".", port=8080)


# Run livereload in a separate thread in parallel
thread = threading.Thread(target=start_livereload, daemon=True)
thread.start()


def show_link():
    print(
        "\033]8;;"
        + HTML_LOCAL_URL
        + "\033\\"
        + "  Ctrl+Click here for the browser view."
        + "\033]8;;\033\\\n"
    )


def read_template(file_path):
    """Returns the content of the template file as string"""
    with open(file_path, "r") as handle:
        return handle.read()


def format_data(movie_dict):
    """Aggregates and returns a string from the input data"""

    data_string = ""

    if movie_dict:
        for movie, info in movie_dict.items():
            data_string += serialize_movie(movie, info)
    else:
        data_string += serialize_no_movie()

    return data_string


def generate_html_file(movie_dict):
    write_html(HTML_OUTPUT_FILENAME, create_html_string(movie_dict))


def create_html_string(movie_dict):
    """
    Reads the template file and replaces the placeholder
    text with the generated html code
    """
    return read_template(HTML_TEMPLATE_FILE).replace(
        "__REPLACE_MOVIES_INFO__", format_data(movie_dict)
    )


def write_html(file_path, html_string):
    """Returns the content of the template file as string"""
    with open(file_path, "w") as handle:
        handle.write(html_string)


def serialize_no_movie():
    data_string = ""
    data_string += '<li style="max-width=360px">\n'
    data_string += '<div class="movie">\n'
    data_string += '<img class="movie-poster" src="no_results.jpg"/>\n'
    data_string += '<div class="movie-title">Sorry, no movies yet.</div>\n'
    data_string += '<div class="movie-year">____</div>\n'
    data_string += "</div>\n"
    data_string += "</li>"

    return data_string


def serialize_movie(movie, info):
    """wraps data retrieved from a single object in html code"""
    data_string = ""
    # add html and data to output string
    data_string += "<li>\n"
    data_string += '<div class="movie">\n'
    data_string += '<img class="movie-poster"\n'
    data_string += 'src="' + info["poster"] + '"/>\n'
    data_string += '<div class="movie-title">' + movie + "</div>"
    data_string += (
        '<div class="movie-info">'
        + str(info["year"])
        + " / "
        + str(info["rating"])
        + "</div>"
    )
    data_string += "</div>\n" + "</li>"

    return data_string
