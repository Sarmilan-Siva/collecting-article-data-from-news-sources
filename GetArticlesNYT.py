## This is to extract article data from NYTs archive and return them in tabular formS

# importing necessary libraries
import pandas as pd
import numpy as np
import json
import requests
import time
import os

# simple extractor function
def send_request(yr, month, api_key):
  '''Sends a request to the NYT Archive API for a given year and month, and receive the response'''
    
  base_url = 'https://api.nytimes.com/svc/archive/v1'
  full_url = base_url + '/' + yr + '/' + month + '.json?api-key=' + api_key
    
  try:
    response = requests.get(full_url).json()
  except Exception:
    return None
  return response
  
## followings are additional functions to support and make main function more efficient
def manage_missing_fields(doc_field, article):
  ''' some fields are not available in some dictionaries; making sure those fields are available otherwise assign nan '''
  if doc_field in article:
    value = article[doc_field]
  else:
    value = np.nan
  return value

def is_main(article):
  ''' making sure the headline has main in it '''
  is_true = type(article['headline']) == dict and 'main' in article['headline'].keys()

  return is_true

def extracting_headline(article):
  ''' extracting main of the headline if it is available '''
  if is_main(article):
    value = article['headline']['main']
  else:
    value = np.nan
  return value

def writer_name(article):
  ''' checking whether the writer name is there and return it in First Name, Middle Name, Last Name format'''
  writer_detail = article['byline']['person'] 
  is_true = len(writer_detail) > 0 and type(writer_detail[0]) == dict and 'firstname' in writer_detail[0].keys()

  if is_true:
    firstname = writer_detail[0]['firstname']
    lastname = writer_detail[0]['lastname']
    middlename = writer_detail[0]['middlename']

    FullName = firstname + (" " + middlename if middlename else "") + " " + lastname

  else:
    FullName = None

  return FullName

def keyword_parser(keyword_type, article):
  ''' extracts keywords based on its type in a list'''
  kw_list = [keyword['value'] for keyword in article['keywords'] if keyword['name'] == keyword_type]
  return kw_list

# article parser
def article_parser(nyt_articles):
  ''' parsing interested fields from NYT's archive response and return a tabular DataFrame '''
  
  # defining empty fields
  data = {'pub_date': [],
          'document_type':[],
          'news_desk':[],
          'section_name': [], 'subsection_name':[],
          'abstract': [], 'headline': [],
          'writer': [],
          'key_subject': [], 'key_glocations': [], 'key_persons': [], 'key_organizations': [], 
          'word_count':[],
          'web_url': []}

  articles = nyt_articles['response']['docs']

  for article in articles:
    data['abstract'].append(article['abstract'])
    data['headline'].append(extracting_headline(article))
    data['writer'].append(writer_name(article))
    data['document_type'].append(article['document_type'])
    data['news_desk'].append(article['news_desk'])
    data['key_subject'].append(keyword_parser('subject', article))
    data['key_glocations'].append(keyword_parser('glocations', article))
    data['key_persons'].append(keyword_parser('persons', article))
    data['key_organizations'].append(keyword_parser('organizations', article))
    data['section_name'].append(article['section_name'])
    data['subsection_name'].append(manage_missing_fields('subsection_name', article))
    data['pub_date'].append(pd.to_datetime(article['pub_date'], format='%Y%m%d %H:%M:%S.%f').date())
    data['web_url'].append(article['web_url'])
    data['word_count'].append(article['word_count'])
    
  df = pd.DataFrame(data)
  print('{} articles successfully parsed to the table'.format(len(articles)))
  
  return df
  
  
  ##---- main function -------
  
def get_articles(start_date, end_date, api_key, file_path):
  ''' request and receive articles for a date range and save them in a directory as .csv file '''
  
  # create file path
  if not os.path.exists(file_path):
    os.mkdir(file_path)
  
  # create possible Year - Month combinations
  ym_list = pd.date_range(start_date, end_date, freq='MS').strftime("%Y-%m").tolist()
  
  # make API calls for all year, month within the range interested
  for ym in ym_list:
    ym_spl = ym.split('-')
    
    csv_name = 'nyt_arc' + str(ym_spl[0]) + '-' + str(ym_spl[1]) + '.csv'
    csv_path = file_path + '/' + csv_name
    if os.path.exists(csv_path):
      print(csv_name + ' already exists \n')      
      
    else:
      nyt_articles = send_request(str(ym_spl[0]), str(int(ym_spl[1])), api_key)
      
      if nyt_articles is not None:
        df_article = article_parser(nyt_articles)
        
        df_article.to_csv(csv_path, index=False)
        time.sleep(5)
        print('Saving ' + csv_name + '\n')
        
  print('---- Completing parsing the articles ----')