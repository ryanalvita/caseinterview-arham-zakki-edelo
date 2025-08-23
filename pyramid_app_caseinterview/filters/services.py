from sqlalchemy.orm import Query

from typing import Dict, Type
from pyramid_app_caseinterview.filters.timeseries import timeseries_datetime_filter

def get_filtered_query(
    model: Type,    
    query: Query ,
    filters: Dict[str, str],
    filter_type: str = "timeseries_datetime_filter"
    ):
    """
    Modular filter dispatcher for any model.
    """
    filter_collections = {
        "timeseries_datetime_filter": timeseries_datetime_filter,
        # Place other filters here
    }

    filter_func = filter_collections.get(filter_type)
    if not filter_func:
        raise KeyError(f"Invalid filter type '{filter_type}'.")

    return filter_func(model, query, filters)