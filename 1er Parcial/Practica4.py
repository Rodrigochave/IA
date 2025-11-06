import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats.mstats import winsorize
from sklearn.preprocessing import StandardScaler, MinMaxScaler, LabelEncoder, OneHotEncoder
from sklearn.impute import SimpleImputer

def analyze_dataset_structure(df):
    print("=== ESTRUCTURA DEL DATASET ===")
    print(f"• Instancias: {df.shape[0]:,}")
    print(f"• Dimensiones: {df.shape[1]}")
    
    # Análisis de tipos de datos
    print("\n=== TIPOS DE DATOS ===")
    type_counts = df.dtypes.value_counts()
    for dtype, count in type_counts.items():
        print(f"• {dtype}: {count} columnas")
    
    return df

def comprehensive_eda(df):        
    # A) Valores faltantes
    print("\n=== VALORES FALTANTES DETECTADOS ===")
    missing_data = pd.DataFrame({
        'Missing_Count': df.isnull().sum(),
        'Missing_Percentage': (df.isnull().sum() / len(df)) * 100
    }).sort_values('Missing_Percentage', ascending=False)
    
    # Filtrar solo columnas con valores faltantes
    missing_data_filtered = missing_data[missing_data['Missing_Count'] > 0]
    
    if len(missing_data_filtered) > 0:
        print(f"SE ENCONTRARON {len(missing_data_filtered)} COLUMNAS CON VALORES FALTANTES:")
        for idx, row in missing_data_filtered.iterrows():
            print(f" {idx}: {int(row['Missing_Count'])} valores ({row['Missing_Percentage']:.2f}%)")
    else:
        print("No se encontraron valores faltantes")
    
    return missing_data

def encode_categorical_variables(df):
    print(f"\nCONVIRTIENDO VARIABLES CATEGÓRICAS A NUMÉRICAS")
    
    categorical_cols = df.select_dtypes(include=['object']).columns.tolist()
    
    if len(categorical_cols) == 0:
        print("No hay variables categóricas para convertir")
        return df, {}, []    
    df_encoded = df.copy()
    encoding_info = {}
    label_encoded_cols = []  # Para trackear columnas convertidas a numéricas
    
    for col in categorical_cols:
        unique_count = df[col].nunique()
        
        print(f"\n {col}:")
        print(f"   • Valores únicos: {unique_count}")
        
        # Estrategia de codificación basada en cardinalidad
        if unique_count == 2:
            # Variables binarias: Label Encoding
            le = LabelEncoder()
            df_encoded[col] = le.fit_transform(df_encoded[col].astype(str))
            encoding_info[col] = {
                'method': 'Label Encoding',
                'mapping': dict(zip(le.classes_, range(len(le.classes_))))
            }
            label_encoded_cols.append(col)
            print(f"Label Encoding aplicado")
            
        elif 3 <= unique_count <= 10:
            # Cardinalidad baja: One-Hot Encoding
            dummies = pd.get_dummies(df_encoded[col], prefix=col)
            df_encoded = pd.concat([df_encoded.drop(col, axis=1), dummies], axis=1)
            encoding_info[col] = {
                'method': 'One-Hot Encoding',
                'new_columns': dummies.columns.tolist()
            }
            print(f"One-Hot Encoding aplicado")
            print(f"      Nuevas columnas: {len(dummies.columns)}")
            
        else:
            # Cardinalidad alta: Label Encoding (para evitar demasiadas columnas)
            le = LabelEncoder()
            df_encoded[col] = le.fit_transform(df_encoded[col].astype(str))
            encoding_info[col] = {
                'method': 'Label Encoding (alta cardinalidad)',
                'mapping': f"{len(le.classes_)} categorías convertidas a números"
            }
            label_encoded_cols.append(col)
            print(f"Label Encoding aplicado (alta cardinalidad)")
    
    print(f"\nCodificación completada")
    print(f"   • Dataset antes: {df.shape}")
    print(f"   • Dataset después: {df_encoded.shape}")
    print(f"   • Columnas convertidas a numéricas: {len(label_encoded_cols)}")
    
    return df_encoded, encoding_info, label_encoded_cols

