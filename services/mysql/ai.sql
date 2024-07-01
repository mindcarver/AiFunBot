USE ai_fun_bot;
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY, 
    telegram_id VARCHAR(100),
    invite_code VARCHAR(10),
    create_at timestamp DEFAULT CURRENT_TIMESTAMP,
    update_at timestamp DEFAULT CURRENT_TIMESTAMP,
    delete_at timestamp DEFAULT NULL
);




