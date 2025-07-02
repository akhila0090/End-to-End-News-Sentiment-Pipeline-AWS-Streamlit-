# End-to-End News Sentiment Pipeline (AWS + Streamlit)
This project implements a fully automated, end-to-end news sentiment analysis pipeline using AWS cloud services and a Streamlit web application. It fetches real-time news headlines, analyzes sentiment using VADER (NLTK), stores results in Amazon S3 and PostgreSQL (RDS), and visualizes the insights in a responsive dashboard hosted via Docker and deployed on Amazon ECS Fargate.

##  OVERVIEW

This project provides a real-time news sentiment analysis dashboard that:

Fetches news articles from an API every 5 minutes

Analyzes the sentiment of each article

Stores the analyzed results

Presents insights through an interactive Streamlit dashboard

##  ARCHITECTURE

![architecture](https://github.com/user-attachments/assets/cfd5872f-637a-4c11-9d3a-ea6693db25bd)


##  1.Creating the NewsAPI Key

To access news data, sign up at NewsAPI.org and generate a free API key. Store this key securely as an environment variable for Lambda config for AWS to authenticate your API requests.

##  2.Fetches news articles from an API every 5 minutes and Analyzes the sentiment of each article

The system automatically collects the latest news articles every 5 minutes. This is done using AWS EventBridge, which triggers a Lambda function at regular intervals. When triggered, the function connects to NewsAPI and retrieves recent headlines, descriptions, sources, and timestamps. After fetching the articles, the function performs sentiment analysis using the VADER model from the NLTK library to determine whether each article is positive, negative, or neutral.

![1 0](https://github.com/user-attachments/assets/ae7625fd-afed-41ff-a958-9c05d422c31a)


![4 0](https://github.com/user-attachments/assets/71973838-d41a-48bb-9cb4-48a1b3fc65cb)

##  3.Inserting Sentiment-Tagged News into PostgreSQL (RDS) via Lambda
A Lambda function that reads JSON files containing sentiment-analyzed news articles from an S3 bucket is created. For each article, it extracts the title, source, timestamp, and VADER sentiment score, then classifies the sentiment as Positive, Negative, or Neutral. It inserts the processed data into a PostgreSQL RDS table called news_articles, while avoiding duplicates using a unique constraint on title, published date, and source. After successful insertion, the Lambda deletes the processed file from S3 to prevent reprocessing.

![3 0](https://github.com/user-attachments/assets/114178b7-4125-48b9-bf6e-aedcafbd57d5)

view of table in dbeaver

![5 0](https://github.com/user-attachments/assets/e2f4cd7a-674b-4b89-b795-c0705bb1d697)

##  4.Visualize with Streamlit Dashboard
The Streamlit dashboard (app.png) connects to the RDS database and displays sentiment-labeled news in a color-coded table— Green (Positive), Red (Negative), and White (Neutral)

![7 0](https://github.com/user-attachments/assets/b61298aa-4531-4e15-8465-62d591599ffb)


![6 0](https://github.com/user-attachments/assets/819bebf2-4685-4ec8-8365-460d962a1794)

## 5.Containerize the App with Docker
The Streamlit app is containerized using Docker with the help of a Dockerfile and requirements.txt, ensuring all dependencies are packaged for consistent deployment. The Docker image is then pushed to an Amazon ECR repository, making it ready for deployment on ECS Fargate.

![8 0](https://github.com/user-attachments/assets/0fa0bd0f-7273-43e6-b371-438d3a2e9369)


![9 0](https://github.com/user-attachments/assets/f6fc3f41-f59e-4033-a7b6-f7a62699eb97)


## 6.Deploy to AWS ECS Fargate
The Docker container is deployed to AWS ECS Fargate, which automatically manages scaling and infrastructure, making the Streamlit dashboard easy to run without managing any servers.

![10 0](https://github.com/user-attachments/assets/355a338b-a36d-453f-b0c2-0b1432d4503e)


![11 0](https://github.com/user-attachments/assets/05b3c575-627a-4b9a-8328-4bc4fb51f33d)

Final Dashboard

![12 0](https://github.com/user-attachments/assets/7e8d878a-07c0-4ee2-82ec-048db654b949)



