import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import pearsonr
from math import sqrt
from scipy.stats import f_oneway, kruskal

def tipifica_variables(df, umbral_categoria, umbral_continua):
    """
    Classify columns into variable types based on cardinality and thresholds.

    Arguments:
    df (pd.DataFrame): Input dataframe.
    umbral_categoria (int): Threshold for categorical variables.
    umbral_continua (float): Threshold for continuous variables.

    Returns:
    pd.DataFrame: Dataframe with variable names and suggested types.
    """
    results = []
    for col in df.columns:
        cardinality = df[col].nunique()
        cardinality_percentage = cardinality / len(df)

        if cardinality == 2:
            tipo = "Binaria"
        elif cardinality < umbral_categoria:
            tipo = "Categorica"
        elif cardinality_percentage >= umbral_continua:
            tipo = "Numerica Continua"
        else:
            tipo = "Numerica Discreta"

        results.append({"nombre_variable": col, "tipo_sugerido": tipo})

    return pd.DataFrame(results)


def get_features_num_regression(df, target_col, umbral_corr=0.3, pvalue=None):
    """
    Devuelve una lista con las columnas numéricas del DataFrame cuya correlación absoluta con target_col 
    sea superior a umbral_corr. Si pvalue no es None, también se filtran por significación estadística.
    Si los argumentos de entrada no son adecuados, devuelve None e imprime la razón.

    Args:
        df (pd.DataFrame): DataFrame con los datos.
        target_col (str): Columna del DataFrame que será utilizada como target (debe ser numérica continua).
        umbral_corr (float): Umbral de correlación absoluta (0 a 1).
        pvalue (float, optional): Nivel de significancia para filtrar (1 - pvalue).

    Returns:
        list or None: Lista de columnas numéricas que cumplen los criterios, o None si los argumentos son inválidos.
    """
    # Comprobación 1: Que el DataFrame sea válido
    if not isinstance(df, pd.DataFrame):
        print("Error: El argumento 'df' debe ser un DataFrame de pandas.")
        return None

    # Comprobación 2: Que target_col exista y sea numérica continua
    if target_col not in df.columns:
        print(f"Error: La columna target '{target_col}' no está en el DataFrame.")
        return None
    if not pd.api.types.is_numeric_dtype(df[target_col]):
        print(f"Error: La columna target '{target_col}' no es numérica.")
        return None
    if len(df[target_col].unique()) <= 10:  # Suponemos que <10 valores únicos no es continuo
        print(f"Error: La columna target '{target_col}' no parece ser continua (tiene pocos valores únicos).")
        return None

    # Comprobación 3: Que umbral_corr sea un float entre 0 y 1
    if not isinstance(umbral_corr, (float, int)) or not (0 <= umbral_corr <= 1):
        print("Error: El argumento 'umbral_corr' debe ser un número entre 0 y 1.")
        return None

    # Comprobación 4: Que pvalue sea None o un float válido
    if pvalue is not None and (not isinstance(pvalue, (float, int)) or not (0 < pvalue <= 1)):
        print("Error: El argumento 'pvalue' debe ser None o un número entre 0 y 1.")
        return None

    # Seleccionar columnas numéricas excluyendo el target
    columnas_numericas = df.select_dtypes(include='number').columns
    columnas_numericas = [col for col in columnas_numericas if col != target_col]

    if len(columnas_numericas) == 0:
        print("Error: No hay columnas numéricas (excluyendo la target) en el DataFrame.")
        return None

    # Lista para almacenar las columnas que cumplen los criterios
    columnas_seleccionadas = []

    # Calcular correlaciones y valores p
    for col in columnas_numericas:
        correlacion, p_val = pearsonr(df[col], df[target_col])

        # Filtrar por correlación
        if abs(correlacion) > umbral_corr:
            # Filtrar por p-value si se proporciona
            if pvalue is None or p_val <= pvalue:
                columnas_seleccionadas.append(col)

    # Si no se encuentran columnas que cumplan los criterios, devolver None
    if not columnas_seleccionadas:
        print("No se encontraron columnas que cumplan con los criterios especificados.")
        return None

    return columnas_seleccionadas

def plot_features_num_regression(df, target_col, selected_features):
    """
    Lo que hace esta función es generar gráficas para ver la relación entre las features y la variable objetivo

    Argumentos:
    - df_nike (pd.DataFrame): DataFrame de entrada de los datos
    - target_col (str): Nombre de la columna objetivo (tiene que ser numérica).
    - selected_features (list): Lista de variables seleccionadas para hacer el modelo de regresión.

    Returns:
    - Devuelve gráficas de dispersión entre cada variable seleccionada y la variable target
    """
    # Hago las validaciones oportunas
    if not isinstance(df, pd.DataFrame):
        raise ValueError("El argumento 'df_nike' debe ser un DataFrame")
    
    if target_col not in df.columns:
        raise ValueError(f"'{target_col}' no está en el DataFrame")
    
    if not pd.api.types.is_numeric_dtype(df[target_col]):
        raise ValueError(f" '{target_col}' no es numérica")
    
    if not selected_features or not isinstance(selected_features, list):
        raise ValueError("El argumento 'selected_features' debe ser una lista de variables")
    
    # Filtro las variables seleccionadas del DataFrame
    selected_features = [col for col in selected_features if col in df.columns]
    
    if len(selected_features) == 0: 
        raise ValueError("No hay variables seleccionadas en el DataFrame")

    for feature in selected_features:
        plt.figure(figsize=(8, 6))
        sns.scatterplot(x=df[feature], y=df[target_col], alpha=0.7,color="#f55e13")
        plt.title(f"Relación entre {feature} y {target_col}")
        plt.xlabel(feature)
        plt.ylabel(target_col)
        plt.grid(True)
        plt.show()


