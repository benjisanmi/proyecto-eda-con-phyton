# ===============================================================
# FASE 1: CARGA, INSPECCIÓN Y LIMPIEZA INICIAL DE DATOS
# ===============================================================

# --- Importar librerías necesarias ---
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Configuraciones generales de visualización
pd.set_option('display.max_columns', None)
sns.set(style="whitegrid", palette="pastel")

# ===============================================================
# fASE 1:CARGA DE DATOS
# ===============================================================

# Cargar dataset principal
bank_df = pd.read_csv('bank-additional.csv', sep=',')

# Cargar dataset de detalles de clientes (tres hojas en Excel)
customer_2018 = pd.read_excel('customer-details.xlsx', sheet_name=0)
customer_2019 = pd.read_excel('customer-details.xlsx', sheet_name=1)
customer_2020 = pd.read_excel('customer-details.xlsx', sheet_name=2)

# Unir las tres hojas en un solo DataFrame
customer_df = pd.concat([customer_2018, customer_2019, customer_2020], ignore_index=True)

print("Datos cargados correctamente.")
print(f"Dimensiones - Bank: {bank_df.shape} | Customers: {customer_df.shape}")

# ===============================================================
# fASE 2: INSPECCIÓN INICIAL
# ===============================================================

# Mostrar las primeras filas de ambos datasets
print(bank_df.head())
print(customer_df.head())

# Tipos de datos y valores nulos
print("\n--- Información general ---")
bank_df.info()
print("\n--- Valores nulos en Bank ---")
print(bank_df.isnull().sum())

print("\n--- Información general (Customers) ---")
customer_df.info()
print("\n--- Valores nulos en Customers ---")
print(customer_df.isnull().sum())

# ===============================================================
# fase 3: DETECCIÓN DE DUPLICADOS Y CONSISTENCIA
# ===============================================================

# Duplicados
print(f"\nDuplicados en bank-additional: {bank_df.duplicated().sum()}")
print(f"Duplicados en customer-details: {customer_df.duplicated().sum()}")

# Eliminar duplicados si existen
bank_df.drop_duplicates(inplace=True)
customer_df.drop_duplicates(inplace=True)

# ===============================================================
# FASE 4: LIMPIEZA Y ESTANDARIZACIÓN DE COLUMNAS
# ===============================================================

# Convertir nombres de columnas a minúsculas y reemplazar espacios por "_"
bank_df.columns = bank_df.columns.str.lower().str.replace(" ", "_")
customer_df.columns = customer_df.columns.str.lower().str.replace(" ", "_")

# Comprobamos columnas clave
print("\nColumnas bank_additional:", bank_df.columns.tolist())
print("Columnas customer_details:", customer_df.columns.tolist())

# ===============================================================
# fase 5:Gráficos
# ===============================================================

# Revisar valores únicos de variables categóricas
for col in bank_df.select_dtypes(include='object').columns:
    print(f"\n{col}: {bank_df[col].unique()}")

# Boxplot para revisar posibles outliers en edad o duración
plt.figure(figsize=(10,4))
sns.boxplot(x=bank_df["age"])
plt.title("Distribución de la edad (detección de outliers)")
plt.show()

plt.figure(figsize=(10,4))
sns.boxplot(x=bank_df["duration"])
plt.title("Duración de llamadas (detección de outliers)")
plt.show()

# -------------------------------------------------------------
# 1. Histogramas de variables numéricas
# -------------------------------------------------------------
numeric_cols = bank_df.select_dtypes(include=np.number).columns

for col in numeric_cols:
    plt.figure(figsize=(8,4))
    plt.hist(bank_df[col].dropna(), bins=30, edgecolor='black')
    plt.title(f"Histograma de {col}")
    plt.xlabel(col)
    plt.ylabel("Frecuencia")
    plt.tight_layout()
    plt.show()

# -------------------------------------------------------------
# 2. Pie charts
# -------------------------------------------------------------
categorical_cols = bank_df.select_dtypes(include='object').columns

for col in categorical_cols:
    if bank_df[col].nunique() <= 6:   # Evitar gráficos ilegibles
        plt.figure(figsize=(6,6))
        bank_df[col].value_counts().plot(
            kind='pie', autopct='%1.1f%%', startangle=90
        )
        plt.title(f"Distribución (Pie Chart) de {col}")
        plt.ylabel("")
        plt.tight_layout()
        plt.show()

# -------------------------------------------------------------
#3. Gráficos de barras para variables categóricas
# -------------------------------------------------------------
for col in categorical_cols:
    plt.figure(figsize=(10,4))
    sns.countplot(data=bank_df, x=col)
    plt.xticks(rotation=45)
    plt.title(f"Conteo de valores para {col}")
    plt.tight_layout()
    plt.show()

# =============================================================
# fase 6: TRATAMIENTO DE VALORES FALTANTES
# ===============================================================

# Ejemplo: reemplazar 'unknown' por NaN para tratarlos como faltantes
bank_df.replace('unknown', np.nan, inplace=True)

# Visualizar porcentaje de nulos
missing_percent = bank_df.isnull().mean() * 100
print("\nPorcentaje de valores faltantes por columna:")
print(missing_percent[missing_percent > 0].sort_values(ascending=False))

# ===============================================================
# fase 7: EXPORTAR DATOS LIMPIOS
# ===============================================================

# Guardar versión limpia para uso posterior
bank_df.to_csv('clean_data.csv', index=False)
print("\n clean_data.csv")


