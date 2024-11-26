import requests
import pandas as pd
from sentiment import sentiment
from datetime import datetime, timedelta
import urllib.parse

api_key = "ENTER API KEY"
num = 5

def fetch(query, from_date, to_date, api_key, page_size=100, max_pages=5):
    all_articles = []

    for page in range(1, max_pages + 1):
        url = (
            f"https://newsapi.org/v2/everything?"
            f"q={query}&"
            f"from={from_date}&"
            f"to={to_date}&"
            f"pageSize={page_size}"
            f"page={page}&"
            f"apiKey={api_key}"
        )
        
        print(url)

        try: 
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()

            articles = data.get("articles", [])
            if not articles:
                print("Nothing found")
                break

            all_articles.extend(articles)

        except requests.exceptions.RequestException as e:
            print(e)
            break
        except Exception as e:
            print(e)
            break

    return all_articles

def run_sentiment():
    query_terms = [
        "innovation",
        "breakthrough",
        "achievement",
        "success",
    ]
    combined_query = ' OR '.join(query_terms)
    encoded_query = urllib.parse.quote(combined_query)

    num_days = 2
    max_pages_per_day = 5

    all_articles = []

    for i in range(num_days):
        to_date = datetime.utcnow() - timedelta(days=i)
        from_date = to_date - timedelta(days=1)
        to_date_str = to_date.strftime('%Y-%m-%d')
        from_date_str = from_date.strftime('%Y-%m-%d')

        print(f"Fetching articles from {from_date_str} to {to_date_str}")

        # Fetch articles for the date range
        articles = fetch(
            query=encoded_query,
            from_date=from_date_str,
            to_date=to_date_str,
            api_key=api_key,
            page_size=100,
            max_pages=max_pages_per_day
        )

        all_articles.extend(articles)
    
    df = pd.DataFrame(all_articles)

    if 'source' in df.columns:
        df['source'] = df['source'].apply(lambda x: x.get('name') if isinstance(x, dict) else x)

    # Select desired columns
    desired_columns = ["source", "title", "description", "author", "url", "urlToImage", "publishedAt"]
    df = df[desired_columns]

    # Print the number of articles fetched
    print(f"Total articles fetched: {len(df)}")

    # Run sentiment analysis
    sentiment_results = sentiment(df)

    return sentiment_results