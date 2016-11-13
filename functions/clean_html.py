import re, HTMLParser

def clean_html(raw_html):
	# Removing all HTML Tags
	cleanr = re.compile('<.*?>')
	cleantext = re.sub(cleanr, '', raw_html)

	# Remove all HTML Codes and convert them to string
	cleantext = HTMLParser.HTMLParser().unescape(cleantext)

	return cleantext
