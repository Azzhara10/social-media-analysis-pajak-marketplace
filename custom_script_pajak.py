import pandas as pd
from pathlib import Path

folder = Path("tweets-data")
csv_file = folder / "pajak_marketplace_bersih.csv"

# Membaca data CSV
df = pd.read_csv(csv_file)

# Menampilkan informasi data
print("Jumlah baris:", len(df))
print("Kolom:", df.columns.tolist())

# Menampilkan 5 data pertama
print("\nContoh data:")
print(df.head())

print("\nData CSV berhasil dibaca.")