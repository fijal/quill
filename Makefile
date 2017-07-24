all: test

venv:
	@git submodule update --init
	@virtualenv venv -p `python -c "import sys; print('%s/bin/python' % getattr(sys, 'real_prefix', sys.prefix))"`
	@venv/bin/pip install rply pytest
	@ln -fs `pwd`/vendor/pypy/rpython venv/lib/python2.7/site-packages

compile:
	@PYTHONPATH=. venv/bin/python vendor/pypy/rpython/bin/rpython -O2 nolang/target.py

clean:
	@rm -rf venv

test:
	@if [ ! -f venv/bin/pytest ]; then $(MAKE) venv; fi
	@venv/bin/pytest tests --tb=short

.PHONY: all venv clean compile test
