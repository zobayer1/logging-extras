# -*- coding: utf-8 -*-
import atexit
import copy
import logging.config
from logging import Handler, LogRecord
from logging.handlers import QueueListener
from typing import Any


class QueueListenerHandler(Handler):
    """QueueListenerHandler class for managing a queue listener with configured handlers.

    This class sets up a queue listener logger handler with customizable configurations. Inspired by Rob Blackbourn's
    article: ``https://rob-blackbourn.medium.com/how-to-use-python-logging-queuehandler-with-dictconfig-1e8b1284e27a``.

    It intentionally subclasses ``logging.Handler`` and re-implements the small ``QueueHandler`` behaviour
    (``prepare``/``enqueue``/``emit``) instead of subclassing ``logging.handlers.QueueHandler``. Since Python 3.12,
    ``logging.config.dictConfig`` special-cases every ``QueueHandler`` subclass and takes over its construction
    (creating the ``QueueListener`` itself and rejecting the ``class``-style queue specifier used here). Subclassing
    ``Handler`` directly avoids that intercept, so the same YAML configuration works identically on Python 3.8-3.15.

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

        A simple ``QueueHandler``-like implementation utilizing ``QueueListener`` for configured handlers. This is
        helpful for detaching your logger handlers from the main processing threads, which reduces the risk of getting
        blocked, for example, when using slower handlers such as smtp, file, or socket handlers.

        Args:
            queue: A queue instance passed from configuration.
            handlers: A list of handlers passed from configuration.
            respect_handler_level: Flag for overriding logging levels specified in handlers. Default: True.
            auto_run: Flag for starting the queue listener automatically. Default: True.
        """

        super().__init__()
        self.queue = self._resolve_queue(queue)
        _handlers = self._resolve_handlers(handlers)
        self._listener = QueueListener(self.queue, *_handlers, respect_handler_level=respect_handler_level)
        self._atexit_registered = False
        if auto_run:
            self._listener.start()
            # Register a guarded stop so a manual stop() + interpreter exit
            # does not double-call QueueListener.stop() (not idempotent < 3.13).
            atexit.register(self.stop)
            self._atexit_registered = True

    def stop(self) -> None:
        """Stop the queue listener safely, even if already stopped.

        Unregisters the atexit callback first so interpreter shutdown will not
        invoke ``QueueListener.stop`` a second time. On Python < 3.13 a second
        ``stop()`` raises ``AttributeError`` because ``_thread`` is already
        ``None`` after the first call.
        """
        if self._atexit_registered:
            try:
                atexit.unregister(self.stop)
            except Exception:  # pragma: no cover - best effort on exotic interpreters
                pass
            self._atexit_registered = False

        if self._listener._thread is not None:
            self._listener.stop()

    def prepare(self, record: LogRecord) -> LogRecord:
        """Prepares a record for queuing.

        Mirrors ``logging.handlers.QueueHandler.prepare``: formats the record and removes unpickleable items so the
        record can safely cross the queue to the listener thread.

        Args:
            record: A logging.LogRecord object.

        Returns:
            A copy of the record, safe to enqueue.
        """

        msg = self.format(record)
        record = copy.copy(record)
        record.message = msg
        record.msg = msg
        record.args = None
        record.exc_info = None
        record.exc_text = None
        record.stack_info = None
        return record

    def enqueue(self, record: LogRecord):
        """Enqueues a record on the queue using ``put_nowait``.

        Args:
            record: A logging.LogRecord object.
        """

        self.queue.put_nowait(record)

    def emit(self, record: LogRecord):
        """Processes the specified logging record by enqueuing it for the listener.

        Args:
            record: A logging.LogRecord object.
        """

        try:
            self.enqueue(self.prepare(record))
        except Exception:
            self.handleError(record)

    @staticmethod
    def _resolve_queue(queue: Any) -> Any:  # pragma: no cover
        """Resolves and evaluates queue object."""

        if not isinstance(queue, logging.config.ConvertingDict):
            return queue
        if "__resolved_value__" in queue:
            return queue["__resolved_value__"]
        cname = queue.pop("class")
        klass = queue.configurator.resolve(cname)
        props = queue.pop(".", None)
        kwargs = {k: queue[k] for k in queue if logging.config.valid_ident(k)}
        result = klass(**kwargs)
        if props:
            for name, value in props.items():
                setattr(result, name, value)
        queue["__resolved_value__"] = result
        return result

    @staticmethod
    def _resolve_handlers(handlers: Any) -> Any:  # pragma: no cover
        """Resolves and evaluates handler objects."""

        if not isinstance(handlers, logging.config.ConvertingList):
            return handlers
        return [handlers[i] for i in range(len(handlers))]
