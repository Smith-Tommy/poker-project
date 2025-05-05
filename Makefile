.PHONY: test dist

test:
	PYTHONPATH=. pytest --cov=poker --cov-report=term-missing

dist:
	\tpython -m build