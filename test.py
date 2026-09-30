import pandas as pd

df = pd.read_csv("anime_dataset.csv")

# Cleaning unknown values
df["Anime_Name"] = df["Anime_Name"].replace("?", "Unknown")
df["Genre"] = df["Genre"].replace("?", "Unknown")
df["Studio"] = df["Studio"].replace("?", "Unknown")

print("Unknown values after cleaning:")
print((df == "Unknown").sum())

print("\nDataset shape:")
print(df.shape)

print("\nFirst 5 rows:")
print(df.head())


# Basic Analysis

print("\nAverage Score:")
print(df["Score"].mean())

print("\nAverage Episodes:")
print(df["Episodes"].mean())

print("\nTotal Anime Records:")
print(len(df))

print("\nUnique Anime:")
print(df["Anime_Name"].nunique())

print("\nUnique Genres:")
print(df["Genre"].nunique())

print("\nUnique Studios:")
print(df["Studio"].nunique())

print("\nGenre Distribution:")
print(df["Genre"].value_counts())

print("\nStudio Distribution:")
print(df["Studio"].value_counts())

print("\nRating Distribution:")
print(df["Rating"].value_counts())

print("\nAverage Score by Anime:")
anime_score = df.groupby("Anime_Name")["Score"].mean()
print(anime_score.sort_values(ascending=False))

print("\nAverage Score by Studio:")
studio_score = df.groupby("Studio")["Score"].mean()
print(studio_score.sort_values(ascending=False))