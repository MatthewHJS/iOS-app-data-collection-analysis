import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import CountVectorizer

apps_df = pd.read_csv('all_apps.csv')

most_parents_collection = [1608789604, 6479435323, 6446139013, 1643294506, 1643294506, 1643294506, 1600367795, 1608789604, 1605388852, 1543581137, 1611978184, 1370599950, 1172501360, 1611978184, 1597279982, 1605388852, 1546598842, 1608789604, 1611978184, 1643294506, 1643294506, 1172501360, 1608789604, 1611978184, 1611978184, 1643294506, 1643294506, 1608789604, 1611978184, 1605388852, 1643294506, 1643294506, 1608789604, 1608789604, 1605388852, 1643294506, 1643294506, 1608789604, 1611978184, 1611978184, 1643294506, 1605388852, 1370599950, 1611978184, 1643294506, 1605388852, 1605388852, 1608789604, 1611978184, 1643294506, 1605388852, 1172501360, 1608789604, 1611978184, 1605388852, 1643294506, 1643294506, 1608789604, 1611978184, 1643294506, 1605388852, 1605388852, 1608789604, 1611978184, 1643294506, 1605388852, 1605388852, 1608789604, 1611978184, 1605388852, 1643294506, 1172501360, 1370599950, 1611978184, 1611978184, 1605388852, 1643294506, 1608789604, 1600367795, 1611978184, 1172501360, 1629904853, 1608789604, 1611978184, 1643294506, 1643294506, 1605757785, 1608789604, 1611978184, 1643294506, 1605388852, 1629371699, 1608789604, 1611978184, 1605388852, 1643294506, 1644160969, 1608789604, 1611978184, 1643294506, 1605388852, 1575419096, 1608789604, 1611978184, 1605388852, 1643294506, 1606868055, 1608789604, 1643294506, 1611978184, 1605388852, 1636100189, 1608789604, 1611978184, 1643294506, 1568434949, 1172501360, 1550483828, 1611978184, 1611978184, 1643294506, 1172501360, 1608789604, 1611978184, 1643294506, 1643294506, 1172501360, 1370599950, 1611978184, 1643294506, 1605388852, 1370599950, 1608789604, 1608789604, 1643294506, 1605388852, 1608789604, 1608789604, 1611978184, 1643294506, 1605388852]

collections_data = []
with open('collections.csv', 'r') as file:
    for line in file:
        collections_data.append(line.strip().split(','))

collections_df = pd.DataFrame(collections_data)

def convert_size(size):
    try:
        if 'KB' in size:
            return float(size.replace(' KB', '')) / 1024  
        elif 'MB' in size:
            return float(size.replace(' MB', ''))
        elif 'GB' in size:
            return float(size.replace(' GB', '')) * 1024  
    except:
        return None  

apps_df['App Size (MB)'] = apps_df['App Size'].apply(convert_size)
collections_df.dropna(how='all', inplace=True) 

#####################################################################################
##                             Most Parents Analysis                               ##
#####################################################################################

most_parents_collection_df = apps_df[apps_df['App ID'].isin(most_parents_collection)]

# Distribution by App Category
category_distribution = most_parents_collection_df['App Category'].value_counts()
plt.figure(figsize=(12, 8))
category_distribution.plot(kind='pie', autopct='%1.1f%%', startangle=140, colors=plt.cm.Paired.colors)
plt.title('Distribution of App Categories in Most Parents Collection')
plt.ylabel('')
plt.tight_layout()
plt.show()

# Distribution by App Size
size_distribution = most_parents_collection_df['App Size (MB)'].dropna()
plt.figure(figsize=(12, 8))
sns.boxplot(y=size_distribution, color='c')
plt.title('Distribution of App Sizes in Most Parents Collection')
plt.ylabel('App Size (MB)')
plt.grid(True)
plt.tight_layout()
plt.show()

# Distribution by App Languages
languages_exploded = most_parents_collection_df['App Languages'].str.split(', ').explode()
language_distribution = languages_exploded.value_counts().head(20)
plt.figure(figsize=(12, 8))
language_distribution.plot(kind='bar')
plt.title('Distribution of App Languages in Most Parents Collection (Top 20)')
plt.xlabel('App Languages')
plt.ylabel('Number of Apps')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()

# Distribution by Age
age_rating_distribution = most_parents_collection_df['App Age Rating'].value_counts()
filtered_age_rating_distribution = age_rating_distribution.loc[['4+', '12+', '9+']]
plt.figure(figsize=(10, 6))
filtered_age_rating_distribution.plot(kind='bar', color='skyblue')
plt.title('Distribution of App Age Ratings in Most Parents Collection')
plt.xlabel('App Age Rating')
plt.ylabel('Number of Apps')
plt.xticks(rotation=0)
plt.tight_layout()
plt.show()

