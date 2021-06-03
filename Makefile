PHONY: clean, lint

clean:
	@find ./api -type f -name "*.py[co]" -delete
	@find ./api -type d -name "__pycache__" -delete
	@find ./api -type d -name ".pytest_cache" -delete

## Lint using black
lint:
	@black api
