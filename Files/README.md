# Dokumentasi Text Mining untuk Pemetaan Nama Produk ke SKU

## Deskripsi Umum
Kode ini dibuat untuk melakukan pemetaan antara nama produk yang ditulis bebas dalam data POS (Point of Sale) ke SKU (Stock Keeping Unit) yang sesuai dalam katalog produk menggunakan teknik text mining. Metode yang digunakan termasuk vektorisasi teks dengan TF-IDF (Term Frequency-Inverse Document Frequency) dan perhitungan kesamaan cosine.

## Fungsi Utama

### `preprocess_text(text: str) -> str`
Fungsi ini melakukan pra-pemrosesan pada teks, mengonversi NaN menjadi string dan mengubah huruf menjadi huruf kecil.

### `map_product_names(pos_df: DataFrame, catalog_df: DataFrame, new_sku_threshold=0.6) -> DataFrame`
Fungsi ini melakukan pemetaan antara nama produk dalam data POS (`pos_df`) ke SKU yang sesuai dalam katalog produk (`catalog_df`). Proses ini melibatkan vektorisasi teks menggunakan TF-IDF untuk nama produk dan formula, perhitungan kesamaan cosine, dan pemetaan berdasarkan ambang batas kesamaan yang digabungkan. Hasilnya mencakup kolom-kolom seperti Nama Produk, SKU Produk, Merek, Tipe, Formula, dan Skor Kesamaan.

## Penggunaan

```python
# Memuat dataset
product_catalog = pd.read_excel("productCatalog.xlsx")
pos_transactions = pd.read_excel("productName.xlsx")

# Memetakan nama produk
mapped_results = map_product_names(pos_transactions, product_catalog)

# Menampilkan hasil pemetaan
print(mapped_results)

# Parameter Utama
- pos_df: DataFrame - Data POS yang berisi nama produk yang akan dipetakan.
- catalog_df: DataFrame - Katalog produk yang berisi SKU, nama produk, dan informasi lainnya.
- threshold: Nilai ambang batas kesamaan untuk pemetaan produk (opsional).
- new_sku_threshold: Nilai ambang batas kesamaan untuk menetapkan SKU baru (opsional).
- formula_threshold: Nilai ambang batas kesamaan untuk pemetaan berdasarkan formula produk (opsional).

# Output
DataFrame hasil pemetaan dengan kolom-kolom: Nama Produk, SKU Produk, Merek, Tipe, Formula, dan Skor Kesamaan.