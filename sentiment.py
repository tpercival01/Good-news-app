from nltk.sentiment.vader import SentimentIntensityAnalyzer

def sentiment(data):
    sentiment_analyzer = SentimentIntensityAnalyzer()
    results = []

    # Define weights outside the loop
    weight_title = 0.4
    weight_description = 0.6
    print(data)

    for index, row in data.iterrows():
        # Initialize scores to default values
        score_title = 0.0
        score_desc = 0.0

        # Process title
        try:
            title_text = str(row['title']) if row['title'] is not None else ''
            score_title = sentiment_analyzer.polarity_scores(title_text)['compound']
        except Exception as e:
            title_text = ''

        # Process description
        try:
            desc_text = str(row['description']) if row['description'] is not None else ''
            score_desc = sentiment_analyzer.polarity_scores(desc_text)['compound']
        except Exception as e:
            desc_text = ''

        # Calculate overall score
        overall_score = (score_title * weight_title) + (score_desc * weight_description)

        # Determine sentiment category
        if overall_score >= 0.06:
            results.append({
                'title': title_text,
                'description': desc_text
            })

    return results