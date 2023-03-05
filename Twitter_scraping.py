import snscrape.modules.twitter as sntwitter
import pandas as pd
import streamlit as st
import pymongo as pm


st.title("Twitter Scraping")

scraped_word = st.text_area("Scraped Word")
#scraped_date = st.text_area("Scraped Date")
scraped_data = st.slider("Scraped Data", min_value=1, max_value=3000, value=100, step=10)


tweets = []

def main():
  if st.button("Scrap data"): 
    scraper = sntwitter.TwitterSearchScraper(scraped_word)
    for tweet in scraper.get_items():
      data = [tweet.date,
              tweet.id, 
              tweet.url, 
              tweet.content, 
              tweet.user.username, 
              tweet.replyCount, 
              tweet.retweetCount, 
              tweet.lang, 
              tweet.source, 
              tweet.likeCount]
      tweets. append(data)
      if len(tweets)>=scraped_data:
        break
    
    tweet_DF = pd.DataFrame(tweets, columns =['Date','ID','URL',
                                          'Content','User_Name',
                                          'Replycount','Retweetcount',
                                          'Language','Source','LikeCount'])
    st.write(tweet_DF)
    client = pm.MongoClient("mongodb+srv://Gowtham_kg:Gowtham12345@cluster1.swkilwf.mongodb.net/?retryWrites=true&w=majority")
    mydb = client["scraptwitter"]
    mycol = mydb["twitter"]
    tweet_mongo = tweet_DF.to_dict("records")
    st.write(tweet_mongo)


    st.download_button(label='Download CSV', data = tweet_DF.to_csv(), file_name='Scraped_Data.csv', mime= 'text/csv')
    st.download_button(label='Download JSON', data = tweet_DF.to_csv(),file_name='Scraped_Data.json', mime= 'text/json')


    if st.button('Upload to MongoDB'):
      mycol.insert_many(tweet_mongo)

if __name__ == "__main__":
  main()