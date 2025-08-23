"""Shared fixtures."""

import os

import pytest
import transaction
import webtest
from paste.deploy.loadwsgi import appconfig

from pyramid_app_caseinterview import main
from pyramid_app_caseinterview.models import Base, get_tm_session

INI_FILE = os.path.join(os.path.dirname(__file__), "testing.ini")
SETTINGS = appconfig("config:" + INI_FILE)


@pytest.fixture(scope="session")
def app():
    app = main({}, **SETTINGS)
    print("SETUP app")

    # Drop and recreate schema
    from pyramid_app_caseinterview.scripts import initializedb
    initializedb.main([str(INI_FILE), "--drop-all"])

    # Generate fake data for testing
    from pyramid_app_caseinterview.scripts import generate_fake_data
    generate_fake_data.main([str(INI_FILE), "--clear-data"])

    yield app

    # Teardown: drop all tables at the very end of the tests
    print("TEARDOWN app")
    Base.metadata.drop_all(app.registry["session_factory"].kw["bind"])
    print("TEARDOWN app complete")


@pytest.fixture(scope="session")
def engine(app):
    yield app.registry["session_factory"].kw["bind"]


@pytest.fixture(scope="session")
def testapp(app):
    testapp = webtest.TestApp(app)
    yield testapp
    del testapp


# @pytest.fixture(scope="module")
# def session(app):
#     """Session without transaction manager"""
#     session_factory = app.registry["session_factory"]
#     session = session_factory()
#     yield session
#     session.close()


@pytest.fixture(scope="function")
def session_tm(app):
    """Transaction managed session with rollback."""
    session_factory = app.registry["session_factory"]
    session = get_tm_session(session_factory, transaction.manager)
    yield session
    session.close()


# @pytest.fixture(scope="module")
# def session_tm_module_scope(app):
#     """Transaction managed session in module scope with rolback."""
#     session_factory = app.registry["session_factory"]
#     session = get_tm_session(session_factory, transaction.manager)
#     yield session
#     session.close()
