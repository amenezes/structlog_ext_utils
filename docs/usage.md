# Usage

## Timestamp

Add `@timestamp` RFC 3339 to logging.

```python
import structlog
import structlog_ext_utils

structlog.configure(
    processors=[
        structlog_ext_utils.processors.Timestamp()
    ]
)
logger = structlog.get_logger()
```

## VersionAppender

Add `@version` to logging.

```python
import structlog
import structlog_ext_utils

structlog.configure(
    processors=[
        structlog_ext_utils.processors.VersionAppender()
    ]
)
logger = structlog.get_logger()
```

## Application

Add `app_name` and `hostname` to logging

```python
import structlog
import structlog_ext_utils

structlog.configure(
    processors=[
        structlog_ext_utils.processors.Application(name="myapp", hostname="127.0.0.1")
    ]
)
logger = structlog.get_logger()
```

## Renamefield

Rename some logging key to another one.

```python
import structlog
import structlog_ext_utils

structlog.configure(
    processors=[
        structlog_ext_utils.processors.Renamefield(fields={"event": "message"})
    ]
)
logger = structlog.get_logger()
```
