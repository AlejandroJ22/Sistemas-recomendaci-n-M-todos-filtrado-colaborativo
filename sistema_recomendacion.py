import argparse
import numpy as np

# Leer la matriz de utilidad desde un fichero .txt
def leer_matriz_utilidad(fichero):
    with open(fichero, 'r') as f:
        lines = f.readlines()
    
    # Leer los valores mínimo y máximo de puntuación
    min_val = float(lines[0].strip())
    max_val = float(lines[1].strip())
    
    # Leer las filas de calificaciones, separadas por espacios
    matriz = []
    for line in lines[2:]:
        row = [float(x) if x != '-' else np.nan for x in line.strip().split()]
        matriz.append(row)
    
    return np.array(matriz), min_val, max_val

# Calcular Correlación de Pearson
def pearson_correlation(usuario1, usuario2):
    mask = ~np.isnan(usuario1) & ~np.isnan(usuario2)  
    if np.sum(mask) == 0:
        return 0  # No hay datos comunes, devolver 0
    
    usuario1_filtrado = usuario1[mask]
    usuario2_filtrado = usuario2[mask]
    
    mean1 = np.mean(usuario1_filtrado)
    mean2 = np.mean(usuario2_filtrado)
    
    numerador = np.sum((usuario1_filtrado - mean1) * (usuario2_filtrado - mean2))
    denominador = np.sqrt(np.sum((usuario1_filtrado - mean1)**2)) * np.sqrt(np.sum((usuario2_filtrado - mean2)**2))
    
    return numerador / denominador if denominador != 0 else 0

# Calcular Distancia Coseno
def cosine_similarity(usuario1, usuario2):
    mask = ~np.isnan(usuario1) & ~np.isnan(usuario2)
    if np.sum(mask) == 0:
        return 0  # No hay datos comunes, devolver 0

    usuario1_filtrado = usuario1[mask]
    usuario2_filtrado = usuario2[mask]
    
    dot_product = np.dot(usuario1_filtrado, usuario2_filtrado)
    norm1 = np.linalg.norm(usuario1_filtrado)
    norm2 = np.linalg.norm(usuario2_filtrado)
    
    return dot_product / (norm1 * norm2) if norm1 != 0 and norm2 != 0 else 0

# Calcular Distancia Euclídea
def euclidean_distance(usuario1, usuario2):
    mask = ~np.isnan(usuario1) & ~np.isnan(usuario2)
    if np.sum(mask) == 0:
        return 0  # No hay datos comunes, devolver 0
    
    usuario1_filtrado = usuario1[mask]
    usuario2_filtrado = usuario2[mask]
    
    return 1 / (1 + np.sqrt(np.sum((usuario1_filtrado - usuario2_filtrado) ** 2)))

# Calcular similaridad entre usuarios o ítems usando la métrica seleccionada
def calcular_similaridad(matriz, idx1, idx2, metrica, es_usuario=True):
    if es_usuario:
        return calcular_similaridad_usuario(matriz[idx1], matriz[idx2], metrica)
    else:
        return calcular_similaridad_item(matriz[:, idx1], matriz[:, idx2], metrica)

def calcular_similaridad_usuario(usuario1, usuario2, metrica):
    if metrica == 'pearson':
        return pearson_correlation(usuario1, usuario2)
    elif metrica == 'coseno':
        return cosine_similarity(usuario1, usuario2)
    elif metrica == 'euclidean':
        return euclidean_distance(usuario1, usuario2)
    else:
        raise ValueError("Métrica no reconocida. Use 'pearson', 'coseno', o 'euclidean'.")

def calcular_similaridad_item(item1, item2, metrica):
    return calcular_similaridad_usuario(item1, item2, metrica)

# Mostrar la métrica seleccionada entre los usuarios o ítems
def mostrar_metricas(matriz, metrica, es_usuario=True):
    print("\nMétrica entre los " + ("usuarios:" if es_usuario else "ítems:"))
    n = matriz.shape[0] if es_usuario else matriz.shape[1]
    
    for i in range(n):
        for j in range(i + 1, n):
            similaridad = calcular_similaridad(matriz, i, j, metrica, es_usuario)
            print(f"{'Usuario' if es_usuario else 'Ítem'} {i+1} - {'Usuario' if es_usuario else 'Ítem'} {j+1}: {metrica.capitalize()} = {similaridad:.3f}")

# Seleccionar los vecinos más cercanos
def obtener_vecinos(matriz, idx, metrica, num_vecinos, es_usuario=True):
    distancias = []
    entidad = matriz[idx] if es_usuario else matriz[:, idx]
    for i in range(matriz.shape[0] if es_usuario else matriz.shape[1]):
        if i != idx:
            similaridad = calcular_similaridad(matriz, idx, i, metrica, es_usuario)
            distancias.append((i, similaridad))
    
    distancias.sort(key=lambda x: x[1], reverse=True)
    return distancias[:num_vecinos]

