all: test

venv:
	@git submodule update --init
	@virtualenv venv -p `python -c "import sys; print('%s/bin/python' % getattr(sys, 'real_prefix', sys.prefix))"`
	@ln -sf ../../../../vendor/pypy/rpython venv/lib/python2.7/site-packages
	@echo '#!${PWD}/venv/bin/python\n' > venv/bin/rpython
	@cat vendor/pypy/rpython/bin/rpython >> venv/bin/rpython
	@chmod +x venv/bin/rpython
	@venv/bin/pip install rply pytest flake8

ensure-venv:
	@if [ ! -f venv/bin/pytest ]; then $(MAKE) venv; fi

compile: ensure-venv
	@PYTHONPATH=. venv/bin/rpython $(RPYTHONFLAGS) -O2 nolang/target.py

clean:
	@rm -rf venv
	@rm -f nolang-c

lint: ensure-venv
	@venv/bin/flake8

test: ensure-venv
	@venv/bin/pytest tests --tb=short

check: lint test compile

install-vscode-extension:
	ln -fs `pwd`/editor-support/vscode ~/.vscode/extensions/quill

uninstall-vscode-extension:
	rm -f ~/.vscode/extensions/quill

.PHONY: all venv ensure-venv clean compile test check lint install-vscode-extension uninstall-vscode-extension
