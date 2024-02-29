from nltk.sentiment.vader import SentimentIntensityAnalyzer

def analyze_reviews(comments):
    """
    Analyzes a list of article comments and classifies on a scale of -1 to 1 them based on sentiment
    (-1 being more negative, and 1 being positive).

    Args:
        comments: A list of strings, where each string represents a comment from one article.

    Returns:
        A mean value for sentiment scores
    """
    # Uncomment the line below if VADER lexicon is out of date / unable to load the VADER lexicon
    # nltk.download('vader_lexicon')

    try:
        analyzer = SentimentIntensityAnalyzer()
        commentSum = 0

        for comment in comments:
            scores = analyzer.polarity_scores(comment)
            compound_score = scores["compound"]
            commentSum += compound_score
        
        return commentSum / len(comments)
    except Exception as e:
        print("Sentiment failed at ", e)
        return 0.0