# Keyword Extraction Using NLP
app_names = most_parents_collection_df['App Name']
vectorizer = CountVectorizer(stop_words='english', max_features=40)
X = vectorizer.fit_transform(app_names)
keywords = vectorizer.get_feature_names_out()
keyword_counts = X.toarray().sum(axis=0)

valid_keywords_df = pd.DataFrame({'Keyword': keywords, 'Count': keyword_counts})
valid_keywords_df = valid_keywords_df[~valid_keywords_df['Keyword'].str.contains(r'[^a-zA-Z0-9 ]', regex=True)]
valid_keywords_df = valid_keywords_df.sort_values(by='Count', ascending=False).head(20)

plt.figure(figsize=(12, 8))
plt.barh(valid_keywords_df['Keyword'], valid_keywords_df['Count'], color='skyblue')
plt.xlabel('Frequency')
plt.title('Top 20 Keywords in Most Parents Collection App Names')
plt.gca().invert_yaxis()
plt.tight_layout()
plt.show()

print(valid_keywords_df)


##############################################################################
##                            Dimention Analysis                            ##
##############################################################################

# Distribution by App Category
category_distribution = apps_df['App Category'].value_counts()
category_percentage = (category_distribution / category_distribution.sum()) * 100
filtered_distribution = category_distribution[category_percentage >= 1]
filtered_percentage = (filtered_distribution / filtered_distribution.sum()) * 100
plt.figure(figsize=(12, 8))
filtered_distribution.plot(kind='pie', autopct='%1.1f%%', startangle=140, colors=plt.cm.Paired.colors)
plt.title('Distribution of Apps by Category')
plt.ylabel('')
plt.tight_layout()
plt.show()
print(category_percentage)


# Distribution by App Languages
languages_exploded = apps_df['App Languages'].str.split(', ').explode()
language_distribution = languages_exploded.value_counts().head(20)
plt.figure(figsize=(12, 8))
language_distribution.plot(kind='bar')
plt.title('Distribution of Apps by Language (Top 20)')
plt.xlabel('App Languages')
plt.ylabel('Number of Apps')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()
language_distribution = apps_df['App Languages'].value_counts()
language_percentage = (language_distribution / language_distribution.sum()) * 100
print(language_distribution)
print(language_percentage)

# Distribution by App Size
size_distribution = apps_df['App Size (MB)'].dropna()
plt.figure(figsize=(12, 8))
sns.boxplot(y=size_distribution, color='c')
plt.title('Distribution of App Sizes')
plt.ylabel('App Size (MB)')
plt.yscale('log')
plt.grid(True)
plt.tight_layout()
plt.show()

# Distribution by Age
age_rating_distribution = apps_df['App Age Rating'].value_counts()
filtered_age_rating_distribution = age_rating_distribution.loc[['4+', '17+', '12+', '9+']]
plt.figure(figsize=(10, 6))
filtered_age_rating_distribution.plot(kind='bar', color='skyblue')
plt.title('Distribution of Apps by Age Rating')
plt.xlabel('App Age Rating')
plt.ylabel('Number of Apps')
plt.xticks(rotation=0)
plt.tight_layout()
plt.show()
age_percentage = (age_rating_distribution / age_rating_distribution.sum()) * 100
print(age_percentage)


##################################################################################################
##                                  Largest Collection Analysis                                 ##
##################################################################################################

largest_collection_idx = collections_df.apply(lambda x: x.count(), axis=1).idxmax()
largest_collection = collections_df.iloc[largest_collection_idx].dropna().astype(str).tolist()
largest_collection_df = apps_df[apps_df['App ID'].astype(str).isin(largest_collection)]
largest_collection_category_distribution = largest_collection_df['App Category'].value_counts()
print(len(largest_collection))

# Distribution of App Categories
plt.figure(figsize=(12, 8))
largest_collection_category_distribution.plot(kind='pie', autopct='%1.1f%%', startangle=140, colors=plt.cm.Paired.colors)
plt.title('Distribution of App Categories in the Largest Collection')
plt.ylabel('')
plt.tight_layout()
plt.show()

