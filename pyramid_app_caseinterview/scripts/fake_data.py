import random
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from pyramid_app_caseinterview.models.depthseries import Depthseries, Base  # Adjust if in same file

# Setup DB engine (update with your real credentials)
engine = create_engine("postgresql://postgres:abc@caseinterview_database:5432/caseinterview")

# Create tables (if not already created)
Base.metadata.create_all(engine)

# Insert fake rows
with Session(engine) as session:
    fake_depthseries = [
        Depthseries(depth=10.0, value=100.5),
        Depthseries(depth=20.5, value=95.3),
        Depthseries(depth=30.1, value=None),
        Depthseries(depth=15.2, value=105.0),
        Depthseries(depth=40.0, value=87.7),
    ]

    session.add_all(fake_depthseries)
    session.commit()
