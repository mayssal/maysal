# Rapport module — Reconnaissance faciale

## Pipeline
1. Prétraitement optionnel: amélioration du contraste (CLAHE) + débruitage léger
2. Détection du visage: MTCNN (seuil configurable `detection_threshold`)
3. Embedding: InceptionResnetV1 pré-entraîné sur VGGFace2 (512D)
4. Agrégation (vidéo): moyenne des embeddings sur frames échantillonnées

## Paramètres clés
- `face.detection_threshold` ≈ 0.90–0.99 selon bruit
- `video.sample_fps` et `video.max_frames` pour diversifier les poses/expressions
- Prétraitement `face.image_enhance` activé pour conditions difficiles

## Robustesse
- Multi-frames permet de lisser artefacts compression/flou
- CLAHE aide en basse luminosité

## Limitations
- Très fortes occultations ou rotations extrêmes
- Forte compression vidéo ou très basse résolution

## Bonnes pratiques
- Utiliser des images de référence nettes, frontales si possible
- Échantillonner plusieurs frames sur la référence vidéo
- Surveiller les distributions de similarité pour ajuster `min_confidence`