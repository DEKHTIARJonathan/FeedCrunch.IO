'''
Follow these steps to configure the webhook in Slack:

  1. Navigate to https://<your-team-domain>.slack.com/services/new

  2. Search for and select "Incoming WebHooks".

  3. Choose the default channel where messages will be sent and click "Add Incoming WebHooks Integration".

  4. Copy the webhook URL from the setup instructions and use it in the next section.


Follow these steps to encrypt your Slack hook URL for use in this function:

  1. Create a KMS key - http://docs.aws.amazon.com/kms/latest/developerguide/create-keys.html.

  2. Encrypt the event collector token using the AWS CLI.
	 $ aws kms encrypt --key-id alias/<KMS key name> --plaintext "<SLACK_HOOK_URL>"

	 Note: You must exclude the protocol from the URL (e.g. "hooks.slack.com/services/abc123").

  3. Copy the base-64 encoded, encrypted key (CiphertextBlob) to the ENCRYPTED_HOOK_URL variable.

  4. Give your function's role permission for the kms:Decrypt action.
	 Example:

{
	"Version": "2012-10-17",
	"Statement": [
		{
			"Sid": "Stmt1443036478000",
			"Effect": "Allow",
			"Action": [
				"kms:Decrypt"
			],
			"Resource": [
				"<your KMS key ARN>"
			]
		}
	]
}
'''
from __future__ import print_function

import boto3
import json
import logging

from base64 import b64decode
from urllib2 import Request, urlopen, URLError, HTTPError


ENCRYPTED_HOOK_URL = 'CiDzDqG+/DQa98VgADa9xubV2PosZRGpUwf1RFMy24amZRLQAQEBAgB48w6hvvw0GvfFYAA2vcbm1dj6LGURqVMH9URTMtuGpmUAAACnMIGkBgkqhkiG9w0BBwaggZYwgZMCAQAwgY0GCSqGSIb3DQEHATAeBglghkgBZQMEAS4wEQQMThIw6fscqfJ+nFjJAgEQgGBij5fPmCcWdaG+KF03KGmoz6uWONAOsf2jqEhGTAicHsIxwdaQTkfuYbmA0cT5Q5JOW7ti3FpQEOM0Ta9bzPNBpxDxmhBEkimWBB6dlVX17fXUG8oxrvq7o+Zs+NT3B5g='  # Enter the base-64 encoded, encrypted key (CiphertextBlob)
SLACK_CHANNEL = '#build_infos'  # Enter the Slack channel to send a message to

HOOK_URL = "https://" + boto3.client('kms').decrypt(CiphertextBlob=b64decode(ENCRYPTED_HOOK_URL))['Plaintext']

def pretty(d, indent=0):
	data = ""
	for key, value in d.iteritems():
		data += '\t' * indent + str(key) + " "
		if isinstance(value, dict):
			data += pretty(value, indent+1)
		else:
			data += '\t' * (indent+1) + str(value) + " "
			
	return data

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(event, context):
	logger.info(pretty(event))
	
	data = event['Records'][0]['Sns']
	message = json.loads(data['Message'])
	
	logger.info(pretty(data))

	timestamp = message['createTime']
	application = message['applicationName']
	status = message['status']

	slack_message = {
		'channel': SLACK_CHANNEL,
		'text': "@ %s : Deploy of  %s with status %s" % (timestamp, application, status)
	}

	req = Request(HOOK_URL, json.dumps(slack_message))
	try:
		response = urlopen(req)
		response.read()
		logger.info("Message posted to %s", slack_message['channel'])
	except HTTPError as e:
		logger.error("Request failed: %d %s", e.code, e.reason)
	except URLError as e:
		logger.error("Server connection failed: %s", e.reason)