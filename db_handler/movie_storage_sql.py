from sqlalchemy import create_engine, text

# Define the database URL as relative path
DB_URL = "sqlite:///data/moviebrain.db"

engine = create_engine(DB_URL)

# Create the movies table if it does not exist
with engine.connect() as connection:
    connection.execute(
        text("""
        CREATE TABLE IF NOT EXISTS movies (
            movie_id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT UNIQUE NOT NULL,
            year INTEGER NOT NULL,
            rating REAL NOT NULL,
            poster TEXT NOT NULL
        )
    """)
    )
    connection.commit()

# Create the user table if it does not exist
with engine.connect() as connection:
    connection.execute(
        text("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL
        )
    """)
    )
    connection.commit()

# Create the movies_user table if it does not exist
with engine.connect() as connection:
    connection.execute(
        text("""
        CREATE TABLE IF NOT EXISTS movies_users (
            movie_id INTEGER NOT NULL REFERENCES movies(movie_id),
            user_id INTEGER NOT NULL REFERENCES users(user_id)
        )
    """)
    )
    connection.commit()


def get_movies(user_id):
    """
    Retrieve all movies from the movies table that are linked through the
    movies-users cross-reference table.
    Returns a dict of dicts, where the keys of the first dict are
    the movie titles and the values are dicts containing the movie info.
    """
    with engine.connect() as connection:
        result = connection.execute(
            text("""
                SELECT title, year, rating, poster
                FROM movies AS m
                JOIN movies_users AS mu
                ON m.movie_id = mu.movie_id
                WHERE mu.user_id = :user_id
                """),
            {"user_id": user_id}
        )
        movies = result.fetchall()

    return {
        row[0]: {"year": row[1], "rating": row[2], "poster": row[3]}
        for row in movies
    }


def add_movie(user_id, title, year, rating, poster):
    """
    If it is not already in the movie table, add a new movie to the
    movie table and add a reference to user_id in movies_users table.
    """
    # check if movie already exits for different user
    with engine.connect() as connection:
        results = connection.execute(
            text("""
                 SELECT movie_id FROM movies
                 WHERE movies.title = :title
                 """),
            {"title": title},
        )
        # fetchall returns a list of tuples for every row
        # accessing list item 0 tupel item 0
        movie_id = results.scalar()

    # add movie to movies table if it has no entry yet
    if not movie_id:
        with engine.connect() as connection:
            result = connection.execute(
                text("""
                     INSERT INTO movies (
                     title, year, rating, poster
                     ) VALUES (
                     :title, :year, :rating, :poster
                     )
                     RETURNING movie_id
                    """),
                {
                    "title": title,
                    "year": year,
                    "rating": rating,
                    "poster": poster,
                }
            )
            movie_id = result.scalar()
            connection.commit()

    # add crossreference in both cases
    with engine.connect() as connection:
        connection.execute(
            text("""
                 INSERT INTO movies_users (
                 movie_id, user_id
                 ) VALUES (
                 :movie_id, :user_id
                 )
                """),
            {"movie_id": movie_id, "user_id": user_id}
        )
        connection.commit()


def delete_movie(user_id, title):
    """
    Delete movie from the cross-reference table for given user_id and
    from the database, if it is not referenced anymore.
    """
    with engine.connect() as connection:
        connection.execute(
            text("""
                 DELETE FROM movies_users AS mu
                 WHERE mu.user_id = user_id
                 AND mu.movie_id = (
                    SELECT movie_id
                    FROM movies
                    WHERE movies.title = :title
                )
                 """),
            {"title": title, "user_id": user_id}
        )
        connection.commit()

    with engine.connect() as connection:
        connection.execute(
            text("""
                 DELETE FROM movies
                 WHERE title = :title
                 AND movie_id NOT IN (
                    SELECT movie_id
                    FROM movies_users
                )
                 """),
            {"title": title}
        )
        connection.commit()


def update_movie_note(user_id, title, note):
    """Update a movies note in the database."""
    with engine.connect() as connection:
        connection.execute(
            text("""
                 UPDATE movies_users
                 SET
                   note = :note
                 WHERE user_id = :user_id
                 AND movie_id = (
                    SELECT movie_id
                    FROM movies
                    WHERE title = :title
                )
                 """),
            {"user_id": user_id, "title": title, "note": note}
        )
        connection.commit()


def get_movie_note(user_id, title):
    """Returns a movie note from the database."""
    with engine.connect() as connection:
        result = connection.execute(
            text("""
                 SELECT note
                 FROM movies_users
                 WHERE user_id = :user_id
                 AND movie_id = (
                    SELECT movie_id
                    FROM movies
                    WHERE title = :title
                )
                 """),
            {"title": title, "user_id": user_id}
        )
        connection.commit()

        return result.fetchall()[0][0]



def get_users():
    """
    Retrieve all users from the database.
    Returns a list of user names
    """
    with engine.connect() as connection:
        result = connection.execute(text("SELECT name FROM users"))
        users = result.fetchall()

    return users


def get_user_id(name):
    """
    Returns a user id for a given user name.
    """
    with engine.connect() as connection:
        result = connection.execute(
            text(f"SELECT user_id FROM users WHERE name = '{name}'")
        )
        result_list = result.fetchall()

    if result_list:
        user_id = result_list[0][0]
        return user_id
    else:
        return


def add_user(name):
    """
    Adds a new user with name name and returns its user id.
    """
    with engine.connect() as connection:
        result = connection.execute(
            text(f"INSERT INTO users (name) VALUES ('{name}')")
        )
        connection.commit()

    with engine.connect() as connection:
        result = connection.execute(
            text(f"SELECT user_id FROM users WHERE name = '{name}'")
        )
        result_list = result.fetchall()

    user_id = result_list[0][0]

    return user_id


def delete_user(name):
    """
    Deletes user with name name.
    """
    # delete movies from user
    with engine.connect() as connection:
        connection.execute(
            text("""
                DELETE FROM movies
                WHERE movie_id IN (
                    SELECT m.movie_id
                    FROM movies AS m
                    JOIN movies_user AS mu
                        ON m.movie_id = mu.movie_id
                    JOIN users AS u
                        ON u.user_id = mu.user_id
                    WHERE u.name = :name
                )
            """),
            {"name": name}
        )
        connection.commit()

    # delete cross-referencing entries from movies_users
    with engine.connect() as connection:
        connection.execute(
            text("""
                DELETE FROM movies_user
                WHERE user_id IN (
                    SELECT user_id FROM users WHERE name = :name
                )
            """),
            {"name": name}
        )
        connection.commit()

    # delete user
    with engine.connect() as connection:
        connection.execute(text(f"DELETE FROM users WHERE name = '{name}'"))
        connection.commit()
