all: test

venv:
	@virtualenv venv -p `python -c "import sys; print('%s/bin/python' % getattr(sys, 'real_prefix', sys.prefix))"`
	@venv/bin/pip install rpython rply pytest flake8

ensure-venv:
	@if [ ! -f venv/bin/pytest ]; then $(MAKE) venv; fi

compile: ensure-venv
	@PYTHONPATH=. venv/bin/rpython -O2 nolang/target.py

clean:
	@rm -rf venv
	@rm -f nolang-c

lint: ensure-venv
	@flake8

test: ensure-venv
	@venv/bin/pytest tests --tb=short

.PHONY: all venv ensure-venv clean compile test lint
