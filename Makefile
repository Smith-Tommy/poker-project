.PHONY: test dist

test:
\tpytest --cov=poker --cov-report=term-missing

dist:
\tpython -m build