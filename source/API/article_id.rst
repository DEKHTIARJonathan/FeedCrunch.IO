GET article/id
==============

Returns a single Article, specified by the id parameter.

The Article will be returned in JSON with the following data: title, id, domain and a link to the ressource.

Resource URL
~~~~~~~~~~~~
**https://www.feedradar.io/api/v1/article/id/**

.. code-block:: shell

		curl https://www.feedradar.io/api/v1/article/id/?APIKey=00000000-0000-0000-0000-000000000000&id=XXXXX

Parameters
~~~~~~~~~~

+--------------------------------------------+-------------------------------------------------------------+
|**Parameters**                              |                                             **Description** |
+============================================+=============================================================+
|APIKey                                      |                                         Your Unique API Key |
+--------------------------------------------+-------------------------------------------------------------+
|id                                          |     The ID of the Ressource for which to return results for |
+--------------------------------------------+-------------------------------------------------------------+


Example Result
~~~~~~~~~~~~~~

.. code-block:: json

	{
		"status":"success",
		"uri":"/api/v1/article/id/",
		"status_code":"200",
		"output":{
			"id": "24",
			"when":"XXXX/XX/XX XX:XX",
			"domain": "domain.tld",
			"title": "Article / Blog post title",
			"link": "https://www.feedradar.io/article.php?postID=24"
		}
	}
