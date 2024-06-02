# I like makefiles. this is completely optional and you needn't use it for any reason (other than liking makefiles).

test: .test-reqs
	pytest

ipy ipython: .IPY-reqs

.%-reqs: %-requirements.txt
	pip install -U pip wheel -r $< | tee $@
