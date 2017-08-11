GET articles/all
================

Returns a collection of every Articles ever posted on the platform.
They are sorted from the newest to the oldest.

Each Article will be returned in JSON with the following data: title, id, domain and a link to the ressource.

Resource URL
~~~~~~~~~~~~
**https://www.feedradar.io/api/v1/articles/all/**

.. code-block:: shell

		curl https://www.feedradar.io/api/v1/articles/all/?APIKey=00000000-0000-0000-0000-000000000000

Parameters
~~~~~~~~~~

+--------------------------------------------+-------------------------------------------------------------+
|**Parameters**                              |                                             **Description** |
+============================================+=============================================================+
|APIKey                                      |                                         Your Unique API Key |
+--------------------------------------------+-------------------------------------------------------------+


Example Result
~~~~~~~~~~~~~~

.. code-block:: json

	{
		"status": "success",
		"uri": "/api/v1/articles/all/",
		"status_code": "200",
		"output": [
			{
				"id": "1",
				"when":"XXXX/XX/XX XX:XX",
				"domain": "domain.tld",
				"title": "Article / Blog post title",
				"link": "https://www.feedradar.io/article.php?postID=1"
			},
			{
			"id": "2",
			"when":"XXXX/XX/XX XX:XX",
			"domain": "domain.tld",
			"title": "Article / Blog post title",
			"link": "https://www.feedradar.io/article.php?postID=2"
			},
			{
				"id": "718",
				"when":"XXXX/XX/XX XX:XX",
				"domain": "domain.tld",
				"title": "Article / Blog post title",
				"link": "https://www.feedradar.io/article.php?postID=718"
			}
		]
	}
