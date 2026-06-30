# Documentation Index

This directory contains the authoritative documentation for AI Story Factory.

The docs are organized to be navigable in GitHub. Every section has a home page, and the root `docs/README.md` is the canonical entry point.

---

## Repo

- **[Repo README](../README.md)** — top-level project entry point

---

## Core

- **[Core Index](core/README.md)** — architecture, contracts, configuration, and subsystem design
- **[Architecture](core/ARCHITECTURE.md)** — end-to-end system architecture
- **[Pipeline Specification](core/PIPELINE_SPEC.md)** — pipeline stages, inputs, outputs, and responsibilities
- **[Timeline Schema](core/TIMELINE_SCHEMA.md)** — central timeline contract
- **[Configuration](core/CONFIGURATION.md)** — configuration system and default YAML reference
- **[Coding Standards](core/CODING_STANDARDS.md)** — Python and project conventions
- **[Image Architecture](core/IMAGE_ARCHITECTURE.md)** — image providers, cache, and local AI backend
- **[Voice Architecture](core/VOICE_ARCHITECTURE.md)** — voice providers, Kokoro, and voice cache
- **[Subtitle Architecture](core/SUBTITLE_ARCHITECTURE.md)** — subtitle providers, chunking, and timing
- **[Renderer Architecture](core/RENDERER_ARCHITECTURE.md)** — FFmpeg renderer and motion provider integration
- **[Scene Planning](core/SCENE_PLANNING.md)** — scene planner provider architecture
- **[Prompt Architecture](core/PROMPT_ARCHITECTURE.md)** — prompt provider architecture

---

## Operations

- **[Operations Index](operations/README.md)** — runtime workflow, releases, scripts, and testing
- **[Git Workflow](operations/GIT_WORKFLOW.md)** — branching, commits, tags, and releases
- **[Working Style](operations/WORKING_STYLE.md)** — sprint workflow and engineering cadence
- **[Script Commands](operations/SCRIPT_COMMANDS.md)** — Makefile and shell command reference
- **[Changelog](operations/CHANGELOG.md)** — release history
- **[Release Process](operations/RELEASE_PROCESS.md)** — release checklist
- **[Testing](operations/TESTING.md)** — validation commands and smoke checks
- **[Benchmarks](operations/BENCHMARKS.md)** — performance measurements
- **[TODO](operations/TODO.md)** — active tasks

---

## Intent

- **[Intent Index](intent/README.md)** — product direction and project philosophy
- **[Project Proposal](intent/PROJECT_PROPOSAL.md)** — project purpose and goals
- **[Roadmap](intent/ROADMAP.md)** — planned phases
- **[Milestones](intent/MILESTONES.md)** — milestone history
- **[Design Philosophy](intent/DESIGN_PHILOSOPHY.md)** — local-first, modular, provider-based engineering approach
- **[Later](intent/LATER.md)** — intentionally deferred ideas

---

## Safety

- **[Safety Index](safety/README.md)** — safety and model-risk documentation
- **[Content Policy](safety/CONTENT_POLICY.md)** — content generation boundaries
- **[Model Risk Notes](safety/MODEL_RISK_NOTES.md)** — model limitations and mitigations
