import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def preprocess_text(text):
    # Add any additional text preprocessing steps if needed
    return str(text).lower()  # Convert NaN to string and lowercase

def map_product_names(pos_df, catalog_df, new_sku_threshold=0.6):
    # Text preprocessing
    pos_df["Processed_Product_Name"] = pos_df["Product Name"].apply(preprocess_text)
    catalog_df["Processed_Product_Name"] = catalog_df["productSKUCleaned"].apply(preprocess_text)

    # Text embedding using TF-IDF
    vectorizer = TfidfVectorizer()
    catalog_embeddings = vectorizer.fit_transform(catalog_df["Processed_Product_Name"])
    pos_embeddings = vectorizer.transform(pos_df["Processed_Product_Name"])

    # Similarity calculation for product names
    similarity_matrix_name = cosine_similarity(pos_embeddings, catalog_embeddings)

    # Text embedding using TF-IDF for formulas
    vectorizer_formula = TfidfVectorizer()
    catalog_formula_embeddings = vectorizer_formula.fit_transform(catalog_df["formula"].apply(preprocess_text))
    pos_formula_embeddings = vectorizer_formula.transform(pos_df["Processed_Product_Name"])

    # Similarity calculation for formulas
    similarity_matrix_formula = cosine_similarity(pos_formula_embeddings, catalog_formula_embeddings)

    # Combine the similarity scores for names and formulas with weights
    combined_similarity = 0.8 * similarity_matrix_name + 0.2 * similarity_matrix_formula

    # Mapping based on combined similarity threshold
    mapped_sku_index = combined_similarity.argmax(axis=1)
    mapped_sku = catalog_df.iloc[mapped_sku_index]['productSKUCleaned'].values
    original_sku = catalog_df.iloc[mapped_sku_index]['productSKU'].values

    pos_df["Mapped_Product_SKU"] = mapped_sku
    pos_df["Original_Product_SKU"] = original_sku
    pos_df["Similarity_Score"] = combined_similarity.max(axis=1)

    # Propose new SKU for low similarity
    pos_df.loc[pos_df["Similarity_Score"] < new_sku_threshold, "Mapped_Product_SKU"] = "NEW_SKU"

    # Optional: Map to Brand, Type, and Formula
    pos_df = pd.merge(pos_df, catalog_df[["productSKU", "brand", "type", "formula"]],
                      left_on="Mapped_Product_SKU", right_on="productSKU", how="left")

    # Set Product SKU based on Mapped_Product_SKU
    pos_df["Product SKU"] = pos_df.apply(lambda row: row["Mapped_Product_SKU"] if row["Mapped_Product_SKU"] == "NEW_SKU" else row["Original_Product_SKU"], axis=1)

    # Drop unnecessary columns
    pos_df = pos_df[["Product Name", "Product SKU", "brand", "type", "formula", "Similarity_Score"]]

    return pos_df

# Load datasets
product_catalog = pd.read_excel("productCatalog.xlsx")
pos_transactions = pd.read_excel("productName.xlsx")

# Map product names
mapped_results = map_product_names(pos_transactions, product_catalog)

# print the mapped results into csv file
print(mapped_results.to_csv('result.csv'))
