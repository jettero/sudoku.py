# I like makefiles. this is completely optional and you needn't use it for any reason (other than liking makefiles).

test: .test-reqs
	pytest

cov coverage: .test-reqs
	pytest --cov sudoku --cov-report term-missing:skip-covered --no-cov-on-fail --cov-fail-under 100

ipy ipython: .IPY-reqs

.%-reqs: %-requirements.txt
	pip install -U pip wheel -r $< | tee $@
