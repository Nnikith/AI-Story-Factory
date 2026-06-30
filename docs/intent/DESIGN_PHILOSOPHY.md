# Design Philosophy

AI Story Factory is built around a few core principles.

## Local First

Prefer local AI models when practical to reduce cost and improve reproducibility.

## Provider Architecture

Each major subsystem should be replaceable:

- images
- voice
- subtitles
- renderer
- motion
- scene planning
- prompts

## Timeline as Source of Truth

`timeline.json` is the central contract. Every stage reads it, updates its own fields, and writes it back.

## Small Stages

Every pipeline stage should be independently runnable.

## Cache Expensive Work

Generated images, audio, and future model outputs should be cached.

## Reproducibility

The project should be Git-versioned, Makefile-driven, and reproducible on a local WSL2 Ubuntu environment.
