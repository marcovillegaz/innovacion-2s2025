# Documentación Técnica - Análisis de Texto con spaCy

## Descripción General

Este proyecto es una plantilla completa para analizar datos de texto tabulados provenientes de Google Forms utilizando técnicas de Procesamiento de Lenguaje Natural (NLP) con la biblioteca spaCy.

## Arquitectura del Proyecto

### Módulos Principales

#### 1. `config.py` - Configuración Central
Define todas las constantes y configuraciones del proyecto:
- Rutas de directorios
- Modelo de spaCy a utilizar
- Nombres de columnas por defecto
- Configuración de procesamiento y visualización

#### 2. `src/data_loader.py` - Carga y Procesamiento de Datos
Funciones principales:
- `load_data()`: Carga archivos CSV o Excel
- `get_text_column()`: Extrae columna de texto específica
- `clean_text()`: Limpieza básica de texto
- `preprocess_dataframe()`: Preprocesamiento completo del DataFrame
- `save_results()`: Exporta resultados en múltiples formatos

#### 3. `src/text_analyzer.py` - Análisis de Texto
Clase principal: `TextAnalyzer`

Métodos:
- `analyze_text()`: Análisis completo de un texto individual
- `analyze_batch()`: Procesamiento por lotes de múltiples textos
- `extract_entities()`: Extracción de entidades nombradas (NER)
- `get_top_words()`: Palabras más frecuentes con filtros de POS
- `get_sentiment_statistics()`: Estadísticas básicas del texto

#### 4. `src/visualizer.py` - Visualización de Resultados
Funciones de visualización:
- `plot_word_frequency()`: Gráfico de barras de frecuencias
- `create_wordcloud()`: Nube de palabras
- `plot_entity_distribution()`: Distribución de tipos de entidades
- `plot_text_statistics()`: Estadísticas individuales
- `plot_multiple_statistics()`: Panel múltiple de estadísticas
- `save_plot()`: Guardar visualizaciones

#### 5. `analyze.py` - Script Principal
Script ejecutable desde línea de comandos que orquesta todo el análisis:
1. Carga de datos
2. Preprocesamiento
3. Análisis NLP
4. Generación de visualizaciones
5. Exportación de resultados

## Flujo de Trabajo

```
┌─────────────────┐
│  Datos CSV/XLSX │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Carga de Datos │ (data_loader.load_data)
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Preprocesamiento│ (data_loader.preprocess_dataframe)
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Análisis spaCy  │ (TextAnalyzer)
├─────────────────┤
│ • Tokenización  │
│ • POS Tagging   │
│ • NER           │
│ • Lemmatización │
└────────┬────────┘
         │
         ├──────────────┬──────────────┐
         ▼              ▼              ▼
    ┌────────┐    ┌────────┐    ┌────────┐
    │Estadís │    │Entida  │    │Palabras│
    │ticas   │    │des     │    │Frecuen │
    └───┬────┘    └───┬────┘    └───┬────┘
         │            │              │
         └──────┬─────┴──────────────┘
                ▼
        ┌──────────────┐
        │Visualización │ (visualizer)
        └──────┬───────┘
               │
               ▼
        ┌──────────────┐
        │ Exportación  │ (CSV/PNG)
        └──────────────┘
```

## Características Técnicas

### Procesamiento de Texto

**spaCy** realiza:
- **Tokenización**: Separación del texto en tokens
- **Lematización**: Reducción de palabras a su forma base
- **POS Tagging**: Etiquetado de categorías gramaticales
- **NER**: Reconocimiento de entidades nombradas
- **Dependency Parsing**: Análisis de dependencias sintácticas

### Entidades Reconocidas (Modelo Español)

- **PER**: Personas
- **LOC**: Lugares
- **ORG**: Organizaciones
- **MISC**: Miscelánea

### Métricas Extraídas

Por cada texto:
- Número de tokens
- Número de oraciones
- Número de entidades nombradas
- Longitud promedio de palabras
- Frecuencia de palabras (total, sustantivos, verbos, adjetivos)

