# Análisis de Texto con spaCy - Google Forms

Repositorio del curso de innovación y emprendimiento 2s2025 dictado a estudiantes de Ingeniería en Geografía de la USACH

## 📋 Descripción

Este proyecto proporciona una plantilla completa para analizar datos de texto tabulados provenientes de Google Forms utilizando la biblioteca spaCy de Python. Incluye herramientas para procesamiento de lenguaje natural (NLP), extracción de entidades, análisis de frecuencia de palabras y visualización de resultados.

## 🚀 Características

- **Carga de datos**: Soporte para CSV y Excel
- **Análisis NLP**: Procesamiento de texto con spaCy
- **Extracción de entidades**: Identificación automática de personas, lugares, organizaciones, etc.
- **Análisis de frecuencias**: Palabras, sustantivos, verbos y adjetivos más comunes
- **Visualizaciones**: Gráficos de barras, nubes de palabras, distribuciones estadísticas
- **Exportación**: Resultados en CSV, Excel o JSON
- **Notebook interactivo**: Análisis exploratorio con Jupyter

## 📁 Estructura del Proyecto

```
.
├── data/                      # Archivos de datos (CSV, Excel)
│   └── ejemplo_formulario.csv # Ejemplo de datos de Google Forms
├── src/                       # Código fuente
│   ├── __init__.py
│   ├── data_loader.py        # Utilidades para cargar y limpiar datos
│   ├── text_analyzer.py      # Análisis de texto con spaCy
│   └── visualizer.py         # Funciones de visualización
├── notebooks/                 # Jupyter notebooks
│   └── analisis_interactivo.ipynb
├── output/                    # Resultados del análisis
├── config.py                  # Configuración del proyecto
├── analyze.py                 # Script principal de análisis
├── requirements.txt           # Dependencias de Python
└── README.md                  # Este archivo
```

## 🔧 Instalación

### 1. Clonar el repositorio

```bash
git clone https://github.com/marcovillegaz/innovaci-n-2s2025.git
cd innovaci-n-2s2025
```

### 2. Crear un entorno virtual (recomendado)

```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Descargar el modelo de spaCy

Para español:
```bash
python -m spacy download es_core_news_sm
```

Para inglés:
```bash
python -m spacy download en_core_web_sm
```

Para modelos más precisos (mayor tamaño):
```bash
python -m spacy download es_core_news_md  # Modelo mediano
python -m spacy download es_core_news_lg  # Modelo grande
```

## 💻 Uso

### Opción 1: Script de línea de comandos

```bash
python analyze.py data/ejemplo_formulario.csv --text-column "Respuesta" --output-prefix "mi_analisis"
```

Parámetros:
- `input_file`: Ruta al archivo CSV o Excel (obligatorio)
- `--text-column` o `-c`: Nombre de la columna con texto (opcional, por defecto usa config.py)
- `--output-prefix` o `-o`: Prefijo para archivos de salida (opcional, por defecto "analysis")

### Opción 2: Jupyter Notebook

```bash
jupyter notebook notebooks/analisis_interactivo.ipynb
```

El notebook proporciona un análisis paso a paso e interactivo.

### Opción 3: Usar como biblioteca

```python
from src.data_loader import load_data, preprocess_dataframe
from src.text_analyzer import TextAnalyzer
from src.visualizer import plot_word_frequency

# Cargar datos
df = load_data("data/ejemplo_formulario.csv")
df_clean = preprocess_dataframe(df, text_column="Respuesta")

# Analizar
analyzer = TextAnalyzer(model_name="es_core_news_sm")
texts = df_clean["Respuesta"].tolist()
top_words = analyzer.get_top_words(texts, n=30)

# Visualizar
fig = plot_word_frequency(top_words)
```

## 📊 Resultados

El análisis genera los siguientes archivos en el directorio `output/`:

- `*_statistics.csv`: Estadísticas por texto (tokens, oraciones, entidades, etc.)
- `*_entities.csv`: Todas las entidades nombradas encontradas
- `*_top_words.csv`: Palabras más frecuentes
- `*_top_nouns.csv`: Sustantivos más frecuentes
- `*_top_verbs.csv`: Verbos más frecuentes
- `*_word_frequency.png`: Gráfico de frecuencia de palabras
- `*_wordcloud.png`: Nube de palabras
- `*_entities.png`: Distribución de tipos de entidades
- `*_statistics.png`: Panel con múltiples estadísticas

## ⚙️ Configuración

Edita el archivo `config.py` para personalizar:

- Modelo de spaCy a utilizar
- Nombres de columnas predeterminados
- Tamaños de lotes para procesamiento
- Configuración de visualización
- Formato de exportación

## 📝 Formato de Datos

Los datos deben estar en formato CSV o Excel con al menos una columna de texto. Ejemplo de estructura de Google Forms:

| Marca temporal | Nombre | Correo electrónico | Respuesta |
|----------------|--------|-------------------|-----------|
| 2024-01-15 10:30:00 | Juan Pérez | juan@example.com | Texto de respuesta... |

## 🛠️ Personalización

### Cambiar el idioma del análisis

Modifica `config.py`:

```python
SPACY_MODEL = "en_core_web_sm"  # Para inglés
```

### Añadir nuevas visualizaciones

Agrega funciones en `src/visualizer.py`:

```python
def mi_nueva_visualizacion(data):
    # Tu código aquí
    pass
```

## 📚 Recursos

- [Documentación de spaCy](https://spacy.io/)
- [Modelos de spaCy para español](https://spacy.io/models/es)
- [Pandas Documentation](https://pandas.pydata.org/)
- [Matplotlib Gallery](https://matplotlib.org/stable/gallery/)

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor:

1. Fork el repositorio
2. Crea una rama para tu función (`git checkout -b feature/nueva-funcion`)
3. Commit tus cambios (`git commit -am 'Añadir nueva función'`)
4. Push a la rama (`git push origin feature/nueva-funcion`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto es parte del curso de Innovación y Emprendimiento de la USACH.

## ✉️ Contacto

Para preguntas sobre el proyecto, contacta al instructor del curso o abre un issue en GitHub.
