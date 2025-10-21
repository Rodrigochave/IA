import pandas as pd
import numpy as np
from ydata_profiling import ProfileReport

# Cargar dataset
df = pd.read_csv('tu_dataset.csv')

# Análisis básico de estructura
print("=== ESTRUCTURA DEL DATASET ===")
print(f"• Número de instancias (filas): {df.shape[0]:,}")
print(f"• Número de dimensiones (columnas): {df.shape[1]}")
print(f"• Memoria utilizada: {df.memory_usage(deep=True).sum() / 1024**2:.2f} MB")

# Tipos de datos
print("\n=== TIPOS DE DATOS ===")
print(df.dtypes.value_counts())