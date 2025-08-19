import pandas as pd
import json
from configparser import ConfigParser
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.models import SessionDuration, Base
import logging

# Load configurations
configs = ConfigParser()
configs.read(".configs/config.ini")

# Database connection
engine = create_engine(f"postgresql+psycopg2://{configs['database']['user']}:{configs['database']['password']}@{configs['database']['url']}/{configs['database']['db_name']}")
Base.metadata.create_all(engine)



# Configure Logger
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def aggregate(file:str) -> list[dict]:
    with open(file, 'r') as f:
        events = [json.loads(line) for line in f]
    df = pd.DataFrame(events)
    aggregated = df.groupby('userId').sum().drop(columns=['productId', 'timestamp', 'eventType'])
    return aggregated.reset_index().to_dict(orient='records')

def main():
    Session = sessionmaker(bind=engine)
    session = Session()
    agg = aggregate(configs["variables"]["input_file"])
    for i in agg:
        session_duration = SessionDuration(userId=i['userId'], sessionDuration=i['sessionDuration'])
        try:
            existing_record = session.query(SessionDuration).filter_by(userId=i['userId']).one_or_none()
            if existing_record:
                existing_record.sessionDuration += i['sessionDuration']
            else:
                session_duration = SessionDuration(userId=i['userId'], sessionDuration=i['sessionDuration'])
                session.add(session_duration)
        
            session.commit()
        except Exception as e: 
            logger.error(f"An error occurred while processing user {i['userId']}: {e}")
            session.rollback()
    session.close()


if __name__ == "__main__":
    main()
