# -*- coding: utf-8 -*-

if __name__ == "__main__":
    from pynamodb_session_manager.tests import run_cov_test

    run_cov_test(
        __file__,
        "pynamodb_session_manager",
        is_folder=True,
        preview=False,
    )
