import re
import numpy as np
import soundfile as sf
from TTS.api import TTS
from pathlib import Path
from typing import List, Optional


class XTTSVoiceCloner:
    """Clonador de voz usando XTTS-v2 con manejo profesional de errores."""

    def __init__(
        self,
        model_name: str = "tts_models/multilingual/multi-dataset/xtts_v2",
        device: str = "cuda",
        speaker_wavs: Optional[List[str]] = None,
    ):
        """
        Inicializa el modelo XTTS.

        Args:
            model_name: Nombre del modelo TTS
            device: 'cuda' o 'cpu'
            speaker_wavs: Lista de rutas a audios de referencia para clonar la voz
        """
        self.tts = TTS(model_name=model_name)
        self.device = device
        self.speaker_wavs = speaker_wavs or ["data/reference_audio/train1.wav"]
        self.tts.to(device)

    @staticmethod
    def split_text(text: str, max_length: int = 500) -> List[str]:
        """
        Divide un texto largo en fragmentos respetando puntuación.

        Args:
            text: Texto a dividir
            max_length: Longitud máxima aproximada de cada fragmento

        Returns:
            Lista de fragmentos de texto
        """
        # Divide por puntos, exclamaciones e interrogaciones
        raw_chunks = re.split(r'(?<=[.!?]) +', text)

        # Une fragmentos pequeños para evitar cortes muy cortos
        chunks = []
        current_chunk = ""
        for chunk in raw_chunks:
            if len(current_chunk) + len(chunk) < max_length:
                current_chunk += " " + chunk if current_chunk else chunk
            else:
                if current_chunk:
                    chunks.append(current_chunk.strip())
                current_chunk = chunk
        if current_chunk:
            chunks.append(current_chunk.strip())
        return chunks

    @staticmethod
    def apply_fade(audio: np.ndarray, fade_len: int = 500) -> np.ndarray:
        """Aplica fade in/out para evitar clics entre fragmentos."""
        fade_in = np.linspace(0, 1, fade_len)
        fade_out = np.linspace(1, 0, fade_len)
        audio[:fade_len] *= fade_in
        audio[-fade_len:] *= fade_out
        return audio

    def generate_audio(
        self,
        text: str,
        output_path: str,
        temperature: float = 0.7,
        top_p: float = 0.85,
        repetition_penalty: float = 2.2,
        speed: float = 1.0,
        language: str = "es",
        fade_len: int = 500,
    ) -> None:
        """
        Genera audio a partir de un texto usando la voz clonada.

        Args:
            text: Texto a convertir en audio
            output_path: Ruta donde guardar el archivo .wav
            temperature: Creatividad de la voz (0-1)
            top_p: Nucleus sampling
            repetition_penalty: Penalización por repetición
            speed: Velocidad del habla (0.5-2.0)
            language: Código de idioma ('es', 'en', 'fr', etc.)
            fade_len: Longitud del fade entre fragmentos
        """
        # Validaciones
        if not text:
            raise ValueError("El texto no puede estar vacío")
        if not self.speaker_wavs:
            raise ValueError("Se necesita al menos un audio de referencia")

        # Dividir texto
        chunks = self.split_text(text)
        print(f"Generando {len(chunks)} fragmentos de audio...")

        # Generar audio por fragmentos
        audios = []
        for i, chunk in enumerate(chunks):
            print(f"Fragmento {i+1}/{len(chunks)}: {chunk[:50]}...")
            try:
                wav = self.tts.tts(
                    text=chunk,
                    speaker_wav=self.speaker_wavs,
                    language=language,
                    temperature=temperature,
                    top_p=top_p,
                    repetition_penalty=repetition_penalty,
                    speed=speed,
                )
                audios.append(self.apply_fade(np.array(wav), fade_len))
            except Exception as e:
                print(f"Error en fragmento {i+1}: {e}")
                # Continúa con los demás fragmentos
                continue

        if not audios:
            raise RuntimeError("No se pudo generar ningún fragmento de audio")

        # Unir y normalizar
        final_audio = np.concatenate(audios)
        final_audio = final_audio / np.max(np.abs(final_audio))

        # Guardar
        output_path_obj = Path(output_path)
        output_path_obj.parent.mkdir(parents=True, exist_ok=True)
        sf.write(str(output_path_obj), final_audio, 24000)
        print(f"Audio guardado en {output_path}")


# Ejemplo de uso directo
if __name__ == "__main__":
    # Leer el texto desde un archivo o variable
    texto_largo = """
    Nos ubicamos en la costa caribe colombiana, y era el año 1928... Allí, en Ciénaga, el banano era el gran motor económico gracias a la United Fruit Company...
    """  # (aquí iría tu texto completo)

    # Crear clonador de voz
    cloner = XTTSVoiceCloner(
        speaker_wavs=[
            "data/reference_audio/train1.wav",
            "data/reference_audio/train2.wav",
            "data/reference_audio/train3.wav",
        ]
    )

    # Generar audio
    cloner.generate_audio(
        text=texto_largo,
        output_path="data/output/output_pro.wav",
        temperature=0.7,
        top_p=0.85,
        repetition_penalty=2.2,
    )