import structlog_ext_utils


def test_version_appender_custom():
    v = structlog_ext_utils.VersionAppender(number="2", key="@v")
    assert v.key == "@v"
    assert v.number == "2"


def test_version_appender():
    v = structlog_ext_utils.VersionAppender()
    event_dict = v(None, None, {})
    assert event_dict["@version"]
    assert event_dict["@version"] == "1"


def test_rename_field():
    r = structlog_ext_utils.RenameField(fields={"event": "message"})
    event_dict = r(None, None, {"event": "test message", "@version": 1})
    assert event_dict.get("event") is None


def test_application():
    a = structlog_ext_utils.Application(name="myapp", hostname="localhost")
    event_dict = a(None, None, {})
    assert event_dict["app_name"]
    assert event_dict["hostname"]


def test_application_process_info():
    a = structlog_ext_utils.Application(
        name="myapp", hostname="localhost", enable_process=True
    )
    event_dict = a(None, None, {})
    assert event_dict["process"]


def test_application_thread_info():
    a = structlog_ext_utils.Application(
        name="myapp", hostname="localhost", enable_thread=True
    )
    event_dict = a(None, None, {})
    assert event_dict["thread"]
