import psycopg2
from datetime import datetime

# Database connection string - use the same one from your app.py
DATABASE_URL = 'postgresql://adwait_portfolio_user:VD6UHceZqb63iGWI7ItyLkn82IRzcafi@dpg-d02p84qdbo4c73f1lpvg-a/adwait_portfolio'

def test_database_insert():
    try:
        print("Connecting to database...")
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        cursor = conn.cursor()
        
        # Insert a test message
        name = 'Test User'
        email = 'test@example.com'
        message = 'This is a test message inserted directly by the script.'
        timestamp = datetime.now()
        
        print("Inserting test message...")
        cursor.execute(
            "INSERT INTO contact_messages (name, email, message, timestamp) VALUES (%s, %s, %s, %s) RETURNING id;",
            (name, email, message, timestamp)
        )
        
        # Get the ID of the inserted row
        inserted_id = cursor.fetchone()[0]
        print(f"Test message inserted with ID: {inserted_id}")
        
        # Commit the transaction
        conn.commit()
        
        # Verify the insertion
        print("Verifying insertion...")
        cursor.execute("SELECT * FROM contact_messages WHERE id = %s;", (inserted_id,))
        verification = cursor.fetchone()
        print(f"Verification of inserted data: {verification}")
        
        # Count total messages
        cursor.execute("SELECT COUNT(*) FROM contact_messages;")
        count = cursor.fetchone()[0]
        print(f"Total messages in database: {count}")
        
        conn.close()
        print("Database test completed successfully!")
        return True
    except Exception as e:
        print(f"Error during database test: {e}")
        return False

if __name__ == "__main__":
    test_database_insert()