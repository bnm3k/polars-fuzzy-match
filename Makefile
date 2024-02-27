.SILENT:
.DEFAULT_GOAL:=dev

.PHONY: run build-dev clean format
dev: build-dev
	python examples/usage.py

build-dev: .build-dev

.build-dev: $(wildcard src/*.rs)
	maturin develop
	touch .build-dev

format:
	ruff format polars_fuzzy_match/

clean:
	rm .build-dev
