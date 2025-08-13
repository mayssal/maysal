from app.recognition.matching import cosine_similarity, score_candidates


def test_cosine_similarity_basic():
    a = [1.0, 0.0]
    b = [1.0, 0.0]
    c = [0.0, 1.0]
    assert abs(cosine_similarity(a, b) - 1.0) < 1e-6
    assert abs(cosine_similarity(a, c) - 0.0) < 1e-6


def test_score_candidates_ranking():
    query = [1.0, 0.0]
    candidates = [
        {"id": 1, "full_name": "A", "face_embedding": [0.9, 0.1], "voice_embedding": []},
        {"id": 2, "full_name": "B", "face_embedding": [0.0, 1.0], "voice_embedding": []},
    ]
    results = score_candidates(query_face_emb=query, query_voice_emb=None, candidates=candidates, topk=2)
    assert len(results) == 2
    assert results[0]["id"] == 1