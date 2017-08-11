GET article/search
==================

Returns a collection of relevant Articles matching a specified query.
They are sorted from the newest to the oldest.

Each Article will be returned in JSON with the following data: title, id, domain and a link to the ressource.

Resource URL
~~~~~~~~~~~~
**https://www.feedradar.io/api/v1/articles/search/**

.. code-block:: shell

		curl https://www.feedradar.io/api/v1/articles/search/?APIKey=00000000-0000-0000-0000-000000000000&query=Data%20Science

The string given in argument with query="xxxxxxxx" **must be** `URL ENCODED <http://www.w3schools.com/tags/ref_urlencode.asp>`_.

Parameters
~~~~~~~~~~

+--------------------------------------------+-------------------------------------------------------------+
|**Parameters**                              |                                             **Description** |
+============================================+=============================================================+
|APIKey                                      |                                         Your Unique API Key |
+--------------------------------------------+-------------------------------------------------------------+
|query                                       |         The desired search query to perform on the database |
+--------------------------------------------+-------------------------------------------------------------+


Example Result
~~~~~~~~~~~~~~

.. code-block:: json

	{
		"status": "success",
		"uri": "/api/v1/articles/search/",
		"status_code": "200",
		"query" : "Searched Query",
		"output": [
			{
				"id": "YYY",
				"when":"XXXX/XX/XX XX:XX",
				"domain": "domain.tld",
				"title": "Article / Blog post title - Searched Query Related",
				"link": "https://www.feedradar.io/article.php?postID=YYY"
			},
			{
				"id": "WWW",
				"when":"XXXX/XX/XX XX:XX",
				"domain": "domain.tld",
				"title": "Article / Blog post title - Searched Query Related",
				"link": "https://www.feedradar.io/article.php?postID=WWW"
			}
		]
	}