largest_collection_names = largest_collection_df['App Name']
vectorizer_largest_collection = CountVectorizer(stop_words='english', max_features=40)  # Extract more keywords to ensure we get the top 20 valid ones
X_largest_collection = vectorizer_largest_collection.fit_transform(largest_collection_names)
keywords_largest_collection = vectorizer_largest_collection.get_feature_names_out()
keyword_counts_largest_collection = X_largest_collection.toarray().sum(axis=0)
valid_keywords_largest_collection_df = pd.DataFrame({'Keyword': keywords_largest_collection, 'Count': keyword_counts_largest_collection})
valid_keywords_largest_collection_df = valid_keywords_largest_collection_df[~valid_keywords_largest_collection_df['Keyword'].str.contains(r'[^a-zA-Z0-9 ]', regex=True)]
valid_keywords_largest_collection_df = valid_keywords_largest_collection_df.sort_values(by='Count', ascending=False).head(20)
valid_keywords_largest_collection_df = valid_keywords_largest_collection_df[~valid_keywords_largest_collection_df['Keyword'].str.contains(r'[^a-zA-Z]', regex=True)]
plt.figure(figsize=(12, 8))
plt.barh(valid_keywords_largest_collection_df['Keyword'], valid_keywords_largest_collection_df['Count'], color='skyblue')
plt.xlabel('Frequency')
plt.title('Top 20 Keywords in Largest Collection App Names')
plt.gca().invert_yaxis() 
plt.tight_layout()
plt.show()

print(valid_keywords_largest_collection_df)


# Keyword Extraction Using NLP

app_names = apps_df['App Name']
vectorizer = CountVectorizer(stop_words='english', max_features=40) 
X = vectorizer.fit_transform(app_names)
keywords = vectorizer.get_feature_names_out()
keyword_counts = X.toarray().sum(axis=0)


'''

Some keywords were not readable, maybe because they included chinese characters and the encoding is english, i decided to filter
them out as i wouldnt be able to read them anyways 
    
'''
valid_keywords_df = pd.DataFrame({'Keyword': keywords, 'Count': keyword_counts})
valid_keywords_df = valid_keywords_df[~valid_keywords_df['Keyword'].str.contains(r'[^a-zA-Z0-9 ]', regex=True)]
valid_keywords_df = valid_keywords_df.sort_values(by='Count', ascending=False).head(20)
valid_keywords_df = valid_keywords_df[~valid_keywords_df['Keyword'].str.contains(r'[^a-zA-Z]', regex=True)]

plt.figure(figsize=(12, 8))
plt.barh(valid_keywords_df['Keyword'], valid_keywords_df['Count'], color='skyblue')
plt.xlabel('Frequency')
plt.title('Top 20 Keywords in App Names')
plt.gca().invert_yaxis()  # Invert y-axis to show the highest count on top
plt.tight_layout()
plt.show()

print(valid_keywords_df)

# Top 20 Keywords in the "Games" Category
games_names = apps_df[apps_df['App Category'] == 'Games']['App Name']
vectorizer_games = CountVectorizer(stop_words='english', max_features=40)
X_games = vectorizer_games.fit_transform(games_names)
keywords_games = vectorizer_games.get_feature_names_out()
keyword_counts_games = X_games.toarray().sum(axis=0)
valid_keywords_games_df = pd.DataFrame({'Keyword': keywords_games, 'Count': keyword_counts_games})
valid_keywords_games_df = valid_keywords_games_df[~valid_keywords_games_df['Keyword'].str.contains(r'[^a-zA-Z0-9 ]', regex=True)]
valid_keywords_games_df = valid_keywords_games_df.sort_values(by='Count', ascending=False).head(20)
valid_keywords_games_df = valid_keywords_games_df[~valid_keywords_games_df['Keyword'].str.contains(r'[^a-zA-Z]', regex=True)]

plt.figure(figsize=(12, 8))
plt.barh(valid_keywords_games_df['Keyword'], valid_keywords_games_df['Count'], color='lightgreen')
plt.xlabel('Frequency')
plt.title('Top 20 Keywords in "Games" App Names')
plt.gca().invert_yaxis()
plt.tight_layout()
plt.show()

print(valid_keywords_games_df)

# Top 20 Keywords in the "Photo & Video" Category
photo_video_names = apps_df[apps_df['App Category'] == 'Photo & Video']['App Name']
vectorizer_photo_video = CountVectorizer(stop_words='english', max_features=40)
X_photo_video = vectorizer_photo_video.fit_transform(photo_video_names)
keywords_photo_video = vectorizer_photo_video.get_feature_names_out()
keyword_counts_photo_video = X_photo_video.toarray().sum(axis=0)
valid_keywords_photo_video_df = pd.DataFrame({'Keyword': keywords_photo_video, 'Count': keyword_counts_photo_video})
valid_keywords_photo_video_df = valid_keywords_photo_video_df[~valid_keywords_photo_video_df['Keyword'].str.contains(r'[^a-zA-Z0-9 ]', regex=True)]
valid_keywords_photo_video_df = valid_keywords_photo_video_df.sort_values(by='Count', ascending=False).head(20)
valid_keywords_photo_video_df = valid_keywords_photo_video_df[~valid_keywords_photo_video_df['Keyword'].str.contains(r'[^a-zA-Z]', regex=True)]

