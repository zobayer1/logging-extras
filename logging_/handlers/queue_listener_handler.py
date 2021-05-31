# -*- coding: utf-8 -*-
import atexit
from logging import LogRecord
from logging.config import ConvertingDict, ConvertingList, valid_ident
from logging.handlers import QueueHandler, QueueListener
from typing import Any


class QueueListenerHandler(QueueHandler):
    """QueueListenerHandler class for managing a queue listener with configured handlers.

    This class sets up a queue listener logger handler with customizable configurations. Inspired by Rob Blackbourn's
    article: ``https://rob-blackbourn.medium.com/how-to-use-python-logging-queuehandler-with-dictconfig-1e8b1284e27a``

    Example configuration::

        # logging.yaml
        version: 1
        objects:
          queue:
            class: queue.Queue
            maxsize: -1
        formatters:
          simple:
            format: '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        handlers:
          console:
            class: logging.StreamHandler
            formatter: simple
            stream: ext://sys.stdout
          file_handler:
            class: logging.FileHandler
            filename: test_logger.log
            formatter: simple
          queue_handler:
            class: logging_.handlers.QueueListenerHandler
            handlers:
            - cfg://handlers.console
            - cfg://handlers.file_handler
           queue: cfg://objects.queue

    """

    def __init__(self, queue: Any, handlers: Any, respect_handler_level: bool = True, auto_run: bool = True):
        """Instantiates QueueListenerHandler object.

        A simple ``QueueHandler`` subclass implementation utilizing ``QueueListener`` for configured handlers. This is
        helpful for detaching ypur logger handlers from the main processing threads, which reduces the risk of getting
        blocked, for example, when using slower handlers such as smtp, file, or socket handlers.

        Args:
            queue: A queue instance passed from configuration.
            handlers: A list of handlers passed from configuration.
            respect_handler_level: Flag for overriding logging levels specified in handlers. Default: True.
            auto_run: Flag for starting the queue listener automatically. Default: True.
        """

        _queue = self._resolve_queue(queue)
        _handlers = self._resolve_handlers(handlers)
        super().__init__(_queue)
        self._listener = QueueListener(_queue, *_handlers, respect_handler_level=respect_handler_level)
        if auto_run:
            self._listener.start()
            atexit.register(self._listener.stop)

    def emit(self, record: LogRecord):
        """Processes the specified logging record.

        This method is implemented to avoid raising a NotImplementedError from the subclass.

        Args:
            record: A logging.LogRecord object.
        """

        super().emit(record)

    @staticmethod
    def _resolve_queue(queue: Any) -> Any:
        """Resolves and evaluates queue object.

        Args:
            queue: queue object passed via logging.config.dictConfig.

        Returns:
            Resolved queue object.
        """

        if not isinstance(queue, ConvertingDict):
            return queue
        if "__resolved_value__" in queue:
            return queue["__resolved_value__"]
        cname = queue.pop("class")
        klass = queue.configurator.resolve(cname)
        props = queue.pop(".", None)
        kwargs = {k: queue[k] for k in queue if valid_ident(k)}
        result = klass(**kwargs)
        if props:
            for name, value in props.items():
                setattr(result, name, value)
        queue["__resolved_value__"] = result
        return result

    @staticmethod
    def _resolve_handlers(handlers: Any) -> Any:
        """Resolves and evaluates handler objects.

        Args:
            handlers: handler list passed via logging.config.dictConfig.

        Returns:
            Resolved handler list.
        """

        if not isinstance(handlers, ConvertingList):
            return handlers
        return [handlers[i] for i in range(len(handlers))]
