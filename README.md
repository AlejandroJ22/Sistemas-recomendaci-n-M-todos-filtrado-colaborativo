# Sistemas de recomendación - Filtrado Colaborativo

Este es un sistema de recomendación basado en filtrado colaborativo que predice calificaciones faltantes en una matriz de utilidad de usuarios e ítems. El sistema soporta diversas métricas de similaridad y tipos de predicciones, y está diseñado como una aplicación de línea de comandos.

## Funciones
### leer_matriz_utilidad(fichero)
Lee la matriz de utilidad desde un archivo `.txt`, así como los valores mínimo y máximo de las calificaciones. La matriz leída puede contener valores faltantes representados por `'-'`.
#### Parámetros
- `fichero` (string): ruta del fichero con la matriz de utilidad
#### Retorna
- `np.array`: Matriz de utilidad leída.
- `min_val`, `max_val`: Valores mínimo y máximo de la matriz.

### pearson_correlation(usuario1, usuario2)
Calcula la Correlación de Pearson entre dos usuarios, considerando solo los ítems comunes.
#### Parámetros:
- `usuario1`, `usuario2` (np.array): Vectores de calificaciones de los usuarios.
#### Retorna:
- `float` : Valor de la correlación de Pearson (0 si no hay ítems comunes).

### cosine_similarity(usuario1, usuario2)
Calcula la similitud coseno entre dos usuarios en base a los ítems comunes.

#### Parámetros:
- `usuario1`, `usuario2` (np.array): Vectores de calificaciones de los usuarios.
#### Retorna:
- `float`: Valor de la similitud coseno (0 si no hay ítems comunes).

### euclidean_distance(usuario1, usuario2)
Calcula la distancia Euclídea entre dos usuarios y la convierte en un valor de similitud entre 0 y 1.

#### Parámetros:
- `usuario1`, `usuario2` (np.array): Vectores de calificaciones de los usuarios.
#### Retorna:
- `float`: Valor de la similitud basada en la distancia Euclídea (0 si no hay ítems comunes).


#### calcular_similaridad(usuario1, usuario2, metrica)
Calcula la similaridad entre dos usuarios según la métrica especificada.
#### Parámetros:
- `usuario1`, `usuario2` (np.array): Vectores de calificaciones de los usuarios.
- `metrica` (str): Métrica de similaridad (pearson, coseno o euclidean).
#### Retorna:
- `float`: Valor de la similaridad calculada.


### mostrar_metricas(matriz, metrica)
Calcula y muestra la similaridad entre todos los pares de usuarios en la matriz utilizando la métrica seleccionada.
#### Parámetros:
- `matriz` (np.array): Matriz de utilidad.
- `metrica` (str): Métrica de similaridad.
#### Retorna:
- `list`: Lista de resultados de similaridad para cada par de usuarios.

### obtener_vecinos(matriz, idx, metrica, num_vecinos)
Obtiene los vecinos más cercanos de un usuario según la métrica y el número de vecinos especificados.
#### Parámetros:
- `matriz` (np.array): Matriz de utilidad.
- `idx` (int): Índice del usuario para quien se buscan vecinos.
- `metrica` (str): Métrica de similaridad.
- `num_vecinos` (int): Número de vecinos a considerar.
#### Retorna:
- `list`: Lista de vecinos y sus similitudes.

### predecir_simple(matriz, usuario_idx, item_idx, vecinos)
Predice el valor de un ítem faltante usando una media ponderada de las calificaciones de los vecinos.
#### Parámetros:
- `matriz` (np.array): Matriz de utilidad.
- `usuario_idx` (int): Índice del usuario para quien se hace la predicción.
- `item_idx` (int): Índice del ítem a predecir.
- `vecinos` (list): Lista de vecinos y sus similitudes.
#### Retorna:
- `float`: Predicción calculada.

### predecir_con_media(matriz, usuario_idx, item_idx, vecinos)
Predice el valor de un ítem faltante ajustando las calificaciones de los vecinos en función de sus medias.
#### Parámetros:
- `matriz` (np.array): Matriz de utilidad.
- `usuario_idx` (int): Índice del usuario para quien se hace la predicción.
- `item_idx` (int): Índice del ítem a predecir.
- `vecinos` (list): Lista de vecinos y sus similitudes.
#### Retorna:
- `float`: Predicción calculada.

