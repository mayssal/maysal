import os
import tempfile
from typing import List, Optional


def is_image_file(path: str) -> bool:
    ext = os.path.splitext(path)[1].lower()
    return ext in {".jpg", ".jpeg", ".png", ".bmp", ".tiff", ".tif"}


def is_video_file(path: str) -> bool:
    ext = os.path.splitext(path)[1].lower()
    return ext in {".mp4", ".avi", ".mov", ".mkv", ".wmv"}


def load_image_bgr(path: str):
    import cv2
    img = cv2.imread(path)
    return img


def extract_frames_from_video(path: str, fps: int = 1, max_frames: int = 20) -> List:
    import cv2

    cap = cv2.VideoCapture(path)
    if not cap.isOpened():
        return []
    input_fps = cap.get(cv2.CAP_PROP_FPS) or 30
    step = max(int(round(input_fps / max(1, fps))), 1)

    frames = []
    idx = 0
    kept = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        if idx % step == 0:
            frames.append(frame)
            kept += 1
            if kept >= max_frames:
                break
        idx += 1
    cap.release()
    return frames


essential_audio_codecs = {"aac", "mp3", "pcm_s16le"}


def extract_audio_from_video(path: str) -> Optional[str]:
    """Extract audio track to a temporary WAV file using moviepy.
    Returns path to the WAV or None if extraction fails.
    """
    try:
        from moviepy.editor import VideoFileClip
        tmpdir = tempfile.mkdtemp(prefix="biomatch_")
        out_wav = os.path.join(tmpdir, "audio.wav")
        with VideoFileClip(path) as v:
            if v.audio is None:
                return None
            v.audio.write_audiofile(out_wav, fps=16000, nbytes=2, codec="pcm_s16le", verbose=False, logger=None)
        return out_wav
    except Exception:
        return None