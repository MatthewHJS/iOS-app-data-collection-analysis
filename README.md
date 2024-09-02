# iOS App Data Collection and Analysis

This project involves collecting and analyzing data on iOS apps, with a specific focus on the mechanisms of the 'You Might Also Like' feature in the App Store. Using the Python library BeautifulSoup, I collected metadata from apps released on July 8th, 2023. The analysis categorizes apps, identifies similarities and differences, and seeks to understand the app recommendations based on dimensions such as genre, language, size, and age rating.

## Background

This project analyzes iOS apps and their recommendation relationships through three nodes: root (initially collected apps), leaf (children of the root), and leaf_leaf (children of leaf). By examining the apps that launched on July 8th, 2023, the project aims to discover patterns in recommendations and data distributions across various dimensions.

## Data Collection Methodology

I collected a list of app IDs from the Qimai Data Platform for apps launched on July 8th, 2023. Using this dataset (`collectedapps.csv`), I designed a web crawler in Python to gather the following metadata:

1. App name
2. APK size
3. Supported languages
4. Category
5. Recommended user age

The data was collected in three iterations:
- **Root Apps**: Metadata from the initially collected apps.
- **Leaf Apps**: Metadata from apps recommended by Root Apps.
- **Leaf Leaf Apps**: Metadata from apps recommended by Leaf Apps.

The web crawler utilized the Python libraries `requests` and `BeautifulSoup` to scrape and parse HTML data from the App Store. Due to the dynamic nature of app descriptions, I opted not to extract descriptions to prioritize runtime efficiency. The crawler used for the first iteration took approximately 20 minutes to gather metadata from 800 apps. For subsequent iterations, I implemented a concurrent solution using the `concurrent.futures` library to handle the increased data volume more efficiently.

## Dataset Description

The collected data is stored in three separate CSV files:
1. `root_apps.csv` (510 entries)
2. `leaf_apps.csv` (1,547 entries)
3. `leaf_leaf_apps.csv` (6,084 entries)

Duplicates were removed, and relationships are stored by appending the parent’s ID in the last column of each entry. I created two types of collections for analysis:
- **Direct Relationship Collections**: Grouping nodes connected directly (1,546 collections, average size: 12).
- **5 Same Recommendations**: Grouping nodes with at least five identical recommendations (4,890 collections, average size: 11).

## Data Analysis

For data analysis, I utilized the following Python libraries:
- **Matplotlib**: For data visualization.
- **Pandas**: For data manipulation and analysis.
- **Scikit-learn**: For keyword analysis using Natural Language Processing (NLP).

### Dimension Distributions

**Category:**  
The analysis revealed that the most dominant app categories are Games, Education, and Productivity, which together account for nearly 40% of the total distribution.

**Language:**  
English was the most dominant language, supported by 90% of the apps, with 63% supporting only English. Simplified Chinese was the second most common language.

**Size:**  
The average app size was approximately 102.75 MB, with most apps being relatively small and a few outliers significantly larger.

**Age Rating:**  
The most dominant age rating was 4+, covering 75% of the apps, followed by 17+, making up 13% of the total distribution.

### Keyword Analysis

Using NLP, the top three keywords across all apps were:
1. Simulator (187 instances)
2. Game (181 instances)
3. App (177 instances)

The keyword distribution aligns with the dominant app categories, particularly Games.

## Findings

### Largest Collection

The largest collection consisted of 83 apps. Analysis showed a diverse category distribution, with Shopping being the most dominant category in this collection. The collection also featured a lower average app size (~20 MB) compared to the overall average.

### Node With Most Parents

The node with the most parents was the app "Real Truck," recommended by 141 other apps. Analysis of these parent apps revealed common characteristics: all were Games, supported only English, had an average size of around 300 MB, and were related to simulation or transportation themes.

## Miscellaneous

One of the biggest challenges of this project was optimizing the runtime for data scraping. I implemented a concurrent solution using threads, which significantly reduced the runtime for subsequent iterations. Future improvements could include refactoring the code for scalability and readability.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
