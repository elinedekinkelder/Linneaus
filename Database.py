import sqlite3

class Database:
    def __init__(self, db_name='feedback.db'):
        self.db_name = db_name
        self._init_db()

    def _init_db(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS feedback_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                use_case TEXT,
                user_prompt TEXT,
                model_A TEXT,
                model_b TEXT,
                model_A_response TEXT,
                model_b_response TEXT,
                feedback TEXT,
                feedback_motivation TEXT
            )
        ''')
        conn.commit()
        conn.close()

    def log_feedback(self, use_case, user_prompt, model_a, model_b, model_a_response, model_b_response, feedback, feedback_motivation):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO feedback_log (use_case, user_prompt, model_a, model_b, model_a_response, model_b_response, feedback, feedback_motivation)
            VALUES (?, ?, ?, ?, ?, ?,?,?)
        ''', (use_case, user_prompt, model_a, model_b, model_a_response, model_b_response, feedback, feedback_motivation))
        conn.commit()
        conn.close()
