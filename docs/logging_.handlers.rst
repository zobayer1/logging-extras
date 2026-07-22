Handlers
--------

QueueListenerHandler
++++++++++++++++++++

.. note::

   On **Python 3.12+**, ``logging.config.dictConfig`` natively supports configuring a
   ``QueueHandler`` with an attached ``QueueListener`` (see the `Python docs
   <https://docs.python.org/3/library/logging.config.html#configuring-queuehandler-and-queuelistener>`__).
   Users on 3.12+ can — and generally should — use the standard library directly.

   ``logging-extras``'s ``QueueListenerHandler`` is primarily a backport for
   **Python 3.8 – 3.11** that provides the same end-to-end dictConfig-based queue
   setup on older runtimes. The handler intentionally subclasses ``logging.Handler``
   (not ``logging.handlers.QueueHandler``) so it is not intercepted by the
   3.12+ stdlib special case.

A simple queue-logging handler utilizing ``QueueListener`` for configured handlers (intentionally subclasses ``logging.Handler``, not ``logging.handlers.QueueHandler``, so Python 3.12+ ``dictConfig`` does not special-case construction). This is helpful for detaching the logger handlers from the main threads, which reduces the risk of getting blocked, for example, when using slower handlers such as smtp, file, or socket handlers.

Example Usage
*************

An example YAML configuration file utilizing ``QueueListenerHandler``

.. literalinclude:: snippets/queue_listener_handler/logging.yaml
   :caption: logging.yaml
   :language: yaml
   :emphasize-lines: 2-5, 18-23, 27-28

Just load the configuration file and start logging.

.. literalinclude:: snippets/queue_listener_handler/test_logger.py
   :caption: test_logger.py
   :language: python

Optional Params
***************

A queue object must be passed since the handler does not set a default queue implementation. Set ``maxsize: -1`` to make the queue unlimited.

Module Members
++++++++++++++

.. automodule:: logging_.handlers.queue_listener_handler
   :members:
   :special-members:
   :show-inheritance:
   :exclude-members: emit
