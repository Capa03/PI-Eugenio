import pandas as pd

# Load the Excel file
file_path = "C:\\Users\\tomas\\Downloads\\DadosTratados.xlsx"
df = pd.read_excel(file_path)

# Add the HappyCountry column based on the Happiness Score
df["HappyCountry"] = df["Happiness Score"].apply(lambda x: 1 if x > 6 else 0)

# Save the updated Excel file
output_path = "C:\\Users\\tomas\\Downloads\\DadosTratados2.xlsx"
df.to_excel(output_path, index=False)
