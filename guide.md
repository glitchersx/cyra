<<<<<<< HEAD
API REFERENCE
Knowledge Base
Create knowledge base document from text

POST

https://api.elevenlabs.io
/v1/convai/knowledge-base/text
POST
/v1/convai/knowledge-base/text

cURL

curl -X POST https://api.elevenlabs.io/v1/convai/knowledge-base/text \
     -H "xi-api-key: <apiKey>" \
     -H "Content-Type: application/json" \
     -d '{
  "text": "text"
}'
Try it
200
Successful

{
  "id": "id",
  "name": "name",
  "prompt_injectable": true
}
Create a knowledge base document containing the provided text.

Headers
xi-api-key
string
Required
Request
This endpoint expects an object.
text
string
Required
Text content to be added to the knowledge base.

name
string
Optional
A custom, human-readable name for the document.

Response
Successful Response

id
string
name
string
prompt_injectable
boolean

PI REFERENCE
Knowledge Base
Create knowledge base document from file

POST

https://api.elevenlabs.io
/v1/convai/knowledge-base/file
POST
/v1/convai/knowledge-base/file

cURL

curl -X POST https://api.elevenlabs.io/v1/convai/knowledge-base/file \
     -H "xi-api-key: <apiKey>" \
     -H "Content-Type: multipart/form-data" \
     -F file=@<file1>
Try it
200
Successful

{
  "id": "id",
  "name": "name",
  "prompt_injectable": true
}
Create a knowledge base document generated form the uploaded file.

Headers
xi-api-key
string
Required
Request
This endpoint expects a multipart form containing a file.
file
file
Required
Documentation that the agent will have access to in order to interact with users.

name
string
Optional
A custom, human-readable name for the document.

Response
Successful Response

id
string
name
string
prompt_injectable
=======
API REFERENCE
Knowledge Base
Create knowledge base document from text

POST

https://api.elevenlabs.io
/v1/convai/knowledge-base/text
POST
/v1/convai/knowledge-base/text

cURL

curl -X POST https://api.elevenlabs.io/v1/convai/knowledge-base/text \
     -H "xi-api-key: <apiKey>" \
     -H "Content-Type: application/json" \
     -d '{
  "text": "text"
}'
Try it
200
Successful

{
  "id": "id",
  "name": "name",
  "prompt_injectable": true
}
Create a knowledge base document containing the provided text.

Headers
xi-api-key
string
Required
Request
This endpoint expects an object.
text
string
Required
Text content to be added to the knowledge base.

name
string
Optional
A custom, human-readable name for the document.

Response
Successful Response

id
string
name
string
prompt_injectable
boolean

PI REFERENCE
Knowledge Base
Create knowledge base document from file

POST

https://api.elevenlabs.io
/v1/convai/knowledge-base/file
POST
/v1/convai/knowledge-base/file

cURL

curl -X POST https://api.elevenlabs.io/v1/convai/knowledge-base/file \
     -H "xi-api-key: <apiKey>" \
     -H "Content-Type: multipart/form-data" \
     -F file=@<file1>
Try it
200
Successful

{
  "id": "id",
  "name": "name",
  "prompt_injectable": true
}
Create a knowledge base document generated form the uploaded file.

Headers
xi-api-key
string
Required
Request
This endpoint expects a multipart form containing a file.
file
file
Required
Documentation that the agent will have access to in order to interact with users.

name
string
Optional
A custom, human-readable name for the document.

Response
Successful Response

id
string
name
string
prompt_injectable
>>>>>>> 787b239a67e4f1f5d204f8fe6b5b6edcc491c2f4
boolean