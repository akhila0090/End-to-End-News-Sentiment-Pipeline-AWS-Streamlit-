import json
import boto3
import psycopg2
import os
from datetime import datetime

# Load environment variables from Lambda configuration
DB_HOST = os.environ['DB_HOST']
DB_NAME = os.environ['DB_NAME']
DB_USER = os.environ['DB_USER']
DB_PASS = os.environ['DB_PASS']
DB_PORT = os.environ.get('DB_PORT', '5432')
BUCKET_NAME = os.environ.get('BUCKET_NAME', 'newsdata-akhila')

def lambda_handler(event, context):
    s3 = boto3.client('s3')
    prefix = 'sentiment_news/'

    try:
        # Connect to PostgreSQL RDS
        conn = psycopg2.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASS,
            port=DB_PORT
        )
        cur = conn.cursor()

        # Create table with unique constraint
        cur.execute("""
            CREATE TABLE IF NOT EXISTS news_articles (
                id SERIAL PRIMARY KEY,
                published_at TIMESTAMP,
                source VARCHAR(255),
                sentiment_label VARCHAR(50),
                title TEXT,
                UNIQUE (title, published_at, source)
            );
        """)
        conn.commit()

        # Read all processed sentiment files
        response = s3.list_objects_v2(Bucket=BUCKET_NAME, Prefix=prefix)
        if 'Contents' not in response:
            return {"message": "No sentiment files found."}

        for obj in response['Contents']:
            key = obj['Key']
            if not key.endswith('.json'):
                continue

            file_obj = s3.get_object(Bucket=BUCKET_NAME, Key=key)
            json_data = json.loads(file_obj['Body'].read().decode('utf-8'))

            for item in json_data:
                title = item.get('Title', '')
                source = item.get('Source', '')
                published_at = parse_date(item.get('PublishedAt', ''))
                compound = item.get('VADER_Compound', 0.0)

                sentiment_label = classify_sentiment(compound)

                cur.execute("""
                    INSERT INTO news_articles (
                        published_at, source, sentiment_label, title
                    ) VALUES (%s, %s, %s, %s)
                    ON CONFLICT (title, published_at, source) DO NOTHING;
                """, (
                    published_at,
                    source,
                    sentiment_label,
                    title
                ))

            # Delete processed file after successful insert
            s3.delete_object(Bucket=BUCKET_NAME, Key=key)

        conn.commit()
        cur.close()
        conn.close()

        return {
            'statusCode': 200,
            'message': f"Data inserted into news_articles and deleted from {prefix}"
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'error': str(e)
        }

def parse_date(date_str):
    """Supports '28/06/2025 - 13:44' format and others."""
    if not date_str:
        return None
    for fmt in (
        '%d/%m/%Y - %H:%M',       # Your format
        '%Y-%m-%dT%H:%M:%SZ',
        '%Y-%m-%d %H:%M:%S',
        '%Y-%m-%dT%H:%M:%S'
    ):
        try:
            return datetime.strptime(date_str, fmt)
        except ValueError:
            continue
    return None

def classify_sentiment(score):
    """Returns sentiment label based on compound score."""
    if score >= 0.05:
        return "Positive"
    elif score <= -0.05:
        return "Negative"
    else:
        return "Neutral"
