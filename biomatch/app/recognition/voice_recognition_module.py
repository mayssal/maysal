from typing import List, Optional


class VoiceRecognizer:
    def __init__(self):
        from resemblyzer import VoiceEncoder
        self.encoder = VoiceEncoder()

    def embed_audio_file(self, wav_path: str) -> Optional[List[float]]:
        try:
            from resemblyzer import preprocess_wav
            wav = preprocess_wav(wav_path)
            if wav is None or len(wav) == 0:
                return None
            emb = self.encoder.embed_utterance(wav)
            return emb.astype(float).tolist()
        except Exception:
            return None