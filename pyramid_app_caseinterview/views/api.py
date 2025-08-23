"""Sel value API"""

from pyramid.security import NO_PERMISSION_REQUIRED
from pyramid.view import view_config
from pyramid.httpexceptions import HTTPBadRequest

from pyramid_app_caseinterview.models.depthseries import Depthseries
from pyramid_app_caseinterview.models.timeseries import Timeseries
from pyramid_app_caseinterview.filters.services import get_filtered_query

from sqlalchemy import func

from . import View


class API(View):
    """API endpoints"""

    @view_config(
        route_name="timeseries",
        permission=NO_PERMISSION_REQUIRED,
        renderer="json",
        request_method="GET",
    )
    def timeseries_api(self):
        query = self.session.query(Timeseries)

        try:
            query = get_filtered_query(Timeseries,
                                       query,
                                       self.request.GET,
                                       filter_type="timeseries_datetime_filter"
                                    )
            
        except ValueError as e:
            raise HTTPBadRequest(json_body={"Error": str(e)})

        return [
            {
                "id": str(q.id),
                "datetime": q.datetime.isoformat() if q.datetime else None,
                "value": q.value,
            }   for q in query.all()
        ]

    @view_config(
        route_name="depthseries",
        permission=NO_PERMISSION_REQUIRED,
        renderer="json",
        request_method="GET",
    )
    def depthseries_api(self):
        sub_query = (
            self.session.query(
                Depthseries.id,
                Depthseries.depth,
                Depthseries.value,
                func.row_number()
                .over(
                    partition_by=Depthseries.depth,
                )
                .label("rn")
            )
            .filter(Depthseries.value.isnot(None))
            .subquery()
        )

        # Pick only the first row
        query = self.session.query(
            sub_query.c.id,
            sub_query.c.depth,
            sub_query.c.value
        ).filter(sub_query.c.rn == 1)

        return [
            {
                "id": str(q.id),
                "depth": q.depth,
                "value": q.value
            }
                for q in query.all()
        ]
