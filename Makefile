PHONY: clean, lint

clean:
	@find . -type f -name "*.py[co]" -delete
	@find . -type d -name "__pycache__" -delete

## Lint using black
lint:
	@black api