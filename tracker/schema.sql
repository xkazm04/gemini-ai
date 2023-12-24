CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    username VARCHAR,
    hashed_password VARCHAR,
    email VARCHAR,
    role VARCHAR
);

CREATE TABLE habits (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID,
    day_type BOOLEAN[],
    active BOOLEAN DEFAULT TRUE,
    name TEXT,
    category INTEGER,
    date_from TEXT,
    date_to TEXT DEFAULT '',
    is_recurring BOOLEAN DEFAULT FALSE,
    recurrence_type TEXT DEFAULT 'Week',
    recurrence_interval INTEGER,
    specific_days BOOLEAN[], 
    type TEXT DEFAULT 'Habit', 
    volume_start INTEGER,
    volume_units TEXT,
    volume_target INTEGER,
    volume_actual INTEGER,
    subscribed INTEGER DEFAULT 0,
    ai BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE TABLE task_suggestions (
    id SERIAL PRIMARY KEY,
    name TEXT,
    habit UUID,
    removed BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (habit) REFERENCES habits(id)
);

CREATE TABLE habit_suggestions (
    id SERIAL PRIMARY KEY,
    name TEXT,
    description TEXT,
    rationale TEXT,
    category INTEGER,
    user_id UUID,
    accepted BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

ALTER TABLE habits ADD COLUMN ai BOOLEAN DEFAULT FALSE;
ALTER TABLE habit_templates ADD COLUMN ai BOOLEAN DEFAULT FALSE;
ALTER TABLE tracker_tasks ADD COLUMN completed_at TIMESTAMP DEFAULT NULL;

CREATE TABLE habit_templates (
    id SERIAL PRIMARY KEY,
    name TEXT,
    description TEXT,
    day_type BOOLEAN[],
    active BOOLEAN DEFAULT TRUE,
    category INTEGER,
    date_from TEXT,
    date_to TEXT DEFAULT '',
    is_recurring BOOLEAN DEFAULT FALSE,
    recurrence_type TEXT DEFAULT 'Week',
    recurrence_interval INTEGER,
    specific_days BOOLEAN[],
    type TEXT DEFAULT 'Habit',
    volume_start INTEGER,
    volume_units TEXT,
    volume_target INTEGER,
    volume_actual INTEGER,
    creator UUID,
    ai BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (creator) REFERENCES users(id)
);

CREATE TABLE habit_challenges (
    id SERIAL PRIMARY KEY,
    name TEXT,
    description TEXT,
    type TEXT DEFAULT 'Challenge',
    creator UUID,
    active BOOLEAN DEFAULT TRUE,
    habit_templates INTEGER[],
    FOREIGN KEY (creator) REFERENCES users(id)
);

CREATE TABLE habit_notes (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    habit_id UUID,
    note_created TEXT,
    text TEXT,
    ai BOOLEAN DEFAULT FALSE
);

CREATE TABLE tracker_countdowns (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id UUID NOT NULL,
  countdown INTEGER NOT NULL,
  elapsed INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  state VARCHAR(255)
  FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE TABLE tracker_timers (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL,
    habit_id UUID NOT NULL,
    time INTEGER
    created_at TIMESTAMP NOT NULL,
     FOREIGN KEY (user_id) REFERENCES users(id)
    FOREIGN KEY (habit_id) REFERENCES habits(id)
);

CREATE TABLE tracker_tasks (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL,
    habit_id UUID NOT NULL,
    name TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL,
    completed BOOLEAN DEFAULT FALSE,
    completed_at TIMESTAMP DEFAULT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (habit_id) REFERENCES habits(id)
);

CREATE TABLE tracker_completed (
    id SERIAL PRIMARY KEY,
    habit_id UUID NOT NULL,
    day VARCHAR(255),
    completed BOOLEAN DEFAULT TRUE,
    FOREIGN KEY (habit_id) REFERENCES habits(id)
);

