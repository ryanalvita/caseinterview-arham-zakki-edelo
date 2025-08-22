"""
Ingest Depthseries data form CSV file into database with integrity and clean checks.

Usage:
  pyramid_app_caseinterview_ingest_depthseries <inifile> --csv-file=<filename> [options]
  pyramid_app_caseinterview_ingest_depthseries --help

Options:
  -h --help                Show this screen.
  -o --options=LIST         Comma-separated list of key=value pairs overwriting default setting in initfile.
  --csv-file=<filename>    Name of CSV file located in `datadirectory` (from .ini).
  --clear-data             Clear existing depthseries data before ingestion.

"""

import csv
import logging
import os
from uuid import uuid4

import transaction
from docopt import docopt
from pyramid.paster import get_appsettings, setup_logging

from pyramid_app_caseinterview import get_config
from pyramid_app_caseinterview.models import (
    depthseries,
    get_engine,
    get_session_factory,
    get_tm_session,
)

logger = logging.getLogger(__name__)

def validate_and_clean(records):
    """Validate and clean depthseries records data."""
    recorded_depths = set()    
    cleaned = []

    for row in records:
        depth = row["depth"]
        value = row["value"]

        if depth in recorded_depths:
            logger.warning(f"Duplicate depth {depth} found, skipping row {row}")
            continue

        recorded_depths.add(depth)
        cleaned.append(
            depthseries.Depthseries(
                id = uuid4(),
                depth=depth,
                value = value,
            )
        )
    
    return cleaned


def load_csv(file_path):
    """Read depthseries data from CSV input file"""
    records = []
    with open(file_path, newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            try:
                depth = float(row["depth"])
                value = float(row["value"])
                records.append({
                    "depth": depth,
                    "value": value
                })
            except (KeyError, ValueError) as e:
                logger.warning(f"Skipping invalid row {row}: {e}")

    return records


def main(argv=None):
    """Ingest depthseries data from CSV file"""
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

    datadir = settings.get("datadirectory", "data")
    csv_file = args["--csv-file"]
    csv_path = os.path.join(datadir, csv_file)

    if not os.path.exists(csv_path):
        logger.error(f"CSV file {csv_path} does not exist.")
        return 1
    
    with transaction.manager:
        session = get_tm_session(session_factory, transaction.manager)
        if args["--clear-data"]:
            logger.warning("Clearing existing depthseries data!")
            session.query(depthseries.Depthseries).delete()

        # Load CSV
        logger.info(f"Loading csv file {csv_path}...")
        raw_records = load_csv(csv_path)

        # validate and clean records
        cleaned_records = validate_and_clean(raw_records)

        logger.info(f"Inserting {len(cleaned_records)} depthseries records...")
        session.add_all(cleaned_records)

    logger.info("CSV ingestion complete.")
    return 0


if __name__ == "__main__":
    main()



