import os
import psycopg2
from psycopg2.extras import RealDictCursor
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Fetch DB credentials
USER = os.getenv("SUPABASE_USER")
PASSWORD = os.getenv("SUPABASE_PASSWORD")
HOST = os.getenv("SUPABASE_HOST")
PORT = os.getenv("SUPABASE_PORT")
DBNAME = os.getenv("SUPABASE_DB")

# Track if table has been ensured
_table_checked = False


def get_db_connection():
    try:
        conn = psycopg2.connect(
            user=USER,
            password=PASSWORD,
            host=HOST,
            port=PORT,
            dbname=DBNAME,
            sslmode="require"
        )
        conn.set_client_encoding('UTF8')
        return conn
    except Exception as e:
        print(f"❌ DB connection error: {e}")
        raise


def ensure_table_exists(conn):
    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS predictions (
                id SERIAL PRIMARY KEY,
                timestamp TIMESTAMP,
                predicted INTEGER,
                confidence FLOAT,
                true_label INTEGER
            );
        """)
        conn.commit()


def log_prediction(predicted: int, confidence: float, true_label: int = None):
    global _table_checked
    conn = get_db_connection()

    if not _table_checked:
        ensure_table_exists(conn)
        _table_checked = True

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with conn:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO predictions (timestamp, predicted, confidence, true_label)
                VALUES (%s, %s, %s, %s)
            """, (timestamp, predicted, confidence, true_label))
            conn.commit()
    conn.close()


def get_recent_predictions(limit=10):
    conn = get_db_connection()
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("""
                SELECT timestamp, predicted, confidence, true_label
                FROM predictions
                WHERE true_label IS NOT NULL
                ORDER BY id DESC
                LIMIT %s;
            """, (limit,))
            return cur.fetchall()
    finally:
        conn.close()
