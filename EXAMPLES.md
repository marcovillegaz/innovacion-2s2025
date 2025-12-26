# Ejemplos de Uso

Este documento proporciona ejemplos prácticos de cómo usar el proyecto para diferentes casos de uso.

## Ejemplo 1: Análisis Básico de Encuesta

### Datos de entrada (encuesta.csv)
```csv
Marca temporal,Nombre,Respuesta
2024-01-15 10:00:00,Usuario1,Me gusta mucho la plataforma
2024-01-15 11:00:00,Usuario2,El servicio es excelente
```

### Comando
```bash
python analyze.py encuesta.csv --text-column "Respuesta" --output-prefix "encuesta_resultados"
```

### Resultados
- `output/encuesta_resultados_statistics.csv`
- `output/encuesta_resultados_word_frequency.png`
- `output/encuesta_resultados_wordcloud.png`

## Ejemplo 2: Análisis de Múltiples Columnas

Si tienes varias columnas de texto que quieres analizar:

```python
import pandas as pd
from src.data_loader import load_data, preprocess_dataframe
from src.text_analyzer import TextAnalyzer

# Cargar datos
df = load_data("datos.csv")

# Analizar cada columna
analyzer = TextAnalyzer()
columnas = ["Pregunta1", "Pregunta2", "Pregunta3"]

for col in columnas:
    texts = df[col].dropna().tolist()
    top_words = analyzer.get_top_words(texts, n=20)
    print(f"\nTop palabras en {col}:")
    for word, count in top_words[:10]:
        print(f"  {word}: {count}")
```

## Ejemplo 3: Comparar Respuestas Entre Grupos

```python
import pandas as pd
from src.data_loader import load_data
from src.text_analyzer import TextAnalyzer
from src.visualizer import plot_word_frequency
import matplotlib.pyplot as plt

# Cargar datos
df = load_data("datos.csv")
analyzer = TextAnalyzer()

# Separar por grupo
grupo_a = df[df['Grupo'] == 'A']['Respuesta'].tolist()
grupo_b = df[df['Grupo'] == 'B']['Respuesta'].tolist()

# Analizar cada grupo
words_a = analyzer.get_top_words(grupo_a, n=20)
words_b = analyzer.get_top_words(grupo_b, n=20)

# Visualizar comparación
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))

# Grupo A
words, counts = zip(*words_a[:10])
ax1.barh(range(len(words)), counts)
ax1.set_yticks(range(len(words)))
ax1.set_yticklabels(words)
ax1.set_title('Grupo A - Palabras más frecuentes')
ax1.invert_yaxis()

# Grupo B
words, counts = zip(*words_b[:10])
ax2.barh(range(len(words)), counts)
ax2.set_yticks(range(len(words)))
ax2.set_yticklabels(words)
ax2.set_title('Grupo B - Palabras más frecuentes')
ax2.invert_yaxis()

plt.tight_layout()
plt.savefig('output/comparacion_grupos.png')
```

## Ejemplo 4: Análisis Temporal

```python
import pandas as pd
from src.data_loader import load_data
from src.text_analyzer import TextAnalyzer
import matplotlib.pyplot as plt

# Cargar datos con timestamp
df = load_data("datos.csv")
df['Marca temporal'] = pd.to_datetime(df['Marca temporal'])
df['Mes'] = df['Marca temporal'].dt.to_period('M')

analyzer = TextAnalyzer()

# Analizar por mes
resultados_mensuales = {}
for mes, grupo in df.groupby('Mes'):
    texts = grupo['Respuesta'].tolist()
    stats = analyzer.get_sentiment_statistics(texts)
    resultados_mensuales[str(mes)] = {
        'num_respuestas': len(texts),
        'promedio_tokens': stats['num_tokens'].mean(),
        'promedio_oraciones': stats['num_sentences'].mean()
    }

# Convertir a DataFrame y visualizar
df_temporal = pd.DataFrame(resultados_mensuales).T
df_temporal.plot(kind='line', figsize=(12, 6))
plt.title('Tendencias temporales')
plt.xlabel('Mes')
plt.ylabel('Valor')
plt.tight_layout()
plt.savefig('output/tendencias_temporales.png')
```

## Ejemplo 5: Filtrar por Entidades Específicas

