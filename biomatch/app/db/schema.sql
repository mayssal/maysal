CREATE TABLE IF NOT EXISTS persons (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    full_name TEXT,
    email TEXT,
    phone TEXT,
    address TEXT,
    notes TEXT,
    face_embedding TEXT,
    voice_embedding TEXT,
    created_at TEXT,
    updated_at TEXT
);