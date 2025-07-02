# End-to-End-News-Sentiment-Pipeline-AWS-Streamlit-
This project implements a fully automated, end-to-end news sentiment analysis pipeline using AWS cloud services and a Streamlit web application. It fetches real-time news headlines, analyzes sentiment using VADER (NLTK), stores results in Amazon S3 and PostgreSQL (RDS), and visualizes the insights in a responsive dashboard hosted via Docker and deployed on Amazon ECS Fargate.

# ARCHITECTURE

![architecture](https://github.com/user-attachments/assets/cfd5872f-637a-4c11-9d3a-ea6693db25bd)


#1.Creating Lambda Functions

#1.extraction-news
- Pulls data from News API
- Cleans text and computes sentiment using `vaderSentiment`
- Saves original article JSON to S3
- Invoked via EventBridge every 5 minutes

# 2.news-to-rds
- Triggered in production via S3 events
- Reads cleaned JSONs from S3
- Inserts sentiment-analyzed data into RDS table
- 
![2 0](https://github.com/user-attachments/assets/82276bcc-bd05-42e7-a184-6961e2ab071c)
