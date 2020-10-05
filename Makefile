.DEFAULT_GOAL := about
APP_NAME="structlog_ext_utils"
VERSION := $(shell cat $(APP_NAME)/__version__.py | cut -d'"' -f 2)
SKIP_STYLE=0

lint:
ifeq ($(SKIP_STYLE), 0)
	@echo "> running isort..."
	isort $(APP_NAME)
	isort tests
	@echo "> running black..."
	black $(APP_NAME)
	black tests
endif
	@echo "> running flake8..."
	flake8 $(APP_NAME)
	flake8 tests
	@echo "> running mypy..."
	mypy $(APP_NAME)

tests:
	@echo "> unittest"
	python -m pytest -v --cov-report xml --cov-report term --cov=$(APP_NAME)

docs:
	@echo "> generate project documentation..."
	portray server

install-deps:
	@echo "> installing dependencies..."
	pip install -r requirements-dev.txt

tox:
	@echo "> running tox..."
	tox -r -p all

about:
	@echo "> $(APP_NAME): $(VERSION)"
	@echo ""
	@echo "make lint         - Runs: [isort > black > flake8 > mypy]"
	@echo "make tests        - Execute tests."
	@echo "make tox          - Runs tox."
	@echo "make docs         - Generate project documentation."
	@echo "make install-deps - Install development dependencies."
	@echo ""
	@echo "mailto: alexandre.fmenezes@gmail.com"

ci: lint tests
ifeq ($(CI), true)
	@echo "> download CI dependencies"
	curl -L https://codeclimate.com/downloads/test-reporter/test-reporter-latest-linux-amd64 > ./cc-test-reporter
	chmod +x ./cc-test-reporter
	@echo "> uploading report..."
	codecov --file coverage.xml -t $$CODECOV_TOKEN
	./cc-test-reporter format-coverage -t coverage.py -o codeclimate.json
	./cc-test-reporter upload-coverage -i codeclimate.json -r $$CC_TEST_REPORTER_ID
endif

all: lint tests doc install-deps

.PHONY: lint tests docs install-deps ci all
