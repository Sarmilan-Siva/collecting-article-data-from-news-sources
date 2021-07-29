# Collecting Article Data From News Sources For Analysis

This Repository is to collect article data from various news sources such as New York Times, Guardian, etc. for Natural Language analysis purposes. The text data collected in various formats are processed and saved in tabular format for easy consumption.

## News Sources

* NYT archive articles - [Official documentation](https://developer.nytimes.com/docs/archive-product/1/overview)


## How to Use

### NYT Archive

Run `GetArticlesNYT.py` which contains all necessary functions to extract data from NYT archive. `get_articles()` saves the final table as .csv month wise inside the folder specified in the function.

Following codes explains how the function can be used.

```python
from GetArticlesNYT import get_articles

get_articles(start_date='2021-03-01',
             end_date='2021-03-01',
             api_key=API_KEY,
             file_path = 'NYT_2021')

```


## Files

* GetArticlesNYT.py - This Python file contains all necessary functions to call the NYT archive API, receive the data and to parse all necessary information into a table and download them as .csv files.

* NYT_archive_data.ipynb - Explains how all the functions are builts. It also shows some intermediate outcomes to give more visibility to the data formats and fields that are available in the archive.



