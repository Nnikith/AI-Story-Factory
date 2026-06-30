# Roadmap

## Phase 0 — Setup

- Create project repository
- Set up WSL2 Ubuntu environment
- Install Python, FFmpeg, Make, Git
- Create folder structure
- Add basic Makefile
- Add Git workflow

## Phase 1 — 60-Second MVP

Goal: Generate one complete 60-second video from story text.

Tasks:

- Load story from `data/input/story.txt`
- Generate scene JSON
- Create placeholder images
- Generate or attach voice audio
- Generate subtitles
- Burn subtitles into video
- Export MP4

## Phase 2 — Local AI Image Generation

- Add SDXL or other local image generation
- Add image caching
- Add prompt templates
- Add style settings

## Phase 3 — Voice Quality

- Test paid TTS
- Test local TTS
- Add voice settings
- Add pacing controls

## Phase 4 — Long-Form Pipeline

- Scale from 1 minute to 10 minutes
- Scale from 10 minutes to 30 minutes
- Scale from 30 minutes to 2 hours

## Phase 5 — Multi-Format Output

- Landscape 16:9
- Vertical 9:16
- Square 1:1
- Shorts generation

## Phase 6 — Automation

- Batch queue
- Overnight processing
- Auto thumbnails
- Metadata generation
- YouTube upload
