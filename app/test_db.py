from app.database import engine

def test_connection():
    with engine.connect() as connection:
        print("Database connection successful!")

if __name__ == "__main__":
    test_connection()
