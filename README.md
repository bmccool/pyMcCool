[![codecov](https://codecov.io/gh/bmccool/pyMcCool/graph/badge.svg?token=T7L4GHQT67)](https://codecov.io/gh/bmccool/pyMcCool)

# Installation
  - `pip install pymccool`

# Usage
- For basic, no-nonsense console and file logging:
  ```python
  from pymccool.logging import Logger
  logger = Logger(app_name="<your app name>")
  ```

- For more options, use LoggerKwargs
    ```python
    from pymccool.logging import Logger, LoggerKwargs
    logger = Logger(
            LoggerKwargs(
                app_name="test_logger_loki",
                default_level=Logger.VERBOSE,
                stream_level=Logger.VERBOSE,
                grafana_loki_endpoint="https://loki.end.point.com/loki/api/v1/push")
    )
    ```

- To use the Tracer:
  ```python
  from uuid import uuid1
  from pymccool.tracing import get_tracer, get_decorator
  from pymccool.logging import Logger, LoggerKwargs
  logger = Logger(
          LoggerKwargs(
              app_name="test_logger_loki",
              default_level=Logger.VERBOSE,
              stream_level=Logger.VERBOSE,
              grafana_loki_endpoint="https://loki.end.point.com/loki/api/v1/push")
  )
  tracer = get_tracer(service_name="test_tracer",
                      endpoint="https://otel-rec.end.point.com/v1/traces",
                      uuid=UUID)
  instrument_decorator = get_decorator(e2e_tracer)
  ```
