import pytest

@pytest.fixture
def fetch_test_expected_top_articles():
    expected = [{"title": "Test Article 1", "url": "https://test_site_1"}, 
                {"title": "Test Article 2", "url": "https://test_site_2"}, 
                {"title": "Test Article 3", "url": "https://test_site_3"},
                {"title": "Test Article 4", "url": "https://test_site_4"},
                {"title": "Test Article 5", "url": "https://test_site_5"}]
    return expected

@pytest.fixture
def fetch_test_bbc_expected_top_articles():
    expected = [{"title": "Test Article 1", "url": "https://www.bbc.co.uk/news/technology-111"}, 
                {"title": "Test Article 2", "url": "https://www.bbc.co.uk/news/technology-222"}, 
                {"title": "Test Article 3", "url": "https://www.bbc.co.uk/news/technology-333"},
                {"title": "Test Article 4", "url": "https://www.bbc.co.uk/news/technology-444"},
                {"title": "Test Article 5", "url": "https://www.bbc.co.uk/news/technology-555"}]
    return expected