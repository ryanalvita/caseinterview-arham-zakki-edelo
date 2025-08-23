import csv 
from io import StringIO
from pyramid.response import Response

from sqlalchemy.orm import Query

def write_to_csv(query: Query, header:list, output_name:str = "download.csv"):
    """Write query rows to CSV file and return as HTT response"""
    output = StringIO()
    writer = csv.writer(output)
    writer.writerow(header)

    if not query.all():
        return Response(
            "\n".join([",".join(header)]),
            content_type="text/csv",
            content_disposition=f"attachment; filename={output_name}"
        )
    
    for row in query.all():
        writer.writerow([getattr(row, col) for col in header])
    
    # Prepare HTTP response object
    response = Response(body=output.getvalue())
    response.content_type = "text/csv"
    response.headers["content-deposition"] = f"attachment; filename={output_name}"
    return response
