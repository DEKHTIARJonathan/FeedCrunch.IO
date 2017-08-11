POST article/add
================

Post a ressource to the platform. Title and Link are taken as input.

The API will return the id assigned to the ressource.

Important information
~~~~~~~~~~~~~~~~~~~~~

Every addition to the platform is manually checked and approved before being publicly visible on the platform.
This action is normally done under 24hours.

This review process has been set up in order to keep the high quality of the contents published.
We think that fewer publication with a high added-value is more interesting than the opposite situation.

Resource URL
~~~~~~~~~~~~
**https://www.feedradar.io/api/v1/article/add/**

.. code-block:: shell

		curl -H "Content-Type: application/json" -X POST -d '{"APIKey":"00000000-0000-0000-0000-000000000000","link":"http://example.com", "title":"My Super Article"}' https://www.feedradar.io/api/v1/article/add/

Here is the JSON given as input in a more readable manner:
		
.. code-block:: json
		
	{
	  "APIKey":"00000000-0000-0000-0000-000000000000",
	  "link":"http://www.example.com", 
	  "title":"My Super Article"
	}		
		
Parameters
~~~~~~~~~~

+--------------------------------------------+----------------------------------------------------------------+
|**Parameters**                              |                                                **Description** |
+============================================+================================================================+
|APIKey                                      |                                            Your Unique API Key |
+--------------------------------------------+----------------------------------------------------------------+
|link                                        |  The ressource's full URL that you are posting to the platform |
+--------------------------------------------+----------------------------------------------------------------+
|title                                       |                   The ressource's title that will be displayed |
+--------------------------------------------+----------------------------------------------------------------+

Example Result
~~~~~~~~~~~~~~

.. code-block:: json

	{
		"status":"success",
		"uri":"/api/v1/article/add/",
		"status_code":"200",
		"link":"http://example.com", 
		"title":"My Super Article",
		"id":"XXX"
	}
