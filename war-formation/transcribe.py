#!/usr/bin/env python3
"""Transcribe the 3M system videos to timestamped text.

Audio is extracted with the ffmpeg binary that ships inside imageio_ffmpeg, then
transcribed locally with faster-whisper. No network service is involved and the
video files never leave the machine.

Usage:  python transcribe.py <folder-with-mp4s> [model]
        model defaults to "small" (good accuracy on trading jargon, ~10x realtime on CPU)
"""

import os
import subprocess
import sys
import time

import imageio_ffmpeg
from faster_whisper import WhisperModel

SRC = sys.argv[1] if len(sys.argv) > 1 else "."
MODEL = sys.argv[2] if len(sys.argv) > 2 else "small"
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "transcripts")
TMP = os.environ.get("TEMP", ".")

os.makedirs(OUT, exist_ok=True)
ff = imageio_ffmpeg.get_ffmpeg_exe()

videos = sorted(f for f in os.listdir(SRC) if f.lower().endswith(".mp4"))
print("model:", MODEL, "| videos:", len(videos), flush=True)

model = WhisperModel(MODEL, device="cpu", compute_type="int8")
print("model loaded", flush=True)

for v in videos:
    stem = os.path.splitext(v)[0]
    dest = os.path.join(OUT, stem + ".txt")
    if os.path.exists(dest) and os.path.getsize(dest) > 200:
        print("skip (done):", stem, flush=True)
        continue

    wav = os.path.join(TMP, "3m_audio.wav")
    t0 = time.time()
    r = subprocess.run(
        [ff, "-y", "-i", os.path.join(SRC, v), "-vn", "-ac", "1", "-ar", "16000", "-f", "wav", wav],
        capture_output=True, text=True,
    )
    if r.returncode != 0:
        print("ffmpeg FAILED:", stem, r.stderr[-300:], flush=True)
        continue

    segs, info = model.transcribe(wav, beam_size=1, vad_filter=True)
    lines = []
    for s in segs:
        mm, ss = divmod(int(s.start), 60)
        hh, mm = divmod(mm, 60)
        stamp = f"{hh:02d}:{mm:02d}:{ss:02d}" if hh else f"{mm:02d}:{ss:02d}"
        lines.append(f"[{stamp}] {s.text.strip()}")

    with open(dest, "w", encoding="utf-8") as fh:
        fh.write(f"# {stem}\n# duration {info.duration:.0f}s | language {info.language}\n\n")
        fh.write("\n".join(lines))

    print(f"done {stem}: {len(lines)} segments, {info.duration:.0f}s audio in "
          f"{time.time()-t0:.0f}s -> {dest}", flush=True)
    try:
        os.remove(wav)
    except OSError:
        pass

print("ALL DONE", flush=True)
