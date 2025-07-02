import json
import os
import re
import requests
import boto3
from datetime import datetime
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

s3 = boto3.client('s3')
analyzer = SentimentIntensityAnalyzer()

# to clean HTML, URLs, non-ASCII chars
def clean_text(text):
    if not text:
        return ""
    text = re.sub(r'<.*?>', '', text)
    text = re.sub(r'http\S+|www\.\S+', '', text)
    text = text.encode('ascii', 'ignore').decode('ascii')
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def lambda_handler(event, context):
    
    api_key = os.environ.get('api_key')
    if not api_key:
        return {"statusCode": 500, "error": "Missing API key"}

    
    url = (
        f"https://newsapi.org/v2/everything?q=*"
        f"&language=en&pageSize=20&sortBy=publishedAt&apiKey={api_key}"
    )

    # Fetch data
    try:
        response = requests.get(url)
        response.raise_for_status()
        articles = response.json().get("articles", [])
    except Exception as e:
        return {"statusCode": 500, "error": f"Error fetching data: {str(e)}"}

    formatted_data = []

    for i, article in enumerate(articles, start=1):
        title = clean_text(article.get("title", ""))
        description = clean_text(article.get("description", ""))
        source = article.get("source", {}).get("name", "")
        published_at = article.get("publishedAt", "")

        # Convert to datetime format
        try:
            dt = datetime.fromisoformat(published_at.replace('Z', '+00:00'))
            published_at_fmt = dt.strftime("%d/%m/%Y - %H:%M")
        except:
            published_at_fmt = published_at

        # Combine text for sentiment
        combined_text = f"{title} {description}".strip()
        sentiment = analyzer.polarity_scores(combined_text)

        # Append formatted record
        formatted_data.append({
            "S.No": i,
            "VADER_Positive": sentiment['pos'],
            "VADER_Negative": sentiment['neg'],
            "VADER_Compound": sentiment['compound'],
            "Title": title,
            "Source": source,
            "Description": description,
            "PublishedAt": published_at_fmt
        })

    #  Upload to S3
    try:
        bucket_name = "newsdata-akhila"
        folder = "sentiment_news/"
        timestamp = datetime.now().strftime("%Y-%m-%dT%H-%M-%S")
        filename = f"news_sentiment_{timestamp}.json"
        key = f"{folder}{filename}"

        s3.put_object(
            Bucket=bucket_name,
            Key=key,
            Body=json.dumps(formatted_data, indent=2),
            ContentType='application/json'
        )
    except Exception as e:
        return {"statusCode": 500, "error": f"Error uploading to S3: {str(e)}"}

    return {
        "statusCode": 200,
        "message": f"Sentiment-enhanced news uploaded to s3://{bucket_name}/{key}",
        "article_count": len(formatted_data)
    }
