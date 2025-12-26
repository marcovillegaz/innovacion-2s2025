# Guía de Inicio Rápido - Análisis de Texto con spaCy

## Instalación Rápida

### Opción 1: Script automático (Linux/Mac)

```bash
chmod +x setup.sh
./setup.sh
```

### Opción 2: Manual

```bash
# 1. Crear entorno virtual
python -m venv venv

# 2. Activar entorno virtual
# En Linux/Mac:
source venv/bin/activate
# En Windows:
venv\Scripts\activate

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Descargar modelo de spaCy
python -m spacy download es_core_news_sm
```

## Primer Análisis

### 1. Con el ejemplo incluido

```bash
python analyze.py data/ejemplo_formulario.csv --text-column "Respuesta"
```

### 2. Con tus propios datos

```bash
python analyze.py ruta/a/tu/archivo.csv --text-column "NombreDeTuColumna"
```

### 3. Con Jupyter Notebook

```bash
jupyter notebook notebooks/analisis_interactivo.ipynb
```

## Estructura de tu CSV

Tu archivo debe tener al menos una columna con texto. Ejemplo:

```csv
Marca temporal,Nombre,Respuesta
2024-01-15 10:30:00,Juan,Mi respuesta aquí...
2024-01-15 11:00:00,María,Otra respuesta...
```

## Configuración Básica

Edita `config.py` para cambiar:

```python
# Modelo de spaCy (español por defecto)
SPACY_MODEL = "es_core_news_sm"

# Nombre de la columna de texto en tu CSV
TEXT_COLUMN = "Respuesta"
```

## Resultados

Todos los resultados se guardan en la carpeta `output/`:
- Archivos CSV con estadísticas
- Gráficos PNG con visualizaciones
- Archivos de entidades nombradas

## Problemas Comunes

### Error: "Can't find model 'es_core_news_sm'"

Solución:
```bash
python -m spacy download es_core_news_sm
```

### Error: "Column 'X' not found"

Solución: Verifica el nombre exacto de tu columna y úsalo con `--text-column`

```bash
python analyze.py tu_archivo.csv --text-column "NombreExacto"
```

### Para datos en inglés

```bash
# 1. Descargar modelo en inglés
python -m spacy download en_core_web_sm

# 2. Cambiar config.py
# SPACY_MODEL = "en_core_web_sm"
```

## Próximos Pasos

1. Revisa los resultados en `output/`
2. Explora el notebook interactivo
3. Personaliza las visualizaciones en `src/visualizer.py`
4. Añade tus propias métricas en `src/text_analyzer.py`

## Ayuda

Para ver todas las opciones:
```bash
python analyze.py --help
```