### predecir_matriz(matriz, metrica, num_vecinos, tipo_prediccion)
Realiza predicciones para todos los ítems faltantes en la matriz de utilidad y guarda las predicciones realizadas.
#### Parámetros:
- `matriz` (np.array): Matriz de utilidad.
- `metrica` (str): Métrica de similaridad.
- `num_vecinos` (int): Número de vecinos a considerar.
- `tipo_prediccion` (str): Tipo de predicción (simple o media).
#### Retorna:
- `np.array`: Matriz con las predicciones incluidas.
- `list`: Lista de predicciones realizadas.

### imprimir_matriz(matriz)
Imprime la matriz con un formato adecuado.
#### Parámetros:
- `matriz` (np.array): Matriz a imprimir.

### guardar_matriz(fichero_salida, matriz, min_val, max_val, metricas, predicciones_hechas, matriz_predicha)
Guarda en un archivo la matriz predicha, junto con las métricas y predicciones calculadas.
#### Parámetros:
- `fichero_salida` (str): Ruta del archivo de salida.
- `matriz` (np.array): Matriz original de utilidad.
- `min_val`, `max_val` (float): Valores mínimo y máximo de calificación.
- `metricas` (list): Lista de métricas calculadas.
- `predicciones_hechas` (list): Lista de predicciones realizadas.
- `matriz_predicha` (np.array): Matriz con las predicciones incluidas.


## Instalación
1. Clona el repositorio de tu máquina local:
```bash
git clone https://github.com/ULL-ESIT-LPP-2425/05-programacion-estructurada-oscar-navarro-mesa-alu0101504094.git
```
2. Instala las dependencias necesarias, que son `numpy`:
```bash
pip install numpy
```

## Uso
El sistema se ejecuta desde línea de comandos. Debes especificar la ruta al archivo con la matriz de utilidad, la métrica de similaridad a utilizar, el número de vecinos y el tipo de predicción.

### Ejemplo de ejecución
```bash
python3 sistema_recomendacion.py matriz_utilidad.txt --metrica pearson --vecinos 5 --prediccion simple
```

### Argumentos
- `Fichero`: Ruta al archivo `.txt` que contiene la matriz de utilidad.
- `--metrica`: Métrica de similaridad a utilizar (`pearson`, `cosine`, `euclidean`).
- `--vecinos`: Número de vecinos más cercanos a considerar.
- `--prediccion`: Tipo de predicción a realizar (`simple`, `media`).

### Ejemplo de salida
Al ejecutar el sistema con el archivo anterior, se mostrará la matriz de utilidad completada con las predicciones de los ítems faltantes:
```bash
Opciones seleccionadas:
Métrica: pearson
Número de vecinos: 5
Tipo de predicción: simple
Tipo: usuario

Matriz de utilidad original:
5.0 3.0 4.0 4.0 -
3.0 1.0 2.0 3.0 3.0
4.0 3.0 4.0 3.0 5.0
3.0 3.0 1.0 5.0 4.0
1.0 5.0 5.0 2.0 1.0

Métrica entre los usuarios:
Usuario 1 - Usuario 2: Pearson = 0.853
Usuario 1 - Usuario 3: Pearson = 0.707
Usuario 1 - Usuario 4: Pearson = 0.000
Usuario 1 - Usuario 5: Pearson = -0.792
Usuario 2 - Usuario 3: Pearson = 0.468
Usuario 2 - Usuario 4: Pearson = 0.490
Usuario 2 - Usuario 5: Pearson = -0.900
Usuario 3 - Usuario 4: Pearson = -0.161
Usuario 3 - Usuario 5: Pearson = -0.467
Usuario 4 - Usuario 5: Pearson = -0.642

Matriz de utilidad predicha:
5.0 3.0 4.0 4.0 2.3
3.0 1.0 2.0 3.0 3.0
4.0 3.0 4.0 3.0 5.0
3.0 3.0 1.0 5.0 4.0
1.0 5.0 5.0 2.0 1.0
```

### Formato del archivo de matriz de utilidad
El archivo debe tener el siguiente formato:
```bash
1.0
5.0
5.0 3.0 4.0 4.0 -
3.0 1.0 2.0 3.0 3.0 
4.0 3.0 4.0 3.0 5.0
3.0 3.0 1.0 5.0 4.0
1.0 5.0 5.0 2.0 1.0
```
Donde:
- La primera línea representa el valor mínimo de puntuación asignable por un usuario a un ítem.
- La segunda línea representa el valor máximo de puntuación asignable.
- Las siguientes líneas representan las calificaciones de usuarios a ítems, donde `-` indica una calificación desconocida.
