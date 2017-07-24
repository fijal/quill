venv:
	git submodule update --init
	virtualenv venv -p `python -c "import sys; print('%s/bin/python' % getattr(sys, 'real_prefix', sys.prefix))"`
	venv/bin/pip install rply pytest
	ln -fs `pwd`/vendor/pypy/rpython venv/lib/python2.7/site-packages

clean:
	rm -rf venv

test: venv
	venv/bin/pytest tests --tb=short

.PHONY: venv clean test
