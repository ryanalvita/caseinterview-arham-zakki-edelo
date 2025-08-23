"""
Generate fake realistic data into database.

In this example we simulated cone tip resistance for depthseries
and wind speed for the timeseries.

Usage:
  pyramid_app_caseinterview_generate_fake_data <inifile> [options]
  pyramid_app_caseinterview_generate_fake_data --help

Options:
  -h --help                 Show this screen.
  -o --options=LIST         Comma-separated list of key=value pairs overwriting default setting in initfile.
  --clear-data              Clear existing timeseries and depthseries data before generating new data.
  --num-timeseries=NUM      Number of timeseries records to generate [default: 120].
  --num-depthseries=NUM     Number of depthseries records to generate [default: 50].
"""

import logging
import os 
from datetime import datetime, timedelta
from uuid import uuid4

import numpy as np
import transaction
from docopt import docopt
from pyramid.paster import get_appsettings, setup_logging

from pyramid_app_caseinterview import get_config
from pyramid_app_caseinterview.models.depthseries import Depthseries
from pyramid_app_caseinterview.models.timeseries import Timeseries
from pyramid_app_caseinterview.models import (
    get_engine,
    get_session_factory,
    get_tm_session)

logger = logging.getLogger(__name__)

ALEMBIC_INI = os.path.join(os.path.dirname(__file__), "..", "..", "alembic.ini")

def generate_timeseries_data(num_records: int):
    """Generate fake realistic wind speed timeseries data.
    
    Hourly wind speed data (0–25 m/s, mean 10 m/s, std 5 m/s)
    starting from `num_records` hours before the current time, progressing forward.
    
    """
    now_time = datetime.now() - timedelta(hours=num_records)
    records = []
    for i in range(num_records):
        # Generate hourly timestamps
        timestamp = now_time + timedelta(hours=i)
        # Simulate wind speed (m/s) with realistic variation (0 to 25 m/s)
        wind_speed = np.clip(np.random.normal(10,5), 0, 25)
        record = Timeseries(
            id=uuid4(),
            datetime=timestamp,
            value=round(wind_speed, 2)                  
        )

        records.append(record)
    
    return records


def generate_depthseries_data(num_records:int):
    """Generate fake cone tip resistance depthseries data.
    
    Cone tip resistance (qc, 2–30 MPa, mean 15 MPa, std 5 MPa)
    for depths evenly spaced from 0 to 50 meters
    """
    records = []
    for i in range(num_records):
        # Depth range from 0 to 50 meters
        depth = i * 50 / (num_records - 1) if num_records > 1 else 0
        # Simulate cone tip resistance (qc, MPa) with realistic variation (2 to 30 Mpa)
        qc = np.clip(np.random.normal(15,5), 2, 30)
        record = Depthseries(
            id=uuid4(),
            depth=round(depth, 2),
            value=round(qc, 2)
        )
        records.append(record)
    
    return records


def main(argv=None):
    """Generate fake data for timeseries and depthseries tables."""
    args = docopt(__doc__, argv=argv)
    setup_logging(args["<inifile>"])
    settings = get_appsettings(args["<inifile>"])
    if args["--options"]:
        settings.update(
            {
                k.strip(): v.strip()
                for kv in args["--options"].split(",")
                for k, v in kv.split("=")
            }
        )
    
    config = get_config(settings=settings).get_settings()
    engine = get_engine(config)
    
    session_factory = get_session_factory(engine)

    try:
        num_timeseries = int(args["--num-timeseries"])
        num_depthseries = int(args["--num-depthseries"])

        if num_timeseries <=0 and num_depthseries <=0:
            logger.error("Number of records must be positive")
            raise ValueError("Number of records must be positive")
    except ValueError as e:
        logger.error(f"Invalid input: {e}")
                         

    with transaction.manager:
        session = get_tm_session(session_factory, transaction.manager)
        if args["--clear-data"]:
            logger.warning("Clearing existing timeseries and depthseries data!")
            session.query(Timeseries).delete()
            session.query(Depthseries).delete()
        
        # Generate and insert timeseries data
        logger.info(f"Generating {num_timeseries} timeseries records...")
        timeseries_records = generate_timeseries_data(num_timeseries)
        session.add_all(timeseries_records)

        # Generate and insert depthseries data
        logger.info(f"Generating {num_depthseries} depthseries records...")
        depthseries_records = generate_depthseries_data(num_depthseries)
        session.add_all(depthseries_records)

        logger.info("Committing data to database...")

    logger.info("Finished generating fake data.")


if __name__ == "__main__":
    main()