## Personalización

### Cambiar el Modelo de Idioma

```python
# En config.py
SPACY_MODEL = "en_core_web_sm"  # Para inglés
SPACY_MODEL = "es_core_news_md"  # Modelo español más grande
```

### Añadir Nuevas Métricas

Editar `src/text_analyzer.py`:

```python
def nueva_metrica(self, texts):
    resultados = []
    for doc in self.nlp.pipe(texts):
        # Tu análisis personalizado
        resultados.append(...)
    return resultados
```

### Personalizar Visualizaciones

Editar `src/visualizer.py`:

```python
def mi_visualizacion(data):
    plt.figure(figsize=(12, 6))
    # Tu código de visualización
    return plt.gcf()
```

## Formatos de Entrada Soportados

### CSV
```csv
Columna1,Columna2,TextoColumna
valor1,valor2,texto para analizar
```

### Excel
- `.xlsx` (Excel 2007+)
- `.xls` (Excel 97-2003)

## Formatos de Salida

### Datos
- **CSV**: Formato universal, compatible con Excel y herramientas de análisis
- **Excel**: Formato .xlsx con formato preservado
- **JSON**: Para integración con aplicaciones web

### Visualizaciones
- **PNG**: Imágenes de alta calidad (configurable DPI)

## Dependencias Principales

```
spacy>=3.7.0          # NLP core
pandas>=2.0.0         # Manipulación de datos
matplotlib>=3.7.0     # Visualización básica
seaborn>=0.12.0       # Visualización estadística
wordcloud>=1.9.0      # Nubes de palabras
jupyter>=1.0.0        # Análisis interactivo
tqdm>=4.65.0          # Barras de progreso
```

## Rendimiento

### Optimizaciones Implementadas

1. **Procesamiento por lotes**: `nlp.pipe()` es ~10x más rápido que procesar individualmente
2. **Configuración de batch_size**: Ajustable en `config.py`
3. **Límite de longitud de texto**: Previene problemas de memoria

### Recomendaciones

- Para <100 textos: Cualquier configuración funciona
- Para 100-1000 textos: Batch size de 50-100
- Para >1000 textos: Considerar modelo pequeño y batch size mayor

## Casos de Uso

1. **Análisis de Encuestas**: Procesar respuestas abiertas de Google Forms
2. **Análisis de Feedback**: Comentarios de clientes o estudiantes
3. **Investigación Cualitativa**: Análisis de entrevistas o grupos focales
4. **Monitoreo de Redes Sociales**: Análisis de menciones o comentarios
5. **Análisis de Documentos**: Procesamiento de textos académicos o técnicos

## Limitaciones

1. **Longitud de texto**: spaCy tiene límites de memoria para textos muy largos
2. **Idioma**: Requiere modelo específico del idioma
3. **Precisión de NER**: Depende del modelo y dominio específico
4. **Sentimiento**: No incluye análisis de sentimiento (puede añadirse)

## Extensiones Futuras

- [ ] Análisis de sentimiento con TextBlob o VADER
- [ ] Clasificación de temas con LDA o BERTopic
- [ ] Análisis de similitud entre textos
- [ ] Exportación a formatos de reporte (PDF)
- [ ] Dashboard interactivo con Streamlit o Dash
- [ ] Soporte para múltiples idiomas simultáneos
- [ ] Análisis temporal de tendencias

## Solución de Problemas

### Error: "Can't find model"
```bash
python -m spacy download es_core_news_sm
```

### Error: "Memory error"
Reducir `BATCH_SIZE` en `config.py` o usar modelo más pequeño

### Error: "Encoding issues"
El `data_loader` intenta automáticamente UTF-8 y Latin-1

### Visualizaciones no se ven
Verificar que matplotlib backend está configurado correctamente

## Referencias

- [spaCy Documentation](https://spacy.io/)
- [Pandas Documentation](https://pandas.pydata.org/)
- [Matplotlib Documentation](https://matplotlib.org/)
- [Natural Language Processing with Python](https://www.nltk.org/book/)
