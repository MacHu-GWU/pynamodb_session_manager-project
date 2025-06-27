.. _release_history:

Release and Version History
==============================================================================


x.y.z (Backlog)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Features and Improvements**

**Minor Improvements**

**Bugfixes**

**Miscellaneous**


0.1.2 (2025-06-27)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Breaking Changes**

- Changed parameter order in ``use_boto_session()`` from ``(bsm, table, restore_on_exit)`` to ``(table, bsm, restore_on_exit)`` for better API consistency.

**Minor Improvements**

- Enhanced ``use_boto_session()`` to accept ``None`` for the ``bsm`` parameter. When ``bsm`` is ``None``, the context manager has no effect, providing a clean API for conditional credential switching without separate if/else logic.


0.1.1 (2025-06-27)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
- First release
- Add the following public APIs:
    - ``pynamodb_session_manager.api.use_boto_session``
    - ``pynamodb_session_manager.api.reset_connection``
