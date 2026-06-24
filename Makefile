PYTHON ?= python
APP_MODULE = telemetry_monitor.api.app:app
PYTHONPATH_VALUE = src

.PHONY: install test lint seed demo run-api clean

install:
	$(PYTHON) -m pip install --upgrade pip
	$(PYTHON) -m pip install -e ".[dev]"

test:
	PYTHONPATH=$(PYTHONPATH_VALUE) $(PYTHON) -m pytest

lint:
	PYTHONPATH=$(PYTHONPATH_VALUE) $(PYTHON) -m ruff check src tests

seed:
	PYTHONPATH=$(PYTHONPATH_VALUE) $(PYTHON) scripts/seed_demo_data.py

demo:
	PYTHONPATH=$(PYTHONPATH_VALUE) $(PYTHON) scripts/run_demo.py

run-api:
	PYTHONPATH=$(PYTHONPATH_VALUE) $(PYTHON) -m uvicorn $(APP_MODULE) --reload

clean:
	rm -rf .pytest_cache .ruff_cache __pycache__ data/telemetry.db
	find . -type d -name __pycache__ -prune -exec rm -rf {} +
