PYTHON=python3
VENV=.venv
PIP=$(VENV)/bin/pip
PY=$(VENV)/bin/python

.PHONY: setup bootstrap doctor start stop reset smoke demo scenes images voice subtitles render clean clean-output clean-cache clean-logs commit chmod zone timeline stage1 stage2 stage3 stage4 stage5

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

demo: stage1 stage2 stage3 stage4 stage5
	@echo "Demo pipeline complete."

timeline:
	$(PY) -m app.pipeline.stage1_story

stage1: timeline

scenes: stage1

images: stage2

stage2:
	$(PY) -m app.pipeline.stage2_images

voice: stage3

stage3:
	$(PY) -m app.pipeline.stage3_voice

subtitles: stage4

stage4:
	$(PY) -m app.pipeline.stage4_subtitles

render: stage5

stage5:
	$(PY) -m app.pipeline.stage5_video

clean-output:
	find data/output -mindepth 1 -delete
	mkdir -p data/output/images data/output/audio data/output/subtitles data/output/videos data/output/metadata
	touch data/output/.gitkeep

clean-cache:
	find data/cache -mindepth 1 -delete
	touch data/cache/.gitkeep

clean-logs:
	find data/logs -mindepth 1 -delete
	touch data/logs/.gitkeep

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
