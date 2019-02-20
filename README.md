# File Share

* Run: docker-compose up
* Create user
* Create token for API access
* Enjoy


## Add new link / file
``/link/new/``

## Access to link / file
``/link/download/[UUID]``

# API

## Report 
``GET /api/v1/link/report``

## Add new link / file
``POST /api/v1/link/protected_resource``

``HEAD Authorization: Token xyz``

``BODY {'url': 'http://example.com'}``


## Access new link / file
``POST /api/v1/link/protected_resource/[UUID]``

``HEAD Authorization: Token xyz``

``BODY {'password': 'foo'}``


# xyz

All functionalities are done \o/

* No time for API tests
* No time for gunirorn setup 
* ...
* No time for life <sad_violin.midi>
