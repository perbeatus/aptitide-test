CREATE TABLE movies(
    id SERIAL,
    movieId BIGINT,
    title VARCHAR(255),
    genres VARCHAR(500),
 
    PRIMARY KEY(id)
);
COPY movies(movieId, title, genres) FROM '/fixture-data/db-fixture/movies.csv' DELIMITER ',' CSV HEADER;

CREATE TABLE links(
    id SERIAL,
    movieId BIGINT,
    imdbId BIGINT,
    tmdbId BIGINT,
 
    PRIMARY KEY(id)
);
COPY links(movieId, imdbId, tmdbId) FROM '/fixture-data/db-fixture/links.csv' DELIMITER ',' CSV HEADER;

CREATE TABLE ratings(
    id SERIAL,
    userId BIGINT,
    movieId BIGINT,
    rating FLOAT,
    "timestamp" BIGINT,
 
    PRIMARY KEY(id)
);
COPY ratings(userId, movieId, rating, "timestamp") FROM '/fixture-data/db-fixture/ratings.csv' DELIMITER ',' CSV HEADER;

CREATE TABLE tags(
    id SERIAL,
    userId BIGINT,
    movieId BIGINT,
    tag VARCHAR(500),
    "timestamp" BIGINT,

    PRIMARY KEY(id)
);
COPY tags(userId, movieId, tag, "timestamp") FROM '/fixture-data/db-fixture/tags.csv' DELIMITER ',' CSV HEADER;