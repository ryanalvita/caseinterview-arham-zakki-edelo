from sqlalchemy.orm import Query
from typing import Dict, Type


def depthseries_depth_filter(model: Type, query: Query, filters: Dict[str, str]):
    """Depthseries filter by start_depth and end_depth from filters dict."""
    start_depth = filters.get("start_depth")
    end_depth = filters.get("end_depth")

    if start_depth:
        try:
            start_depth = float(start_depth)
            query = query.filter(model.depth >= start_depth)
        except ValueError:
            raise ValueError(f"Invalid start_depth {start_depth}.")

    if end_depth:
        try:
            end_depth = float(end_depth)
            query = query.filter(model.depth <= end_depth)
        except ValueError:
            raise ValueError(f"Invalid end_depth format {end_depth}.")

    return query
