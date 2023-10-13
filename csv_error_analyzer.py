import pandas as pd
from collections import defaultdict

# Prompt the user for the input file name
input_file = input("Enter the input CSV file name: ")

# Read the CSV file into a DataFrame
data = pd.read_csv(input_file)

# Initialize a defaultdict to store occurrences and a dictionary for aggregator totals
occurrences = defaultdict(lambda: defaultdict(int))
aggregator_totals = defaultdict(int)

# Loop through the DataFrame rows
for _, row in data.iterrows():
    if pd.isna(row['message']):
        print("Found a row with a missing 'message'. Skipping.")
        continue

    # Split the 'message' field by '|' delimiter
    messages = row['message'].split('|')

    # Check if there are at least 19 fields in the 'message'
    if len(messages) >= 19:
        num_2_content = messages[1]  # Assuming this is your aggregator
        num_19_content = messages[18]  # Assuming this is where the error is

        # Increment the count for the specific error for the aggregator
        occurrences[num_2_content][num_19_content] += 1
        # Increment the aggregator total
        aggregator_totals[num_2_content] += 1

# Convert the defaultdict to a DataFrame
agg_df = pd.DataFrame.from_dict(occurrences, orient='index')
agg_df.reset_index(inplace=True)
agg_df.rename(columns={'index': 'Aggregator'}, inplace=True)

# Fill missing values with 0 and reset the index
agg_df.fillna(0, inplace=True)
agg_df.reset_index(drop=True, inplace=True)

# Add a "Total" column by merging with the aggregator totals
agg_df['Total'] = agg_df['Aggregator'].map(aggregator_totals)

# Calculate and add the Grand Total as a new row
grand_total = agg_df['Total'].sum()
agg_df.loc[len(agg_df)] = ['Grand Total'] + [agg_df[column].sum() for column in agg_df.columns[1:]]

# Prompt the user for the output file name
output_file = input("Enter the output CSV file name: ")
agg_df.to_csv(output_file, index=False)

print(f"Data has been processed and saved to '{output_file}'.")
