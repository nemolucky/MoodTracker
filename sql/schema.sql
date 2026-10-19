-- ==========================================
-- Mood Tracker: структура базы данных SQLite
-- ==========================================

CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT
);

CREATE TABLE IF NOT EXISTS moods (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    description TEXT
);

CREATE TABLE IF NOT EXISTS factors (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    category TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS entries (
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    mood_id INTEGER,
    entry_date TEXT NOT NULL,
    score INTEGER NOT NULL,
    comment TEXT,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (mood_id) REFERENCES moods(id)
);

CREATE TABLE IF NOT EXISTS entry_factors (
    entry_id INTEGER NOT NULL,
    factor_id INTEGER NOT NULL,
    PRIMARY KEY (entry_id, factor_id),
    FOREIGN KEY (entry_id) REFERENCES entries(id) ON DELETE CASCADE,
    FOREIGN KEY (factor_id) REFERENCES factors(id) ON DELETE CASCADE
);
