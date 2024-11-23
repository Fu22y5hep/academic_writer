from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists

DATABASE_URL = "postgresql://rossshepstone@localhost/academic_writing"

def test_connection():
    try:
        engine = create_engine(DATABASE_URL)
        if database_exists(engine.url):
            print("✅ Successfully connected to the database!")
            return True
        else:
            print("❌ Database does not exist!")
            return False
    except Exception as e:
        print(f"❌ Failed to connect to the database: {str(e)}")
        return False

if __name__ == "__main__":
    test_connection()
