# test_db.py
import os
import psycopg2

try:
    conn = psycopg2.connect(
        host=os.getenv('SUPABASE_HOST'),
        dbname=os.getenv('SUPABASE_DB'),
        user=os.getenv('SUPABASE_USER'),
        password=os.getenv('SUPABASE_PASSWORD'),
        port=os.getenv('SUPABASE_PORT'),
        sslmode='require'
    )
    with conn.cursor() as cur:
        cur.execute('SELECT NOW();')
        print('✅ Supabase connection successful:', cur.fetchone())
    conn.close()
except Exception as e:
    print('❌ Supabase DB connection failed:', e)
    raise
