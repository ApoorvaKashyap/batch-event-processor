import json
import logging
import os
import sys
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.models import SessionDuration, Base

# Configure Logger
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Load configurations
configs = {
    "database": {
        "user": os.getenv("DB_USER", "user"),
        "password": os.getenv("DB_PASSWORD", "password"),
        "url": os.getenv("DB_URL", "postgres"),
        "db_name": os.getenv("DB_NAME", "database"),
        "db_port": os.getenv("DB_PORT", "5432"),
    },
    "variables": {
        "input_file": os.getenv(
            "INPUT_FILE", "../data/events.jsonl"
        ),  # Default input file
    },
}

# Database connection
try:
    engine = create_engine(
        f"postgresql+psycopg2://{configs['database']['user']}:{configs['database']['password']}@{configs['database']['url']}/{configs['database']['db_name']}"
    )
    Base.metadata.create_all(engine)
    logger.info("Connected to the database successfully.")
except Exception as e:
    logger.error(f"Failed to connect to the database: {e}")
    sys.exit(1)


def aggregate(file: str) -> list[dict]:
    with open(file, "r") as f:
        events = [json.loads(line) for line in f]
    df = pd.DataFrame(events)
    aggregated = (
        df.groupby("userId").sum().drop(columns=["productId", "timestamp", "eventType"])
    )
    return aggregated.reset_index().to_dict(orient="records")


def main():
    Session = sessionmaker(bind=engine)
    session = Session()
    agg = aggregate(configs["variables"]["input_file"])
    for i in agg:
        session_duration = SessionDuration(
            userId=i["userId"], sessionDuration=i["sessionDuration"]
        )
        try:
            existing_record = (
                session.query(SessionDuration)
                .filter_by(userId=i["userId"])
                .one_or_none()
            )
            if existing_record:
                existing_record.sessionDuration += i["sessionDuration"]
            else:
                session_duration = SessionDuration(
                    userId=i["userId"], sessionDuration=i["sessionDuration"]
                )
                session.add(session_duration)
            session.commit()
            logger.info(f"Inserted {i['userId']} successfully.")
        except Exception as e:
            logger.error(f"An error occurred while processing user {i['userId']}: {e}")
            session.rollback()
            sys.exit(1)
    session.close()


if __name__ == "__main__":
    main()