def get_features_cat_regression(df, target_col, pvalue=0.05):
    """
    Devuelve una lista con las columnas categóricas del DataFrame cuyo test de relación con la columna
    designada por 'target_col' sea estadísticamente significativa usando ANOVA o Kruskal-Wallis.
    
    Argumentos:
    df: DataFrame para analizar.
    target_col (str): Columna objetivo (numérica).
    pvalue (float): Nivel de significancia para el test. Por defecto es 0.05.
    
    Retorna:
    list: Una lista con las columnas categóricas del DataFrame que tienen una relación significativa
          con la columna objetivo.
    """
    # Comprobar que la columna objetivo existe y es numérica
    if target_col not in df.columns:
        raise ValueError(f"La columna '{target_col}' no existe en el DataFrame.")
    
    if target_col not in df.select_dtypes(include=[np.number]).columns:
        raise ValueError(f"La columna '{target_col}' no es numérica en el DataFrame.")
    
    # Seleccionar columnas categóricas
    cat_columns = df.select_dtypes(include=['object', 'category']).columns

    # Lista para almacenar las columnas categóricas relevantes
    relevant_cat_columns = []

    # Iterar sobre las columnas categóricas
    for column in cat_columns:
        # Excluir columnas con demasiados valores nulos
        if df[column].isnull().mean() > 0.5:  # Umbral de 50% de valores nulos
            continue

        # Excluir columnas con una sola categoría
        if df[column].nunique() <= 1:
            continue

        # Agrupar los valores de la columna objetivo por las categorías
        groups = [df[df[column] == value][target_col].dropna() for value in df[column].unique()]

        # Si hay categorías sin datos en la columna objetivo, ignorar la columna
        if any(len(group) == 0 for group in groups):
            continue

        # Elegir la prueba estadística (ANOVA o Kruskal-Wallis)
        try:
            if all(len(group) >= 5 for group in groups):  # Suficientes datos para ANOVA
                stat, p_value = f_oneway(*groups)
            else:  # Usar Kruskal-Wallis si hay pocos datos o distribución no normal
                stat, p_value = kruskal(*groups)
        except ValueError:
            continue  # Saltar si ocurre algún error en las pruebas

        # Verificar si el p-value cumple con el umbral especificado
        if p_value <= pvalue:
            relevant_cat_columns.append(column)

    return relevant_cat_columns     

def plot_grouped_histograms(df, target_col, columns=None, pvalue=0.05, with_individual_plot=False):
    """
    Analiza la relación entre columnas categóricas y una columna numérica mediante ANOVA o Kruskal-Wallis,
    y opcionalmente genera histogramas agrupados.

    Argumentos:
    df: DataFrame con los datos.
    target_col: Columna numérica objetivo.
    columns: Lista de columnas categóricas a analizar. Si es None, se seleccionan automáticamente.
    pvalue: Umbral de significancia estadística para los tests (por defecto 0.05).
    with_individual_plot: Si es True, genera histogramas por categoría.
    
    Retorna:
    List: Lista de columnas categóricas con relación significativa con la columna objetivo.
    """
    # Verificar que la columna objetivo existe y es numérica
    if target_col not in df.columns or not pd.api.types.is_numeric_dtype(df[target_col]):
        print(f"Error: {target_col} no es una columna numérica válida.")
        return None
    
    # Si no se especifican columnas, usar las categóricas del DataFrame
    if columns is None:
        columns = df.select_dtypes(include=['object', 'category']).columns

    significant_columns = []  # Para almacenar las columnas significativas

    # Iterar sobre las columnas especificadas
    for col in columns:
        # Verificar si la columna es categórica
        if col not in df.columns or pd.api.types.is_numeric_dtype(df[col]):
            continue

        # Agrupar los valores de la columna objetivo por categorías
        groups = [df[df[col] == value][target_col].dropna() for value in df[col].unique()]

        # Saltar si hay categorías vacías o insuficientes datos
        if any(len(group) < 2 for group in groups):
            continue

        # Aplicar ANOVA si los tamaños de los grupos son suficientes, sino Kruskal-Wallis
        try:
            if all(len(group) >= 5 for group in groups):  # Usar ANOVA si hay suficientes datos
                stat, p_val = f_oneway(*groups)
            else:  # Usar Kruskal-Wallis si hay pocos datos o si ANOVA no es aplicable
                stat, p_val = kruskal(*groups)
        except ValueError:
            continue  # Ignorar si ocurre un error en las pruebas

        # Si el p-value cumple el umbral de significancia, añadir la columna a la lista
        if p_val <= pvalue:
            significant_columns.append(col)

            # Mostrar histogramas agrupados si se solicita
            if with_individual_plot:
                plt.figure(figsize=(10, 6))
                df.groupby(col)[target_col].hist(alpha=0.5, bins=10, legend=True)
                plt.title(f"Distribución de {target_col} por {col}")
                plt.xlabel(target_col)
                plt.ylabel('Frecuencia')
                plt.legend(title=col,bbox_to_anchor=(1.05, 1), loc='upper left')
                plt.grid(axis='y', linestyle='--', alpha=0.7)
                plt.tight_layout()
                plt.show()

    # Devolver las columnas significativas
    return significant_columns