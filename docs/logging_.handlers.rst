Handlers
--------

QueueListenerHander
+++++++++++++++++++

A simple ``QueueHandler`` subclass implementation utilizing ``QueueListener`` for configured handlers. This is helpful for detaching the logger handlers from the main threads, which reduces the risk of getting blocked, for example, when using slower handlers such as smtp, file, or socket handlers.

An example YAML configuration file utilizing ``QueueListenerHander``

.. literalinclude:: snippets/logging.yaml
   :caption: logging.yaml
   :language: yaml
   :emphasize-lines: 2-5, 18-23, 27-28

**Note:** A queue object must be passed since the handler does not set a default queue implementation. Set ``maxsize: -1`` to make the queue unlimited.

Just load the configuration file and start logging.

.. literalinclude:: snippets/test_logger.py
   :caption: test_logger.py
   :language: python

Module Members
++++++++++++++

.. automodule:: logging_.handlers.queue_listener_handler
   :members:
   :special-members:
   :undoc-members:
   :show-inheritance:
