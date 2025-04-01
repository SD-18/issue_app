from .database import Base, engine
from .models import user, issue, attachments  # Ensure all models are imported for table creation
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

def create_tables():
    """
    Function to create all database tables defined in the models.
    """
    try:
        logging.info("✅ Starting the process of creating database tables...")
        Base.metadata.create_all(bind=engine)  # Create tables in the database
        logging.info("✅ All tables created successfully!")
    except Exception as e:
        logging.error(f"❌ Error while creating tables: {e}")
        raise RuntimeError("Table creation failed. Check the logs for more details.")

if __name__ == "__main__":
    create_tables()