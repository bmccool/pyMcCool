# Installation
- To install from commandline:
    `pip install git+https://github.com/bmccool/pymccool`
- To isntall via requirements.txt with e.g. specific tag v0.2.0
  `git+https://github.com/bmccool/pymccool@v0.2.0#egg=pymccool`

# Usage
- For basic, no-nonsense console and file logging:
    `from pymccool.logging import Logger`
    `logger = Logger(app_name="<your app name>")`
- For more options, use LoggerKwargs
    ```
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
  ```
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
