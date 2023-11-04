.PHONY: build

shell:
	python3 -B src/main.py --out=bin/hello.output

build:
	@echo Compiling...
	@mkdir -p bin
	pyinstaller --onefile --distpath ./bin --name bfi ./src/main.py
	@echo Done!