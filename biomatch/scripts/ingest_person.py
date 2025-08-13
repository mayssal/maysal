import argparse
import os
from typing import Optional

from app.config import load_config
from app.db.db_client import DatabaseClient
from app.recognition.video_utils import is_image_file, is_video_file, load_image_bgr, extract_frames_from_video, extract_audio_from_video
from app.recognition.preprocessing import enhance_image


def _embed_face_from_image(path: str, detection_threshold: float, enhance: bool) -> Optional[list]:
    from app.recognition.face_recognition_module import FaceRecognizer

    img = load_image_bgr(path)
    if img is None:
        return None
    if enhance:
        img = enhance_image(img)
    recog = FaceRecognizer(detection_threshold=detection_threshold)
    return recog.embed_bgr_image(img)


def _embed_face_from_video(path: str, detection_threshold: float, enhance: bool, fps: int, max_frames: int) -> Optional[list]:
    from app.recognition.face_recognition_module import FaceRecognizer

    frames = extract_frames_from_video(path, fps=fps, max_frames=max_frames)
    if not frames:
        return None
    recog = FaceRecognizer(detection_threshold=detection_threshold)
    return recog.embed_bgr_frames(frames, enhance=enhance)


def _embed_voice_from_video(path: str) -> Optional[list]:
    from app.recognition.voice_recognition_module import VoiceRecognizer

    wav = extract_audio_from_video(path)
    if wav is None:
        return None
    recog = VoiceRecognizer()
    return recog.embed_audio_file(wav)


def run():
    parser = argparse.ArgumentParser(description="Ingestion d'une personne dans la base BioMatch")
    parser.add_argument("--name", required=True)
    parser.add_argument("--email", default=None)
    parser.add_argument("--phone", default=None)
    parser.add_argument("--address", default=None)
    parser.add_argument("--notes", default=None)
    parser.add_argument("--image", default=None, help="Image de référence (portrait)")
    parser.add_argument("--video", default=None, help="Vidéo de référence (contient visage et/ou voix)")
    parser.add_argument("--config", default=None)

    args = parser.parse_args()
    config = load_config(args.config)

    db = DatabaseClient(config["database"]["url"])

    face_emb = None
    voice_emb = None

    if args.image and is_image_file(args.image):
        face_emb = _embed_face_from_image(
            args.image,
            detection_threshold=config["face"]["detection_threshold"],
            enhance=config["face"].get("image_enhance", True),
        )

    if args.video and is_video_file(args.video):
        # Face from video frames
        vid_face = _embed_face_from_video(
            args.video,
            detection_threshold=config["face"]["detection_threshold"],
            enhance=config["face"].get("image_enhance", True),
            fps=config["video"]["sample_fps"],
            max_frames=config["video"]["max_frames"],
        )
        if vid_face is not None:
            face_emb = vid_face
        # Voice
        vid_voice = _embed_voice_from_video(args.video)
        if vid_voice is not None:
            voice_emb = vid_voice

    person_id = db.insert_person(
        full_name=args.name,
        email=args.email,
        phone=args.phone,
        address=args.address,
        notes=args.notes,
        face_embedding=face_emb,
        voice_embedding=voice_emb,
    )
    print(f"Personne insérée avec id={person_id}")


if __name__ == "__main__":
    run()