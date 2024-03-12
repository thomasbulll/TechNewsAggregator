from email_notifications import find_correct_recipients
import pytest

def test_correct_filters_applied():
  articles = [
    {'title': 'no key matches here', 'url': 'test1.com'},
    {'title': 'essential matches here', 'url': 'test2.com'},
    {'title': 'required matches here', 'url': 'test3.com'}
  ]

  filters = {
    'essential': ['testUser1@test.com', 'testUser2@test.com'],
    'necessary': ['testUser2@test.com'],
    'required': ['testUser1@test.com']
  }

  found_matches = find_correct_recipients(articles, filters)

  expected_matches = [
    {'title': 'essential matches here', 'url': 'test2.com', 'email': 'testUser1@test.com'},
    {'title': 'essential matches here', 'url': 'test2.com', 'email': 'testUser2@test.com'},
    {'title': 'required matches here', 'url': 'test3.com', 'email': 'testUser1@test.com'}
  ]

  assert found_matches == expected_matches

