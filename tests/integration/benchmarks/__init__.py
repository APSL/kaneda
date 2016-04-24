import pytest

mark_benchmark = pytest.mark.skipif(not pytest.config.getoption("--run-benchmark"),
                                    reason="need --run-benchmark option to run")
