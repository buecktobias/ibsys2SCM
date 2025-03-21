import pandas as pd

if __name__ == '__main__':
    df = pd.read_csv("material_costs_cleaned_edited.csv")

    # Filter for item_type 'K' (Bought items)
    bought_items = df[df["item_type"] == "K"].copy()

    # Rename and select required columns for Bought model import
    bought_items = bought_items.rename(columns={
        "article_id": "id",
        "price_per_part": "base_price",
        "order_price": "base_order_cost",
        "order_duration": "mean_order_duration",
        "order_standard_deviation": "order_std_dev",
        "discount_quantity": "discount_amount",
    })[["id", "base_price", "base_order_cost", "mean_order_duration", "order_std_dev", "discount_amount"]]

    # Convert decimal format if necessary
    bought_items = bought_items.applymap(lambda x: str(x).replace(",", ".") if isinstance(x, str) else x)

    # Save to CSVF FILE
    bought_items.to_csv("bought_items.csv", index=False)
