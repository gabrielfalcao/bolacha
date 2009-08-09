all: clean test

clean:
	@echo "Cleaning up all *.pyc files ..."
	@find . -name '*.pyc' -delete
	@echo "Cleaning up all temp files ..."
	@find . -name '*.tmp' -delete
	@rm -f log.txt
	@echo "Cleaning up build files ..."
	@rm -rf build

test: run_server
	@echo "Running all tests ..."
	@nosetests -s --with-coverage --cover-package=bolacha tests/{unit,functional}
	@echo "Done."
	@make clean

unit:
	@echo "Running unit tests ..."
	@nosetests -s --with-coverage --cover-package=bolacha tests/unit
	@echo "Done."

run_server: kill_server
	@echo "Running builtin HTTP server ..."
	@python tests/functional/bolacha_server.py 2>&1 > log.txt &
	@sleep 2

functional: run_server
	@echo "Running functional tests ..."
	@nosetests -s --with-coverage --cover-package=bolacha tests/functional
	@make clean
	@make kill_server

kill_server:
	@echo "Shutting down builtin HTTP server ..."
	@-ps aux | egrep 'bolacha_server' | egrep -v grep | awk '{ print $$2 }' | xargs kill -9 2>&1 /dev/null
	@echo "Done."

build: test
	@echo "Building bolacha"
	@python setup.py build
	@echo "Done."
