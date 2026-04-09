import numpy as np
import soundfile as sf
from pathlib import Path


def normalize_audio(audio: np.ndarray, target_db: float = -3.0) -> np.ndarray:
    """Normaliza el audio a un nivel de decibelios objetivo."""
    rms = np.sqrt(np.mean(audio**2))
    if rms > 0:
        gain = 10 ** (target_db / 20) / rms
        return audio * gain
    return audio


def concatenate_audios(
    audio_paths: list,
    output_path: str,
    crossfade_ms: int = 20,
    sample_rate: int = 24000,
) -> None:
    """Concatena múltiples archivos de audio con crossfade."""
    audios = []
    for path in audio_paths:
        audio, _ = sf.read(path)
        audios.append(audio)

    # Aplicar crossfade en las uniones
    crossfade_samples = int(crossfade_ms * sample_rate / 1000)

    result = audios[0]
    for i in range(1, len(audios)):
        # Crossfade entre el final del anterior y el inicio del siguiente
        overlap_len = min(crossfade_samples, len(result), len(audios[i]))
        if overlap_len > 0:
            fade_out = np.linspace(1, 0, overlap_len)
            fade_in = np.linspace(0, 1, overlap_len)
            result[-overlap_len:] *= fade_out
            audios[i][:overlap_len] *= fade_in
        result = np.concatenate([result, audios[i]])

    sf.write(output_path, result, sample_rate)