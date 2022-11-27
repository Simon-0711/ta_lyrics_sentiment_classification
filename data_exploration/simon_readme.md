# Data Exploration
For our project we chose to use the lyrics and artist dataset from kaggle (https://www.kaggle.com/datasets/neisse/scrapped-lyrics-from-6-genres?select=lyrics-data.csv) containing songs from 79 musical genres.
Let's take a closer look at the data sets provided.

## Lyrics Dataset
The lyrics dataset contains lyrics of a number of songs, as well as some metadata.
First of all let's look at the contained languages: <br>

<img src="images/language_distribution.png" width="600"/>
<br>


As you can seen in the distribution, most songs in the dataset are either written in english or portugese. Overall, 53 languages are existing in the dataset itelf. However as stated before, only portugese and english make up a relevant part of the data. We will limit the project to english songs, as this simplifies the mood calssification signifficantly.

After filtering the lyrics dataset to english we need to look at the general information about the data, such as number of rows, contained columns, non-null count, datatypes, etc.: 
There are 191814 rows and 5 columns in the filtered df.
The following image shows the contained columns and there Non-Null value counts. 

<img src="images/lyrics_info.png" width="300"/>

Let's take a look at the first 10 lines in order to get an understanding of what is contained in the data set. 

<img src="images/lyrics_head.png" width="600"/>

As we can see,
- **ALink** contains a link representation to the corresponding artist
- **SName** contains the name of the song
- **SLink** contians the link representation of the song name 
- **Lyric** contains the lyrics of each song
- **language** contains the language of the lyrics


## Artist Dataset
The artist dataset contains a list of artists and some metadata. 
The unfiltered dataset contains 4168 rows and 5 columns. 

The following image shows the contained columns and there Non-Null value counts. 

<img src="images/artist_info.png" width="300"/>

Let's take a look at the first 10 lines in order to get an understanding of what is contained in the data set. 

<img src="images/artist_head.png" width="600"/>

As we can see,
- **Artist** contains the name of the artist
- **Genres** contains gneres of the artist's songs
- **Songs** contians number of songs of the artist
- **Popularity** contains rating/popularity of the artist
- **Link** contains a link representation to the corresponding artist (same as ALink from lyrics data)


## Analysis 
After merging lyrics and artist data on the ALink and Link, let's take a closer look at what is contained in the data in order to get a better understanding of what we are working with. 

### Song counts per artist
The following figure shows the distribution of song counts per artist. 

<img src="images/song_count_per_artist.png" width="600"/>
<img src="images/artist_song_boxplot.png" width="600"/>

As we can see, 50% of artists have between 0 and 200 songs associated with them, with a median = 82 and mean = 104.994.


### Genres
Let's take a look at the genres in the dataset and their distribution. 
The following figures show the total appearance (count) of songs per genre for all genres as well as the top 20 genres. 

<img src="images/genre_count.png" width="1000"/>
<img src="images/genre_count_zoomed.png" width="600"/>

As we can see, some genres are displayed twice, such as Pop. this is something we need to keep in mind for the data preprocessing steps in order to clean the data appropriatly. 

### Popularity
The popularity is also provided in the datasets. Let's see, if the count of songs per genre correlates with the popularity of the genres. 
<img src="images/popularity_per_genre.png" width="1000"/>

As we can see, the popularity does not correlate with the amount of songs per genre, since piano rock and soft rock seam to be the most popular. 
This popularity per genre is another aspect to keep in mind for the preprocessing. 

Also let's look at the popularity per artist, to get a feeling of the most popular artists in the dataset. As we can see, beyonce, sia, anitta, adele, eminem and ed-sheeran are by far the most popular artists. 
<img src="images/popularity_per_artist.png" width="1000"/>



### Average word count per song
Another interesting metric is to look at is the length of the songs, as depicted in the following graphics:

<img src="images/gaussian_wordcount.png" width="600"/>
<img src="images/median_wordcount.png" width="600"/>

As you can see, there is quite a variance in the dataset overall. The minimum value is 1, whereas the maximum value is 3422. 
However, as you can also see, 50% of the songs have a wordcount of roughly 200 - 300 words per song, with a variance reaching from 1 to ~500, so the variance drastically decreases there, compared to the overall data.
The average of the ammount of words in a song is about 250, the median is at 211.

### Analyzing the CNN keywords

Since this project relies on the CNN provided by (https://github.com/workmanjack/lyric-mood-classification), it is useful, to take a look at their labeling technique. 
They used overall 18 different moods with customly set keywords, which indicate that on a given song a mood is represented. The following graphic depicts the moods and their keywords:

<img src="images/moods.png" width="600"/>

If we know take a look at the occurences of these keywords in our songtexts, we get this overall distribution:

<img src="images/keywords.png" width="600"/>

As you can see, most of the songs are "depressed", followed by "desire" and "anger", according to the occurences of keywords, introduced by our baseline project.
If we know take a look at the overall classification of songs according to the keyword occurences, we get these 2 graphs:

<img src="images/relative_keywords.png" width="600"/>
<img src="images/mood_classification.png" width="600"/>

These show us, that overall many songs could not be labeled correctly, harnessing the keywords of our baseline project. 
This leads to the assumption that either, we would need to adjust the keywords so that we can label more songs overall, or that factors like stemming will play an important role for this project, to increase the number of lableable songs. The consideration and implementation of these 2 is part of the preprocessing and won't be discussed furthere here. 


### Weird Artist Names
One last thing to consider for preprocessing are some of the artist names. 
As seen in the following figure, artist names also include movie titles. This needs to be filtered in some way during the preprocessing. 

<img src="images/weird_artist_names.png" width="300"/>