plt.figure(figsize=(12, 8))
plt.barh(valid_keywords_photo_video_df['Keyword'], valid_keywords_photo_video_df['Count'], color='lightcoral')
plt.xlabel('Frequency')
plt.title('Top 20  Keywords in "Photo & Video" App Names')
plt.gca().invert_yaxis()
plt.tight_layout()
plt.show()

print(valid_keywords_photo_video_df)


##################################################################################
##                         Comparison Between Two Collections                   ##
##################################################################################


collection_1_idx = largest_collection_idx  
collection_2_idx = 2

collection_1 = collections_df.iloc[collection_1_idx].dropna().astype(str).tolist()
collection_2 = collections_df.iloc[collection_2_idx].dropna().astype(str).tolist()

# Filter apps in the two collections
collection_1_df = apps_df[apps_df['App ID'].astype(str).isin(collection_1)]
collection_2_df = apps_df[apps_df['App ID'].astype(str).isin(collection_2)]

# Collection 1: Genre Distribution
collection_1_category_distribution = collection_1_df['App Category'].value_counts()
plt.figure(figsize=(12, 8))
collection_1_category_distribution.plot(kind='bar', color='skyblue')
plt.title('Genre Distribution in Collection 1')
plt.xlabel('App Category')
plt.ylabel('Number of Apps')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()

print("Collection 1 Category Distribution:")
print(collection_1_category_distribution)

# Collection 1: Keywords
collection_1_names = collection_1_df['App Name']
vectorizer_collection_1 = CountVectorizer(stop_words='english', max_features=40)
X_collection_1 = vectorizer_collection_1.fit_transform(collection_1_names)
keywords_collection_1 = vectorizer_collection_1.get_feature_names_out()
keyword_counts_collection_1 = X_collection_1.toarray().sum(axis=0)
valid_keywords_collection_1_df = pd.DataFrame({'Keyword': keywords_collection_1, 'Count': keyword_counts_collection_1})
valid_keywords_collection_1_df = valid_keywords_collection_1_df[~valid_keywords_collection_1_df['Keyword'].str.contains(r'[^a-zA-Z0-9 ]', regex=True)]
valid_keywords_collection_1_df = valid_keywords_collection_1_df.sort_values(by='Count', ascending=False).head(20)

plt.figure(figsize=(12, 8))
plt.barh(valid_keywords_collection_1_df['Keyword'], valid_keywords_collection_1_df['Count'], color='skyblue')
plt.xlabel('Frequency')
plt.title('Top 20 Keywords in Collection 1 App Names')
plt.gca().invert_yaxis()
plt.tight_layout()
plt.show()

print("Top 20 Keywords in Collection 1:")
print(valid_keywords_collection_1_df)

# Collection 2: Genre Distribution
collection_2_category_distribution = collection_2_df['App Category'].value_counts()
plt.figure(figsize=(12, 8))
collection_2_category_distribution.plot(kind='bar', color='orange')
plt.title('Genre Distribution in Collection 2')
plt.xlabel('App Category')
plt.ylabel('Number of Apps')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()

print("Collection 2 Category Distribution:")
print(collection_2_category_distribution)

# Collection 2: Keywords
collection_2_names = collection_2_df['App Name']
vectorizer_collection_2 = CountVectorizer(stop_words='english', max_features=40)
X_collection_2 = vectorizer_collection_2.fit_transform(collection_2_names)
keywords_collection_2 = vectorizer_collection_2.get_feature_names_out()
keyword_counts_collection_2 = X_collection_2.toarray().sum(axis=0)
valid_keywords_collection_2_df = pd.DataFrame({'Keyword': keywords_collection_2, 'Count': keyword_counts_collection_2})
valid_keywords_collection_2_df = valid_keywords_collection_2_df[~valid_keywords_collection_2_df['Keyword'].str.contains(r'[^a-zA-Z0-9 ]', regex=True)]
valid_keywords_collection_2_df = valid_keywords_collection_2_df.sort_values(by='Count', ascending=False).head(20)

plt.figure(figsize=(12, 8))
plt.barh(valid_keywords_collection_2_df['Keyword'], valid_keywords_collection_2_df['Count'], color='orange')
plt.xlabel('Frequency')
plt.title('Top 20 Keywords in Collection 2 App Names')
plt.gca().invert_yaxis()
plt.tight_layout()
plt.show()
