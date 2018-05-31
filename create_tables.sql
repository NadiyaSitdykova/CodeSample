CREATE TABLE IF NOT EXISTS sequence (
    sequence_id INTEGER PRIMARY KEY AUTOINCREMENT,
    sequence_data TEXT NOT NULL,
    description TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS alignment (
    alignment_id INTEGER PRIMARY KEY AUTOINCREMENT,
    sequence_id INTEGER NOT NULL,
    description TEXT NOT NULL,

    FOREIGN KEY (sequence_id) REFERENCES sequence(sequence_id)
);

CREATE TABLE IF NOT EXISTS hit (
    hit_id INTEGER PRIMARY KEY AUTOINCREMENT,
    alignment_id INTEGER NOT NULL,
    percent_identity REAL,
    score INTEGER,
    e_value REAL,
    align_length INTEGER,

    FOREIGN KEY(alignment_id) REFERENCES alignment(alignment_id)
);