PYTHON=python3
export VENV=venv
export SRC=./automate_ui/
export UID=$(shell id -u)
export GID=$(shell id -g)


#----------------------------------------------------------
# BUILD TARGETS
#----------------------------------------------------------

venv: setup.py setup.cfg
	$(PYTHON) -m venv $@
	. ./$@/bin/activate && pip install -U setuptools wheel pip
	. ./$@/bin/activate && pip install -e .[dev]
	touch $@

build: setup.py setup.cfg
	pip install -U setuptools wheel pip
	pip install -e .[dev]

install-playwright:
	playwright install

build-ui: build install-playwright

.PHONY: package
package: $(VENV)
	. ./$(VENV)/bin/activate && python setup.py bdist_wheel

.PHONY: package-clean
package-clean:
	rm -rf ./build
	rm -rf ./dist
	rm -rf *.egg-info

#----------------------------------------------------------
# DEV TARGETS
#----------------------------------------------------------

.PHONY: lint
lint: $(VENV)
	./dev_scripts/lint.sh

.PHONY: format
format: $(VENV)
	./dev_scripts/format.sh

.PHONY: clean
clean: package-clean
	find ./ -name "*.pyc" -delete
	find ./ -name "__pycache__" -delete
	rm -rf ./.mypy_cache
	rm -rf ./.pytest_cache
	rm -rf ./venv
	rm -rf ./docker-venv

#----------------------------------------------------------
# TEST TARGETS
#----------------------------------------------------------

.PHONY: test
test:
	pytest -svv $(TEST_SRC) $(TEST_ARGS)

#----------------------------------------------------------
# LOCAL DEV ENV SETUP TARGETS
#----------------------------------------------------------

local-setup: venv install-playwright

rebuild-local: clean local-setup
