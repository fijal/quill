venv:
	virtualenv venv -p python2.7
	venv/bin/pip install rply pytest
	ln -s `pwd`/vendor/pypy/rpython venv/lib/python2.7/site-packages

test: venv
	venv/bin/pytest tests --tb=short
