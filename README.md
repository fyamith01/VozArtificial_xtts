# VozArtificial_xtts

Sistema de síntesis de voz basado en XTTS (eXtended Text-to-Speech) para generar audio de alta calidad a partir de texto. Este proyecto permite crear voces sintéticas personalizadas utilizando modelos de aprendizaje profundo.

## Características

- **Síntesis de voz de alta calidad**: Utiliza el modelo XTTS de Coqui TTS
- **Voces personalizadas**: Entrenamiento con audios de referencia
- **Procesamiento de audio**: Utilidades para manipulación y optimización de audio
- **Ejecución en Colab**: Notebook optimizado para Google Colab con GPU
- **CI/CD**: Pipelines automatizados para integración continua y despliegue

## Requisitos

- **Python**: 3.10
- **GPU**: Recomendado para entrenamiento (NVIDIA con CUDA)
- **Dependencias**: Ver `requirements.txt`

### Dependencias principales
- PyTorch
- Coqui TTS
- NumPy, SciPy
- Jupyter Notebook

## Instalación

1. **Clona el repositorio**:
   ```bash
   git clone https://github.com/tu-usuario/VozArtificial_xtts.git
   cd VozArtificial_xtts
   ```

2. **Instala las dependencias**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Verifica la instalación**:
   ```bash
   python -c "import src.tts_engine; print('Instalación exitosa')"
   ```

## Estructura del proyecto

```
├── .github/
│   └── workflows/           # Pipelines CI/CD
│       ├── ci.yml          # Integración continua
│       ├── deploy.yml      # Despliegue (validación)
│       └── guard-main.yml  # Protección de rama main
├── notebooks/
│   ├── xtts_demo.ipynb     # Demo interactiva del sistema TTS
│   └── Prueba_ejecutar-desde-colab-GPU.ipynb  # Ejecución completa en Colab
├── src/
│   ├── __init__.py
│   ├── tts_engine.py       # Motor principal de TTS
│   └── audio_utils.py      # Utilidades de procesamiento de audio
├── data/
│   ├── reference_audio/    # Audios de referencia para entrenamiento
│   │   ├── train1.wav
│   │   ├── train2.wav
│   │   └── train3.wav
│   └── output/             # Salida de audios generados
├── requirements.txt        # Dependencias Python
├── .gitignore             # Archivos ignorados por Git
└── README.md              # Este archivo
```

## Uso

### Uso básico desde código Python

```python
from src.tts_engine import TTSEngine

# Inicializar el motor
engine = TTSEngine()

# Generar audio
texto = "Hola, este es un ejemplo de síntesis de voz."
audio_path = engine.generate_audio(texto, output_path="data/output/ejemplo.wav")
```

### Uso desde línea de comandos

```bash
python -c "from src.tts_engine import TTSEngine; engine = TTSEngine(); engine.generate_audio('Texto de ejemplo')"
```

## Uso en Google Colab (Recomendado)

Para una experiencia óptima, especialmente si no tienes GPU local, utiliza el notebook `Prueba_ejecutar-desde-colab-GPU.ipynb`.

### Pasos para usar en Colab:

1. **Abre Google Colab**: Ve a [colab.research.google.com](https://colab.research.google.com)

2. **Sube el notebook**:
   - Haz clic en "Archivo" → "Subir notebook"
   - Selecciona `notebooks/Prueba_ejecutar-desde-colab-GPU.ipynb`

3. **Prepara los archivos de audio**:
   - Los archivos `.wav` de referencia (train1.wav, train2.wav, train3.wav) deben trasladarse a la carpeta temporal de Colab
   - En Colab, crea una carpeta `temp_audio/` y sube los archivos allí

4. **Configura el entorno**:
   - Asegúrate de que Colab esté usando GPU: "Entorno de ejecución" → "Cambiar tipo de entorno de ejecución" → "GPU"
   - Ejecuta las celdas del notebook en orden

5. **Ejecuta el flujo completo**:
   - El notebook contiene todo el flujo de trabajo: instalación de dependencias, carga de modelos, entrenamiento y generación de audio
   - Solo necesitas ejecutar las celdas secuencialmente

### Ventajas de usar Colab:
- GPU gratuita disponible
- No requiere instalación local
- Entorno preconfigurado
- Fácil compartir y colaboración

## 🔧 Desarrollo

### Ejecutar pruebas locales

```bash
# Verificar sintaxis
flake8 src/ --max-line-length=100

# Verificar imports
python -c "import src.tts_engine; import src.audio_utils"
```

### Contribuir

1. Crea una rama desde `develop`
2. Realiza tus cambios
3. Crea un Pull Request hacia `main`
4. Espera aprobación (solo el administrador puede mergear)

## Notas importantes

- **Rama protegida**: La rama `main` está protegida. Todos los cambios deben hacerse mediante Pull Requests
- **CI/CD**: Los workflows de GitHub Actions validan automáticamente el código en cada PR
- **GPU requerida**: Para entrenamiento efectivo, se recomienda GPU con al menos 8GB VRAM
- **Modelos grandes**: Los modelos XTTS pueden ser de varios GB, asegúrate de tener espacio suficiente

## Licencia

Este proyecto está bajo la Licencia MIT. Ver archivo `LICENSE` para más detalles.

## Soporte

Si tienes problemas:
1. Revisa los issues existentes en GitHub
2. Crea un nuevo issue con detalles del error
3. Incluye información sobre tu entorno (Python version, GPU, etc.)

---

**Desarrollado para democratizar el acceso a tecnología de síntesis de voz**