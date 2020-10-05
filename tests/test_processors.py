import pytest

import structlog_ext_utils


@pytest.mark.parametrize("attribute", ["name"])
def test_timestamp(attribute):
    t = structlog_ext_utils.processors.Timestamp()
    assert hasattr(t, attribute)


@pytest.mark.parametrize("name", ["@timestamp", "@time"])
def test_custom_timestamp(name):
    t = structlog_ext_utils.processors.Timestamp(name=name)
    event_dict = t(None, None, {})
    assert event_dict[name] is not None


@pytest.mark.parametrize("attribute", ["key", "number"])
def test_version_appender(attribute):
    v = structlog_ext_utils.processors.VersionAppender()
    assert hasattr(v, attribute)


@pytest.mark.parametrize("number,key", [("2", "@v"), ("1", "@version")])
def test_custom_version_appender(number, key):
    v = structlog_ext_utils.processors.VersionAppender(number=number, key=key)
    event_dict = v(None, None, {})
    assert event_dict[key]
    assert event_dict[key] == number


def test_application():
    a = structlog_ext_utils.processors.Application(name="myapp", hostname="localhost")
    event_dict = a(None, None, {})
    assert event_dict["app_name"]
    assert event_dict["hostname"]


def test_application_process_info():
    a = structlog_ext_utils.processors.Application(
        name="myapp", hostname="localhost", enable_process=True
    )
    event_dict = a(None, None, {})
    assert event_dict["process"]


def test_application_thread_info():
    a = structlog_ext_utils.processors.Application(
        name="myapp", hostname="localhost", enable_thread=True
    )
    event_dict = a(None, None, {})
    assert event_dict["thread"]


def test_rename_field():
    r = structlog_ext_utils.processors.RenameField(fields={"event": "message"})
    event_dict = r(None, None, {"event": "test message", "@version": 1})
    assert event_dict["message"] == "test message"


def test_rename_field_that_not_exist():
    r = structlog_ext_utils.processors.RenameField(fields={"event": "message"})
    event_dict = r(None, None, {"event": "test message", "@version": 1})
    with pytest.raises(KeyError):
        event_dict["event"]
