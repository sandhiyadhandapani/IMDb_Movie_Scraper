from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import pandas as pd
import time

# Chrome options
chrome_options = Options()
chrome_options.add_argument("--start-maximized")

# Launch Chrome
driver = webdriver.Chrome(options=chrome_options)

# Open IMDb Top 250 page
driver.get("https://www.imdb.com/chart/top/")

# Wait for page to load
time.sleep(5)

# Lists to store data
rank_list = []
movie_name_list = []
release_year_list = []
duration_list = []
rating_list = []

# Get all movie rows
movies = driver.find_elements(By.CSS_SELECTOR, "li.ipc-metadata-list-summary-item")

for index, movie in enumerate(movies, start=1):
    try:
        # Movie Name
        movie_name = movie.find_element(By.TAG_NAME, "h3").text

        # Metadata (Year, Duration)
        metadata = movie.find_elements(By.CSS_SELECTOR, "li.ipc-inline-list__item")

        print("Metadata:", [m.text for m in metadata])

        year = metadata[0].text if len(metadata) > 0 else "N/A"
        duration = metadata[1].text if len(metadata) > 1 else "N/A"

        # IMDb Rating
        try:
            rating = movie.find_element(
                By.CSS_SELECTOR,
                "span.ipc-rating-star--rating"
            ).text
        except:
            rating = "N/A"

        rank_list.append(index)
        movie_name_list.append(movie_name)
        release_year_list.append(year)
        duration_list.append(duration)
        rating_list.append(rating)

    except Exception as e:
        print(f"Error in movie {index}: {e}")

# Create DataFrame
df = pd.DataFrame({
    "Rank": rank_list,
    "Movie Name": movie_name_list,
    "Release Year": release_year_list,
    "Duration": duration_list,
    "IMDb Rating": rating_list
})

# Save CSV
df.to_csv("imdb_movies.csv", index=False)

print("\nCSV file created successfully!")
print(df.head())

driver.quit()