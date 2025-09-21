CREATE TABLE movies(
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    title VARCHAR(50),
    description TEXT,
    poster_image_url VARCHAR(250),
    duration_minutes INT,
    created_time TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE genres (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(100) UNIQUE NOT NULL
);

-- Association/Pivot table to link movies and genres
CREATE TABLE movie_genres (
    movie_id UUID NOT NULL REFERENCES movies(id) ON DELETE CASCADE,
    genre_id UUID NOT NULL REFERENCES genres(id) ON DELETE CASCADE,
    PRIMARY KEY (movie_id, genre_id)
);
