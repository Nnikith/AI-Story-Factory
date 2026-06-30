from __future__ import annotations

from pathlib import Path

from app.core.timeline import Timeline


TIMELINE_PATH = Path("data/output/timeline.json")
SUBTITLE_PATH = Path("data/output/subtitles/subtitles.srt")


def _format_srt_time(seconds: float) -> str:
    ms_total = int(seconds * 1000)
    hours = ms_total // 3_600_000
    ms_total %= 3_600_000
    minutes = ms_total // 60_000
    ms_total %= 60_000
    secs = ms_total // 1000
    millis = ms_total % 1000
    return f"{hours:02d}:{minutes:02d}:{secs:02d},{millis:03d}"


def _scene_duration_seconds(scene: dict) -> float:
    return float(scene.get("duration_seconds") or scene.get("duration") or 6.0)


def run() -> None:
    timeline = Timeline.load(TIMELINE_PATH)

    SUBTITLE_PATH.parent.mkdir(parents=True, exist_ok=True)

    current = 0.0
    blocks: list[str] = []

    for index, scene in enumerate(timeline.scenes, start=1):
        duration = _scene_duration_seconds(scene)
        start = current
        end = current + duration
        narration = scene.get("narration", "")

        blocks.append(
            f"{index}\n"
            f"{_format_srt_time(start)} --> {_format_srt_time(end)}\n"
            f"{narration}\n"
        )

        scene["subtitle_text"] = narration
        scene["subtitle_start"] = start
        scene["subtitle_end"] = end
        scene.setdefault("status", {})["subtitle"] = "done"

        current = end

    SUBTITLE_PATH.write_text("\n".join(blocks), encoding="utf-8")

    timeline.data.setdefault("outputs", {})
    timeline.data["outputs"]["subtitles"] = str(SUBTITLE_PATH)

    timeline.save(TIMELINE_PATH)

    print(f"Created subtitles: {SUBTITLE_PATH}")


if __name__ == "__main__":
    run()
