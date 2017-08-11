GET articles/list
=================

Returns a collection of the **n_articles** (an integer > 0) newest Articles.
They are sorted from the newest to the oldest.

Each Article will be returned in JSON with the following data: title, id, domain and a link to the ressource.

Resource URL
~~~~~~~~~~~~
**https://www.feedradar.io/api/v1/articles/list/**

.. code-block:: shell

		curl https://www.feedradar.io/api/v1/articles/list/?APIKey=00000000-0000-0000-0000-000000000000&n_articles=2

Parameters
~~~~~~~~~~

+--------------------------------------------+-------------------------------------------------------------+
|**Parameters**                              |                                             **Description** |
+============================================+=============================================================+
|APIKey                                      |                                         Your Unique API Key |
+--------------------------------------------+-------------------------------------------------------------+
|n_articles                                  |        The desired quantity of articles returned by the API |
+--------------------------------------------+-------------------------------------------------------------+


Example Result
~~~~~~~~~~~~~~

.. code-block:: json

	{
		"status": "success",
		"uri": "/api/v1/articles/list/",
		"status_code": "200",
		"output": [
			{
				"id": "WWW",
				"when":"XXXX/XX/XX XX:XX",
				"domain": "domain.tld",
				"title": "Article / Blog post title",
				"link": "https://www.feedradar.io/article.php?postID=WWW"
			},
			{
				"id": "YYY",
				"when":"XXXX/XX/XX XX:XX",
				"domain": "domain.tld",
				"title": "Article / Blog post title",
				"link": "https://www.feedradar.io/article.php?postID=YYY"
			}
		]
	}
