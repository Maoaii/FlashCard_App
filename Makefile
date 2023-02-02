PYTHON = python3

.PHONY = help run clean setup

help:
	@echo "---------------HELP-----------------"	
	@echo "To setup the project dependencies, type 'make setup'"
	@echo "To run the project type 'make run'"
	@echo "------------------------------------"

setup:
	@echo "Setting up the project"
	pip install --upgrade pip
	pip3 install -r requirements.txt
	@echo done

run:
	${PYTHON} main.py

clean:
	rm -rf __pycache__