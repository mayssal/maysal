import argparse
import os
from typing import Dict, List, Optional

from app.config import load_config
from app.ui.cli import print_match_results, print_no_match
from app.recognition.video_utils import is_image_file, is_video_file, extract_frames_from_video, extract_audio_from_video, load_image_bgr
from app.recognition.preprocessing import enhance_image
from app.recognition.matching import score_candidates
from app.db.db_client import DatabaseClient


def _embed_face(image_bgr, config: Dict):
    # Lazy import heavy libs inside the function
    from app.recognition.face_recognition_module import FaceRecognizer

    recognizer = FaceRecognizer(detection_threshold=config["face"]["detection_threshold"]) 
    if config["face"].get("image_enhance", True):
        image_bgr = enhance_image(image_bgr)
    face_embedding = recognizer.embed_bgr_image(image_bgr)
    return face_embedding


def _embed_faces_from_frames(frames_bgr: List, config: Dict) -> Optional[List[float]]:
    from app.recognition.face_recognition_module import FaceRecognizer

    recognizer = FaceRecognizer(detection_threshold=config["face"]["detection_threshold"]) 
    return recognizer.embed_bgr_frames(frames_bgr, enhance=config["face"].get("image_enhance", True))


def _embed_voice_from_wav(wav_path: str) -> Optional[List[float]]:
    from app.recognition.voice_recognition_module import VoiceRecognizer

    recognizer = VoiceRecognizer()
    return recognizer.embed_audio_file(wav_path)


def run():
    parser = argparse.ArgumentParser(description="BioMatch - Reconnaissance faciale et vocale")
    parser.add_argument("--input", required=True, help="Chemin vers l'image ou la vidéo de requête")
    parser.add_argument("--media-type", choices=["auto", "image", "video"], default="auto", help="Force le type de média si nécessaire")
    parser.add_argument("--use-face", action="store_true", help="Activer la reconnaissance faciale")
    parser.add_argument("--use-voice", action="store_true", help="Activer la reconnaissance vocale")
    parser.add_argument("--topk", type=int, default=None, help="Nombre de meilleurs candidats à afficher")
    parser.add_argument("--min-confidence", type=float, default=None, help="Seuil minimal de confiance à afficher")
    parser.add_argument("--config", type=str, default=None, help="Chemin d'un fichier config.yaml alternatif")

    args = parser.parse_args()
    config = load_config(args.config)

    # Apply CLI overrides
    if args.topk is not None:
        config["matching"]["topk"] = args.topk
    if args.min_confidence is not None:
        config["matching"]["min_confidence"] = args.min_confidence

    # Auto enable both if neither provided
    if not args.use_face and not args.use_voice:
        use_face = True
        use_voice = True
    else:
        use_face = args.use_face
        use_voice = args.use_voice

    input_path = args.input
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"Fichier introuvable: {input_path}")

    if args.media_type == "auto":
        if is_image_file(input_path):
            media_type = "image"
        elif is_video_file(input_path):
            media_type = "video"
        else:
            raise ValueError("Type de média non reconnu (utilisez --media-type pour forcer)")
    else:
        media_type = args.media_type

    # DB
    db = DatabaseClient(config["database"]["url"])
    candidates = db.fetch_candidates()  # list of dicts: {id, full_name, face_embedding, voice_embedding, meta}
    if len(candidates) == 0:
        print("La base ne contient aucune personne indexée.")
        return

    query_face_emb: Optional[List[float]] = None
    query_voice_emb: Optional[List[float]] = None

    if media_type == "image":
        if use_face:
            image_bgr = load_image_bgr(input_path)
            query_face_emb = _embed_face(image_bgr, config)
    elif media_type == "video":
        # Faces from frames
        if use_face:
            frames = extract_frames_from_video(
                input_path,
                fps=config["video"]["sample_fps"],
                max_frames=config["video"]["max_frames"],
            )
            if frames:
                query_face_emb = _embed_faces_from_frames(frames, config)
        # Voice from audio
        if use_voice:
            wav_path = extract_audio_from_video(input_path)
            if wav_path is not None:
                query_voice_emb = _embed_voice_from_wav(wav_path)
    else:
        raise ValueError("Type de média inconnu")

    if not query_face_emb and not query_voice_emb:
        print("Impossible d'extraire une empreinte biométrique du média fourni.")
        return

    results = score_candidates(
        query_face_emb=query_face_emb,
        query_voice_emb=query_voice_emb,
        candidates=candidates,
        face_weight=config["matching"]["face_weight"],
        voice_weight=config["matching"]["voice_weight"],
        topk=config["matching"]["topk"],
    )

    min_conf = config["matching"]["min_confidence"]
    if not results:
        print_no_match()
        return

    # Filter by min confidence for display
    filtered = [r for r in results if r["score"] >= min_conf]
    if not filtered:
        print_no_match()
        return

    print_match_results(filtered)


if __name__ == "__main__":
    run()