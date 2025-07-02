# End-to-End-News-Sentiment-Pipeline-AWS-Streamlit-
This project implements a fully automated, end-to-end news sentiment analysis pipeline using AWS cloud services and a Streamlit web application. It fetches real-time news headlines, analyzes sentiment using VADER (NLTK), stores results in Amazon S3 and PostgreSQL (RDS), and visualizes the insights in a responsive dashboard hosted via Docker and deployed on Amazon ECS Fargate.

# ARCHITECTURE

![architecture](https://github.com/user-attachments/assets/cfd5872f-637a-4c11-9d3a-ea6693db25bd)

# OVERVIEW
# 1.Fetches news articles from an API every 5 minutes and Analyzes the sentiment of each article

The system automatically collects the latest news articles every 5 minutes. This is done using AWS EventBridge, which triggers a Lambda function at regular intervals. When triggered, the function connects to NewsAPI and retrieves recent headlines, descriptions, sources, and timestamps. After fetching the articles, the function performs sentiment analysis using the VADER model from the NLTK library to determine whether each article is positive, negative, or neutral.

![2 0](https://github.com/user-attachments/assets/ac89e50f-b570-4963-82ae-a5973bec1dae)
![1 0](https://github.com/user-attachments/assets/ae7625fd-afed-41ff-a958-9c05d422c31a)
![4 0](https://github.com/user-attachments/assets/71973838-d41a-48bb-9cb4-48a1b3fc65cb)

# 2.Inserting Sentiment-Tagged News into PostgreSQL (RDS) via Lambda
A Lambda function that reads JSON files containing sentiment-analyzed news articles from an S3 bucket is created. For each article, it extracts the title, source, timestamp, and VADER sentiment score, then classifies the sentiment as Positive, Negative, or Neutral. It inserts the processed data into a PostgreSQL RDS table called news_articles, while avoiding duplicates using a unique constraint on title, published date, and source. After successful insertion, the Lambda deletes the processed file from S3 to prevent reprocessing.

![3 0](https://github.com/user-attachments/assets/114178b7-4125-48b9-bf6e-aedcafbd57d5)
![5 0](https://github.com/user-attachments/assets/e2f4cd7a-674b-4b89-b795-c0705bb1d697)




