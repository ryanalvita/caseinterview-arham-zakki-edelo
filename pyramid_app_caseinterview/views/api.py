"""Sel value API"""

from pyramid.security import NO_PERMISSION_REQUIRED
from pyramid.view import view_config

from pyramid_app_caseinterview.models.depthseries import Depthseries
from pyramid_app_caseinterview.models.timeseries import Timeseries

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
        return [
            {
                "id": str(q.id),
                "datetime": q.datetime.isoformat() if q.datetime else None,
                "value": q.value,
            }
            for q in query.all()
        ]

    @view_config(
        route_name="depthseries",
        permission=NO_PERMISSION_REQUIRED,
        renderer="json",
        request_method="GET",
    )
    def depthseries_api(self):
        # ## API layer fixes for duplication problems
        # # Option 1: By keeping only the first occurrence of each depth
        # query = self.session.query(Depthseries)
        # recorded_depths = set()
        # cleaned_records = []
        # for q in query.all():
        #     if q.depth in recorded_depths:
        #         continue 
        #     recorded_depths.add(q.depth)
        #     cleaned_records.append(
        #         {
        #             "id": str(q.id),
        #             "depth": q.depth,
        #             "value": q.value
        #         }
        #     )

        # return cleaned_records
    
        # Option 2: By leveraging sqlalchemy functionalities at query time
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
            .subquery()
        )

        # Pick only the first fow
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
