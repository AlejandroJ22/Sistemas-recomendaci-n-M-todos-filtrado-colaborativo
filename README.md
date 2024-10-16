# Sistemas de recomendación - Filtrado Colaborativo

Este es un sistema de recomendación basado en filtrado colaborativo que predice calificaciones faltantes en una matriz de utilidad de usuarios e ítems. El sistema soporta diversas métricas de similaridad y tipos de predicciones, y está diseñado como una aplicación de línea de comandos.

## Características
- Soporta las siguientes **métricas de similaridad**:
  - Correlación de Pearson
  - Distancia Coseno
  - Distancia Euclídea
- Permite crear dos tipos de **predicciones**:
  - Predicción simple
  - Diferencia con la media
- Selecciona un número configurable de **vecinos** más cercanos para las predicciones

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
python3 sistema_recomendacion.py matriz_utilidad.txt --metrica pearson --vecinos 5 --prediccion simple --tipo usuario
```

### Argumentos
- `Fichero`: Ruta al archivo `.txt` que contiene la matriz de utilidad.
- `--metrica`: Métrica de similaridad a utilizar (`pearson`, `cosine`, `euclidean`).
- `--vecinos`: Número de vecinos más cercanos a considerar.
- `--prediccion`: Tipo de predicción a realizar (`simple`, `media`).
- `--tipo`: Decide si el usuario trabaja por filas o por columnas (`usuario`, `item`).

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
