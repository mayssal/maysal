from typing import Dict, List, Optional
import math


def cosine_similarity(vec_a: List[float], vec_b: List[float]) -> float:
    if not vec_a or not vec_b:
        return 0.0
    if len(vec_a) != len(vec_b):
        # Different models or corrupted embeddings
        return 0.0
    dot = 0.0
    norm_a = 0.0
    norm_b = 0.0
    for a, b in zip(vec_a, vec_b):
        dot += a * b
        norm_a += a * a
        norm_b += b * b
    if norm_a <= 0 or norm_b <= 0:
        return 0.0
    return dot / (math.sqrt(norm_a) * math.sqrt(norm_b))


def score_candidates(
    query_face_emb: Optional[List[float]],
    query_voice_emb: Optional[List[float]],
    candidates: List[Dict],
    face_weight: float = 0.6,
    voice_weight: float = 0.4,
    topk: int = 5,
) -> List[Dict]:
    """Score and rank candidates using available modalities.

    Each candidate dict may contain keys: face_embedding, voice_embedding, id, full_name, meta.
    Returns list of dicts with added scores: score, face_score, voice_score.
    """
    scored: List[Dict] = []
    for cand in candidates:
        face_score = 0.0
        voice_score = 0.0
        weight_sum = 0.0
        if query_face_emb and cand.get("face_embedding"):
            face_score = cosine_similarity(query_face_emb, cand["face_embedding"])
            weight_sum += face_weight
        if query_voice_emb and cand.get("voice_embedding"):
            voice_score = cosine_similarity(query_voice_emb, cand["voice_embedding"])
            weight_sum += voice_weight
        if weight_sum == 0:
            # No comparable modality with this candidate, skip
            continue
        total_score = (face_score * face_weight + voice_score * voice_weight) / weight_sum
        scored.append({
            "id": cand.get("id"),
            "full_name": cand.get("full_name"),
            "meta": cand.get("meta", {}),
            "face_score": face_score,
            "voice_score": voice_score,
            "score": total_score,
        })

    scored.sort(key=lambda r: r["score"], reverse=True)
    return scored[:topk] if topk and topk > 0 else scored