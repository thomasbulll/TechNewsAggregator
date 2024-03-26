from nltk.sentiment.vader import SentimentIntensityAnalyzer

def analyze_article(article):
    """
    Analyzes an article comments and classifies it on a scale of -1 to 1 based on sentiment
    (-1 being more negative, and 1 being positive).

    Args:
        article: a string containing all the text from the article

    Returns:
        A sentiment score
    """
    try:
        analyzer = SentimentIntensityAnalyzer()
        scores = analyzer.polarity_scores(article)
        return scores["compound"]
    except Exception as e:
        print("Sentiment failed at ", e)
        return 0.0

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
        
        if len(comments) > 0:
            return commentSum / len(comments)
        return 0.0
    
    except Exception as e:
        print("Sentiment failed at ", e)
        return 0.0