def impute_missing_values_advanced(df, label_encoded_cols, threshold=10):
    print(f"\nIMPUTANDO VALORES FALTANTES")
    
    # Verificar si hay valores faltantes
    missing_before = df.isnull().sum().sum()
    if missing_before == 0:
        print("No hay valores faltantes para imputar")
        return df, {}
    
    print(f"Valores faltantes antes de imputación: {missing_before}")
    
    df_imputed = df.copy()
    imputation_info = {}
    
    # Identificar columnas con missing values
    cols_with_missing = df.columns[df.isnull().any()].tolist()
    
    for col in cols_with_missing:
        missing_count = df[col].isnull().sum()
        missing_percent = (missing_count / len(df)) * 100
        
        print(f"\n Procesando {col}:")
        print(f"   • Valores faltantes: {missing_count} ({missing_percent:.2f}%)")
        print(f"   • Tipo de dato: {df[col].dtype}")
        
        # Estrategia de imputación basada en el tipo de dato
        if df[col].dtype in ['int64', 'float64'] or col in label_encoded_cols:
            # Para variables numéricas o label-encoded
            if missing_percent > threshold:
                # Muchos valores faltantes: usar mediana (robusta a outliers)
                imputation_value = df[col].median()
                strategy = f"mediana ({imputation_value:.2f})"
            else:
                # Pocos valores faltantes: usar media
                imputation_value = df[col].mean()
                strategy = f"media ({imputation_value:.2f})"
            
            df_imputed[col] = df_imputed[col].fillna(imputation_value)
            print(f"Imputado con {strategy}")
            
        else:
            # Para variables one-hot encoded (booleanas)
            # En one-hot, los missing se imputan con 0 (ausencia de la categoría)
            imputation_value = 0
            strategy = f"cero (0) - ausencia de categoría"
            df_imputed[col] = df_imputed[col].fillna(imputation_value)
            print(f"Imputado con {strategy}")
        
        imputation_info[col] = {
            'missing_before': missing_count,
            'strategy': strategy
        }
    
    # Verificar resultado
    missing_after = df_imputed.isnull().sum().sum()
    print(f"\nValores faltantes después de imputación: {missing_after}")
    
    return df_imputed, imputation_info

def detect_and_handle_outliers_advanced(df, label_encoded_cols):
    """Detección y manejo de outliers en TODAS las variables numéricas - MEJORADO"""
    
    # Incluir todas las columnas numéricas Y las label-encoded
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    
    if len(numeric_cols) == 0:
        print("\nNO HAY VARIABLES NUMÉRICAS - Saltando detección de outliers")
        return df, []
    
    print(f"\nDETECTANDO OUTLIERS EN {len(numeric_cols)} VARIABLES NUMÉRICAS")
    
    outlier_info = []
    
    for col in numeric_cols:
        # Excluir valores nulos para el cálculo
        non_null_data = df[col].dropna()
        if len(non_null_data) == 0:
            continue
            
        # Calcular límites IQR
        Q1 = non_null_data.quantile(0.25)
        Q3 = non_null_data.quantile(0.75)
        IQR = Q3 - Q1
        
        # Solo calcular outliers si IQR > 0 (evitar divisiones por 0)
        if IQR > 0:
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            
            # Contar outliers
            outliers = non_null_data[(non_null_data < lower_bound) | (non_null_data > upper_bound)]
            outlier_count = len(outliers)
            outlier_percent = (outlier_count / len(non_null_data)) * 100
            
            if outlier_count > 0 and outlier_percent < 20:  # Solo si menos del 20% son outliers
                outlier_info.append({
                    'Variable': col,
                    'Outliers': outlier_count,
                    'Porcentaje': f"{outlier_percent:.2f}%",
                    'Límite_Inferior': f"{lower_bound:.2f}",
                    'Límite_Superior': f"{upper_bound:.2f}"
                })
    
    # Mostrar resultados
    if outlier_info:
        print("OUTLIERS DETECTADOS:")
        outlier_df = pd.DataFrame(outlier_info)
        print(outlier_df.to_string(index=False))
        
        # Aplicar winsorize
        print(f"\nAPLICANDO WINSORIZE A {len(outlier_info)} VARIABLES...")
        df_winsorized = df.copy()
        
        for col_info in outlier_info:
            col = col_info['Variable']
            try:
                # Aplicar winsorize solo a los valores no nulos
                non_null_mask = df_winsorized[col].notna()
                if non_null_mask.sum() > 0:  # Verificar que hay datos no nulos
                    winsorized_values = winsorize(df_winsorized.loc[non_null_mask, col], limits=[0.05, 0.05])
                    df_winsorized.loc[non_null_mask, col] = winsorized_values
                    print(f"{col}: winsorize aplicado")
            except Exception as e:
                print(f"{col}: error al aplicar winsorize - {e}")
        
        return df_winsorized, outlier_info
    else:
        print("No se detectaron outliers significativos")
        return df, []

