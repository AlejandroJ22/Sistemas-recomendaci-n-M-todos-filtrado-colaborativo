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
    
    dist_euclidea = np.sqrt(np.sum((usuario1_filtrado - usuario2_filtrado) ** 2))
    return 1 / (1 + dist_euclidea)

# Calcular similaridad entre usuarios usando la métrica seleccionada
def calcular_similaridad(usuario1, usuario2, metrica):
    if metrica == 'pearson':
        return pearson_correlation(usuario1, usuario2)
    elif metrica == 'coseno':
        return cosine_similarity(usuario1, usuario2)
    elif metrica == 'euclidean':
        return euclidean_distance(usuario1, usuario2)
    else:
        raise ValueError("Métrica no reconocida. Use 'pearson', 'coseno', o 'euclidean'.")

# Mostrar la métrica seleccionada entre los usuarios y devolver los resultados como lista
def mostrar_metricas(matriz, metrica):
    n = matriz.shape[0]
    metricas_resultado = []
    
    for i in range(n):
        for j in range(i + 1, n):
            similaridad = calcular_similaridad(matriz[i], matriz[j], metrica)
            metricas_resultado.append(f"Usuario {i+1} - Usuario {j+1}: {metrica.capitalize()} = {similaridad:.3f}")
    
    return metricas_resultado

# Seleccionar los vecinos más cercanos
def obtener_vecinos(matriz, idx, metrica, num_vecinos):
    distancias = []
    entidad = matriz[idx]
    for i in range(matriz.shape[0]):
        if i != idx:
            similaridad = calcular_similaridad(matriz[idx], matriz[i], metrica)
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
# Hacer predicción para completar la matriz de utilidad y guardar las predicciones
def predecir_matriz(matriz, metrica, num_vecinos, tipo_prediccion):
    matriz_predicha = np.copy(matriz)
    n = matriz.shape[0]
    predicciones_hechas = []  # Lista para almacenar las predicciones realizadas
    
    for idx in range(n):
        vecinos = obtener_vecinos(matriz, idx, metrica, num_vecinos)
        for item_idx in range(matriz.shape[1]):
            if np.isnan(matriz[idx, item_idx]):
                if tipo_prediccion == 'simple':
                    prediccion = predecir_simple(matriz, idx, item_idx, vecinos)
                elif tipo_prediccion == 'media':
                    prediccion = predecir_con_media(matriz, idx, item_idx, vecinos)
                
                matriz_predicha[idx, item_idx] = prediccion
                predicciones_hechas.append((idx + 1, item_idx + 1, prediccion))  # Almacena el índice del usuario, el ítem y la predicción
    
    return matriz_predicha, predicciones_hechas

# Función para imprimir la matriz con un formato adecuado
def imprimir_matriz(matriz):
    for fila in matriz:
        fila_formateada = ['{:.1f}'.format(x) if not np.isnan(x) else '-' for x in fila]
        print(" ".join(fila_formateada))

# Guardar la matriz en un fichero junto con las métricas
def guardar_matriz(fichero_salida, matriz, min_val, max_val, metricas, predicciones_hechas, matriz_predicha):
    with open(fichero_salida, 'w') as f:
        
        # Escribir las métricas
        f.write("Métricas:\n")
        f.write("\n".join(metricas) + "\n\n")
        
        # Escribir las predicciones
        f.write("Predicciones:\n")
        for usuario, item, prediccion in predicciones_hechas:
            f.write(f"Usuario {usuario}, Ítem {item}: Predicción = {prediccion:.1f}\n")
        f.write("\n")

        f.write("Matriz Predicha:\n")
        f.write(f"{min_val:.1f}\n")
        f.write(f"{max_val:.1f}\n")

        for fila in matriz_predicha:
            fila_formateada = ['{:.1f}'.format(x) if not np.isnan(x) else '-' for x in fila]
            f.write(" ".join(fila_formateada) + "\n")

# Función principal
def main():
    parser = argparse.ArgumentParser(description="Sistema de recomendación basado en filtrado colaborativo de películas y series.")
    parser.add_argument('fichero', type=str, help="Ruta al fichero con la matriz de utilidad (TXT)")
    parser.add_argument('--metrica', type=str, choices=['pearson', 'coseno', 'euclidean'], required=True, help="Métrica de similaridad")
    parser.add_argument('--vecinos', type=int, required=True, help="Número de vecinos a considerar")
    parser.add_argument('--prediccion', type=str, choices=['simple', 'media'], required=True, help="Tipo de predicción ('simple' o 'media')")
    parser.add_argument('--salida', type=str, required=True, help="Ruta del fichero de salida para guardar la matriz predicha")
    
    args = parser.parse_args()

    # Leer la matriz de utilidad
    matriz, min_val, max_val = leer_matriz_utilidad(args.fichero)

    # Calcular métricas
    metricas = mostrar_metricas(matriz, args.metrica)

    # Predecir la matriz y obtener las predicciones
    matriz_predicha, predicciones_hechas = predecir_matriz(matriz, args.metrica, args.vecinos, args.prediccion)
    
    # Guardar los resultados en un fichero
    guardar_matriz(args.salida, matriz, min_val, max_val, metricas, predicciones_hechas, matriz_predicha)

    print(f"\nMatriz predicha y métricas guardadas en: {args.salida}")

if __name__ == "__main__":
    main()