PYTHON=python3
VENV=.venv
PIP=$(VENV)/bin/pip
PY=$(VENV)/bin/python

.PHONY: setup bootstrap doctor start stop reset smoke demo scenes images voice subtitles render clean clean-output clean-cache clean-logs commit chmod zone

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

clean-output:
	find data/output -mindepth 1 ! -name ".gitkeep" -delete

clean-cache:
	find data/cache -mindepth 1 ! -name ".gitkeep" -delete

clean-logs:
	find data/logs -mindepth 1 ! -name ".gitkeep" -delete

clean: zone clean-cache clean-logs
	@echo "Clean complete."

commit:
	@if [ -z "$(MSG)" ]; then \
		bash scripts/git_commit.sh; \
	else \
		bash scripts/git_commit.sh "$(MSG)"; \
	fi

chmod:
	chmod +x scripts/*.sh

zone:
	find . -name "*:Zone.Identifier" -delete