```python
from src.data_loader import load_data
from src.text_analyzer import TextAnalyzer

# Cargar y analizar
df = load_data("datos.csv")
texts = df['Respuesta'].tolist()
analyzer = TextAnalyzer()

# Extraer entidades
entities_df = analyzer.extract_entities(texts)

# Filtrar por tipo de entidad
organizaciones = entities_df[entities_df['label'] == 'ORG']
personas = entities_df[entities_df['label'] == 'PER']
lugares = entities_df[entities_df['label'] == 'LOC']

print(f"Organizaciones mencionadas: {organizaciones['entity'].unique()}")
print(f"Personas mencionadas: {personas['entity'].unique()}")
print(f"Lugares mencionados: {lugares['entity'].unique()}")

# Encontrar textos que mencionan una entidad específica
textos_con_universidad = entities_df[
    entities_df['entity'].str.contains('Universidad', case=False)
]['text_id'].unique()

print(f"\nTextos que mencionan 'Universidad': {len(textos_con_universidad)}")
for idx in textos_con_universidad[:5]:
    print(f"  - {df.iloc[idx]['Respuesta'][:100]}...")
```

## Ejemplo 6: Exportar a Diferentes Formatos

```python
from src.data_loader import load_data, save_results
from src.text_analyzer import TextAnalyzer
import pandas as pd

# Realizar análisis
df = load_data("datos.csv")
texts = df['Respuesta'].tolist()
analyzer = TextAnalyzer()

top_words = analyzer.get_top_words(texts, n=50)
words_df = pd.DataFrame(top_words, columns=['palabra', 'frecuencia'])

# Guardar en diferentes formatos
save_results(words_df, 'palabras_frecuentes', format='csv')
save_results(words_df, 'palabras_frecuentes', format='xlsx')
save_results(words_df, 'palabras_frecuentes', format='json')

print("Resultados exportados en CSV, Excel y JSON")
```

## Ejemplo 7: Análisis Solo de Sustantivos o Verbos

```python
from src.data_loader import load_data
from src.text_analyzer import TextAnalyzer
from src.visualizer import plot_word_frequency
import matplotlib.pyplot as plt

df = load_data("datos.csv")
texts = df['Respuesta'].tolist()
analyzer = TextAnalyzer()

# Análisis por categoría gramatical
sustantivos = analyzer.get_top_words(texts, n=30, pos_filter=['NOUN'])
verbos = analyzer.get_top_words(texts, n=30, pos_filter=['VERB'])
adjetivos = analyzer.get_top_words(texts, n=30, pos_filter=['ADJ'])

# Visualizar cada categoría
fig, axes = plt.subplots(1, 3, figsize=(18, 6))

for ax, words, title in zip(axes, 
                            [sustantivos, verbos, adjetivos],
                            ['Sustantivos', 'Verbos', 'Adjetivos']):
    w, c = zip(*words[:15])
    ax.barh(range(len(w)), c)
    ax.set_yticks(range(len(w)))
    ax.set_yticklabels(w)
    ax.set_title(f'{title} más frecuentes')
    ax.invert_yaxis()

plt.tight_layout()
plt.savefig('output/analisis_pos.png')
```

## Ejemplo 8: Análisis Personalizado con Jupyter

Crea un nuevo notebook y ejecuta:

```python
# Celda 1: Importaciones
import sys
sys.path.insert(0, '..')
from src.data_loader import load_data
from src.text_analyzer import TextAnalyzer
import pandas as pd
import matplotlib.pyplot as plt

# Celda 2: Cargar datos
df = load_data("../data/ejemplo_formulario.csv")
display(df.head())

# Celda 3: Análisis personalizado
analyzer = TextAnalyzer()
texts = df['Respuesta'].tolist()

# Tu análisis aquí...
for i, text in enumerate(texts[:3]):
    result = analyzer.analyze_text(text)
    print(f"\n--- Texto {i+1} ---")
    print(f"Texto: {text[:100]}...")
    print(f"Tokens: {result['num_tokens']}")
    print(f"Entidades: {result['entities']}")
```

## Consejos Prácticos

1. **Para grandes volúmenes de datos**: Aumenta `BATCH_SIZE` en `config.py`
2. **Para análisis rápido**: Usa el modelo pequeño (`es_core_news_sm`)
3. **Para mayor precisión**: Usa el modelo grande (`es_core_news_lg`)
4. **Para datos en inglés**: Cambia `SPACY_MODEL = "en_core_web_sm"`
5. **Para conservar memoria**: Procesa en lotes pequeños

## Solución de Problemas Comunes

### Problema: "Out of memory"
```python
# Reducir tamaño de lote
# En config.py
BATCH_SIZE = 10  # en lugar de 50
```

### Problema: Codificación incorrecta
```python
# Especificar codificación
df = load_data("datos.csv", encoding='latin-1')
```

### Problema: Columna no encontrada
```python
# Listar columnas disponibles
df = load_data("datos.csv")
print(df.columns.tolist())
```
