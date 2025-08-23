from datetime import datetime
from sqlalchemy.orm import Query
from typing import Dict, Type


def timeseries_datetime_filter(model: Type, query: Query, filters: Dict[str, str]):
    """Datetime filter by start_date and end_date from filters dict."""
    start_date = filters.get("start_date")
    end_date = filters.get("end_date")

    if start_date:
        try:
            dt_start = datetime.fromisoformat(start_date)
            query = query.filter(model.datetime >= dt_start)
        except ValueError:
            raise ValueError(f"Invalid start_date format {start_date}. "
                             f"Expected ISO format YYYY-MM-DDThh:mm:ss for full datetime "
                             f"or YYYY-MM-DD for date resolution only.")

    if end_date:
        try:
            dt_end = datetime.fromisoformat(end_date)
            query = query.filter(model.datetime <= dt_end)
        except ValueError:
            raise ValueError(f"Invalid end_date format {end_date}. "
                             f"Expected ISO format YYYY-MM-DDThh:mm:ss for full datetime "
                             f"or YYYY-MM-DD for date resolution only.")

    return query
