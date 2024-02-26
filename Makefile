.SILENT:
.DEFAULT_GOAL:=dev

.PHONY: run build-dev clean
dev: build-dev
	python examples/usage.py

build-dev: .build-dev

.build-dev: $(wildcard src/*.rs)
	maturin develop
	touch .build-dev

clean:
	rm .build-dev
