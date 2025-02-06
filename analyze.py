import pandas as pd
import matplotlib.pyplot as plt
import re

def analyze_loot_data(csv_file):
    """
    Analyzes loot data from a CSV file, groups it by item name and rarity,
    and generates a stacked bar chart with thicker bars and count labels.

    Args:
        csv_file: Path to the CSV file.
    """

    try:
        # Read the CSV file into a DataFrame
        df = pd.read_csv(csv_file)

        # Extract item name and rarity from the 'Line' column
        df['Item Name'] = df['Line'].apply(lambda x: re.sub(r" \((.*?)\)", "", x).strip())
        df['Rarity'] = df['Line'].str.extract(r" \((.*?)\)")
        df['Rarity'].fillna('Normal', inplace=True)

        # Ensure (Legendary) is the last category when stacking
        rarity_order = ['Normal', 'Enchanted', 'Legendary']  # Define the desired order
        df['Rarity'] = pd.Categorical(df['Rarity'], categories=rarity_order, ordered=True)

       # Calculate total counts for each item
        item_counts = df['Item Name'].value_counts()

        # Sort the item names based on total counts (descending)
        sorted_items = item_counts.index

        # Use the sorted items as the index for the groupby and unstack
        item_rarity_counts = df.groupby(['Item Name', 'Rarity']).size().unstack(fill_value=0).reindex(sorted_items)

        # Create the stacked bar chart with thicker bars
        ax = item_rarity_counts.plot(kind='bar', stacked=True, width=.9)  # Increased bar width

        # Add count labels inside each bar
        for c in ax.containers:
            # Custom label for each bar
            labels = [str(int(v)) if v > 0 else "" for v in c.datavalues] # Filter out 0 labels
            ax.bar_label(c, labels=labels, label_type='center')

        plt.title('Distribution of Looted Items by Rarity')
        plt.xlabel('Item Name')
        plt.ylabel('Number of Loots')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        plt.show()

    except Exception as e:
        print(f"An error occurred: {e}")


csv_file = r'C:\Users\Joe\Desktop\Projects\THJLogsVelious\matched_lines.csv'  # Replace with the actual path to your CSV file
analyze_loot_data(csv_file)