# Hacer predicción simple para un ítem faltante
def predecir_simple(matriz, usuario_idx, item_idx, vecinos):
    num, denom = 0, 0
    for vecino_idx, similaridad in vecinos:
        calificacion_vecino = matriz[vecino_idx, item_idx]
        if not np.isnan(calificacion_vecino):
            num += similaridad * calificacion_vecino
            denom += abs(similaridad)
    return num / denom if denom != 0 else np.nan

# Hacer predicción usando la diferencia con la media
def predecir_con_media(matriz, usuario_idx, item_idx, vecinos):
    media_usuario = np.nanmean(matriz[usuario_idx])
    num, denom = 0, 0
    for vecino_idx, similaridad in vecinos:
        media_vecino = np.nanmean(matriz[vecino_idx])
        calificacion_vecino = matriz[vecino_idx, item_idx]
        if not np.isnan(calificacion_vecino):
            num += similaridad * (calificacion_vecino - media_vecino)
            denom += abs(similaridad)
    return media_usuario + (num / denom) if denom != 0 else np.nan

# Predicción para completar la matriz de utilidad
def predecir_matriz(matriz, metrica, num_vecinos, tipo_prediccion, es_usuario=True):
    matriz_predicha = np.copy(matriz)
    n = matriz.shape[0] if es_usuario else matriz.shape[1]
    
    for idx in range(n):
        vecinos = obtener_vecinos(matriz, idx, metrica, num_vecinos, es_usuario)
        for item_idx in range(matriz.shape[1] if es_usuario else matriz.shape[0]):
            if np.isnan(matriz[idx, item_idx]) if es_usuario else np.isnan(matriz[item_idx, idx]):
                if tipo_prediccion == 'simple':
                    if es_usuario:
                        matriz_predicha[idx, item_idx] = predecir_simple(matriz, idx, item_idx, vecinos)
                    else:
                        matriz_predicha[item_idx, idx] = predecir_simple(matriz.T, item_idx, idx, vecinos)
                elif tipo_prediccion == 'media':
                    if es_usuario:
                        matriz_predicha[idx, item_idx] = predecir_con_media(matriz, idx, item_idx, vecinos)
                    else:
                        matriz_predicha[item_idx, idx] = predecir_con_media(matriz.T, item_idx, idx, vecinos)
    return matriz_predicha

# Función para imprimir la matriz con un formato adecuado
def imprimir_matriz(matriz):
    for fila in matriz:
        fila_formateada = ['{:.1f}'.format(x) if not np.isnan(x) else '-' for x in fila]
        print(" ".join(fila_formateada))

# Función principal
def main():
    parser = argparse.ArgumentParser(description="Sistema de recomendación basado en filtrado colaborativo de películas y series.")
    parser.add_argument('fichero', type=str, help="Ruta al fichero con la matriz de utilidad (TXT)")
    parser.add_argument('--metrica', type=str, choices=['pearson', 'coseno', 'euclidean'], required=True, help="Métrica de similaridad")
    parser.add_argument('--vecinos', type=int, required=True, help="Número de vecinos a considerar")
    parser.add_argument('--prediccion', type=str, choices=['simple', 'media'], required=True, help="Tipo de predicción ('simple' o 'media')")
    parser.add_argument('--tipo', type=str, choices=['usuario', 'item'], required=True, help="Tipo de operación ('usuario' o 'item')")
    
    args = parser.parse_args()

    # Mostrar opciones seleccionadas
    print(f"\nOpciones seleccionadas:\nMétrica: {args.metrica}\nNúmero de vecinos: {args.vecinos}\nTipo de predicción: {args.prediccion}\nTipo: {args.tipo}")

    # Leer la matriz de utilidad
    matriz, min_val, max_val = leer_matriz_utilidad(args.fichero)

    # Mostrar la matriz original
    print("\nMatriz de utilidad original:")
    imprimir_matriz(matriz)

    # Mostrar métricas solo para la opción seleccionada
    if args.tipo == 'usuario':
        mostrar_metricas(matriz, args.metrica, es_usuario=True)
        matriz_predicha = predecir_matriz(matriz, args.metrica, args.vecinos, args.prediccion, es_usuario=True)
    else:
        mostrar_metricas(matriz.T, args.metrica, es_usuario=False)
        matriz_predicha = predecir_matriz(matriz.T, args.metrica, args.vecinos, args.prediccion, es_usuario=False).T

    # Predecir la matriz y mostrar resultados
    matriz_predicha = predecir_matriz(matriz, args.metrica, args.vecinos, args.prediccion, es_usuario=(args.tipo == 'usuario'))

    print("\nMatriz de utilidad predicha:")
    imprimir_matriz(matriz_predicha)

if __name__ == "__main__":
    main()