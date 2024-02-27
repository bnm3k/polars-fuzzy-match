.SILENT:
.DEFAULT_GOAL:=dev

.PHONY: run build-dev clean format lint
dev: build-dev
	python examples/usage.py

build-dev: .build-dev

.build-dev: $(wildcard src/*.rs)
	maturin develop
	touch .build-dev

format:
	ruff format polars_fuzzy_match/
	cargo fmt --all

lint:
	cargo clippy --all-features

clean:
	rm .build-dev
