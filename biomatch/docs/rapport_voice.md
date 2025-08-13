# Rapport module — Reconnaissance vocale

## Pipeline
1. Extraction audio depuis la vidéo (WAV 16 kHz PCM)
2. Prétraitement (normalisation implicite via `resemblyzer.preprocess_wav`)
3. Embedding du locuteur: modèle Resemblyzer (GE2E) -> vecteur spectral (256D)

## Paramètres clés
- Durée minimale utile: `voice.min_duration_seconds` ≈ 2–3 s
- Qualité micro/environnement: limiter bruit et réverbération

## Robustesse
- Résilient au bruit modéré, parle plus d’1–2 s
- Pas besoin de transcription (indépendant du texte)

## Limitations
- Mélange de locuteurs (diarisation non incluse par défaut)
- Musique de fond forte, forte réverbération

## Bonnes pratiques
- Extraire segments où la personne parle seule
- Éviter sons parasites (vent, musique)
- Ajuster la pondération voix vs. visage en fonction du contexte