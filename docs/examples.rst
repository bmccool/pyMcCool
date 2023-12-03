Examples
===========

Example usage

.. testcode:: pymccool

    from pymccool.logging import Logger
    test_string = "hello world"
    logger = Logger(app_name="test_logger")
    logger.info(test_string)
    
Output:

.. testoutput:: pymccool
    :options: +ELLIPSIS

    ...
