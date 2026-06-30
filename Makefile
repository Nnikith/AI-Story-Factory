PYTHON=python3
VENV=.venv
PIP=$(VENV)/bin/pip
PY=$(VENV)/bin/python

.PHONY: setup bootstrap doctor start stop reset smoke demo scenes images voice subtitles render clean commit chmod

setup:
	$(PYTHON) -m venv $(VENV)
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt

bootstrap:
	bash scripts/bootstrap.sh

doctor:
	bash scripts/doctor.sh

start:
	bash scripts/start.sh

stop:
	bash scripts/stop.sh

reset:
	bash scripts/reset.sh

smoke:
	bash scripts/smoke.sh

demo: scenes images voice subtitles render
	@echo "Demo pipeline complete."

scenes:
	$(PY) scripts/placeholder_scenes.py

images:
	$(PY) scripts/placeholder_images.py

voice:
	$(PY) scripts/placeholder_voice.py

subtitles:
	$(PY) scripts/placeholder_subtitles.py

render:
	@if [ -f scripts/render_demo_video.py ]; then $(PY) scripts/render_demo_video.py; else $(PY) scripts/placeholder_render.py; fi

clean:
	rm -rf data/output/*

commit:
	bash scripts/git_commit.sh "$(MSG)"

chmod:
	chmod +x scripts/*.sh