def normalize_dataset_advanced(df, label_encoded_cols, target_col='Type'):
    print(f"\nNORMALIZANDO DATASET")
    
    # Incluir TODAS las columnas numéricas excepto la columna objetivo
    cols_to_normalize = [
        col for col in df.select_dtypes(include=[np.number]).columns 
        if col != target_col
    ]
    
    if len(cols_to_normalize) == 0:
        print("No hay variables numéricas para normalizar")
        return df, None
    
    print(f"Normalizando {len(cols_to_normalize)} variables numéricas (sin incluir '{target_col}')...")
    
    df_normalized = df.copy()
    scaler = StandardScaler()
    method_name = "StandardScaler (media=0, desviación=1)"
    print(f"   • Método: {method_name}")
    
    # Aplicar normalización solo a las variables numéricas (no al target)
    df_normalized[cols_to_normalize] = scaler.fit_transform(df[cols_to_normalize])
    
    print(f"Normalización completada")
    print(f"   • Estadísticas después de normalizar:")
    stats_after = pd.DataFrame({
        'Media': df_normalized[cols_to_normalize].mean(),
        'Desviación': df_normalized[cols_to_normalize].std(),
        'Mínimo': df_normalized[cols_to_normalize].min(),
        'Máximo': df_normalized[cols_to_normalize].max()
    })
    print(stats_after.round(3))
    
    return df_normalized, scaler


# Cargar datos asegurando que se detecten los valores faltantes
def load_data_with_missing_detection(file_path):
    """Carga el dataset forzando la detección de valores faltantes"""
    na_values = ['?', '??', '???', '', ' ', '  ', 'NA', 'N/A', 'nan', 'NaN', 'null', 'NULL', 'unknown', 'Unknown', 'missing', 'Missing', '-', '--', '---']
    
    try:
        df = pd.read_csv(file_path, na_values=na_values, keep_default_na=True)
    except:
        try:
            df = pd.read_excel(file_path, na_values=na_values, keep_default_na=True)
        except:
            df = pd.read_csv(file_path)    
    return df

# PIPELINE COMPLETO MEJORADO
def complete_preprocessing_pipeline_improved(file_path):
    """Pipeline completo de preprocesamiento - VERSIÓN MEJORADA"""
    print("=" * 60)
    
    # 1. Cargar datos
    df = load_data_with_missing_detection(file_path)
    print(f"1. Dataset cargado: {df.shape}")
    
    # 2. Análisis de estructura
    analyze_dataset_structure(df)
    
    # 3. EDA completo
    missing_analysis = comprehensive_eda(df)
    
    # 4. Convertir variables categóricas a numéricas PRIMERO
    df_encoded, encoding_info, label_encoded_cols = encode_categorical_variables(df)
    
    # 5. Imputar valores faltantes DESPUÉS de la codificación (usando media/mediana)
    df_imputed, imputation_info = impute_missing_values_advanced(df_encoded, label_encoded_cols, threshold=10)
    
    # 6. Detectar y manejar outliers en TODAS las variables numéricas
    df_processed, outlier_info = detect_and_handle_outliers_advanced(df_imputed, label_encoded_cols)
    
    # 7. Normalizar el dataset (solo variables label-encoded)
    df_final, scaler = normalize_dataset_advanced(df_processed, label_encoded_cols, target_col='class')
    
    # 8. Resumen final
    print("\n" + "=" * 60)
    print(f"RESUMEN FINAL:")
    print(f"   • Dataset original: {df.shape}")
    print(f"   • Dataset final: {df_final.shape}")
    print(f"   • Variables codificadas: {len(encoding_info)}")
    print(f"   • Variables con outliers tratadas: {len(outlier_info)}")
    print(f"   • Columnas con imputación: {len(imputation_info)}")
    print(f"   • Valores faltantes restantes: {df_final.isnull().sum().sum()}")
    
    if outlier_info:
        print(f"\nVARIABLES CON OUTLIERS TRATADAS:")
        for info in outlier_info:
            print(f"   • {info['Variable']}: {info['Outliers']} outliers ({info['Porcentaje']})")
    
    if imputation_info:
        print(f"\nDETALLE DE IMPUTACIONES:")
        for col, info in imputation_info.items():
            print(f"   • {col}: {info['missing_before']} valores → {info['strategy']}")
    
    return df_final, encoding_info, outlier_info, imputation_info, scaler

# USO COMPLETO MEJORADO
if __name__ == "__main__":
    file_path = 'C:/Users/Rodri/OneDrive/Documentos/GitHub/IA/1er Parcial/mushrooms.csv'
    try:
        # Ejecutar pipeline mejorado
        df_final, encoding_info, outlier_info, imputation_info, scaler = complete_preprocessing_pipeline_improved(file_path)
        # === GUARDAR EL DATASET FINAL ===
        output_path_csv = 'C:/Users/Rodri/OneDrive/Documentos/GitHub/IA/1er Parcial/mushrooms_preprocesado.csv'
        output_path_excel = 'C:/Users/Rodri/OneDrive/Documentos/GitHub/IA/1er Parcial/mushrooms_preprocesado.xlsx'

        # Guardar en CSV
        df_final.to_csv(output_path_csv, index=False)

        # Guardar también en Excel (opcional)
        df_final.to_excel(output_path_excel, index=False)
        print(f"\nMUESTRA DEL DATASET FINAL:")
        print(df_final.head())
    except Exception as e:
        print(f"Error durante el procesamiento: {e}")