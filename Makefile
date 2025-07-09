PYTHON=python3
export VENV=venv
export SRC=./automate_ui/
export UID=$(shell id -u)
export GID=$(shell id -g)


#----------------------------------------------------------
# BUILD TARGETS
#----------------------------------------------------------

venv:
	$(PYTHON) -m venv $@
	. ./$@/bin/activate && pip install -U setuptools wheel pip
	. ./$@/bin/activate && pip install -e .[dev]
	touch $@

build:
	pip install -U setuptools wheel pip
	python install_deps.py

install-playwright: $(VENV)
	. ./$(VENV)/bin/activate && playwright install

build-ui: build install-playwright

.PHONY: package
package: $(VENV)
	. ./$(VENV)/bin/activate && pip install build
	. ./$(VENV)/bin/activate && python -m build

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

#----------------------------------------------------------
# TEST TARGETS
#----------------------------------------------------------

.PHONY: test
test:
	pytest -svv tests/unit/**

#----------------------------------------------------------
# LOCAL DEV ENV SETUP TARGETS
#----------------------------------------------------------

local-setup: venv install-playwright

rebuild-local: clean local-setup

mobile-setup:
	npm install
	npm run install-appium-drivers

clean-mobile:
	rm -rf node_modules package-lock.json

rebuild-mobile-setup: clean-mobile mobile-setup
