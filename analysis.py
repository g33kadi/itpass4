import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# 1. Загрузка данных
df = pd.read_excel("data/livestock_2024.xlsx")

# 2. Первичный анализ
print("▶ Head of dataset:")
print(df.head())

print("\n▶ Info:")
print(df.info())

print("\n▶ Description:")
print(df.describe(include='all'))

# 3. Обработка пропущенных значений
print("\n▶ Null values per column:")
print(df.isnull().sum())

# Стратегия: удаляем строки с пропущенными значениями
df_cleaned = df.dropna()

# 4. Визуализация

# Создаём директорию для скринов, если не существует
os.makedirs("screenshots", exist_ok=True)

# Гистограмма по первому числовому столбцу
plt.figure(figsize=(10, 6))
numeric_col = df_cleaned.select_dtypes(include='number').columns[0]
sns.histplot(df_cleaned[numeric_col], bins=20, kde=True)
plt.title(f'Распределение: {numeric_col}')
plt.xlabel('Значения')
plt.ylabel('Частота')
plt.tight_layout()
plt.savefig("screenshots/histogram.png")
plt.show()

# Столбчатая диаграмма: первый категориальный столбец + числовой
plt.figure(figsize=(12, 7))
cat_col = df_cleaned.select_dtypes(include='object').columns[0]
sns.barplot(x=cat_col, y=numeric_col, data=df_cleaned)
plt.title(f'{numeric_col} по {cat_col}')
plt.xlabel(cat_col)
plt.ylabel(numeric_col)
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("screenshots/barplot.png")
plt.show()