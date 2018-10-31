# Dathena

An application to upload and label document for searching and compute the document category.

## Getting Started

You can read documentation about this application from [here](https://github.com/szetah/dathena/blob/master/README.md)

### Prerequisites

Before starting, make sure you have install [Compose](https://docs.docker.com/compose/install/#prerequisites)

## Testing

#### Automated test case for API

To run the automated test:-

`python manage.py test documents.api.tests`

* **test_upload_document** - upload a document
* **test_rud_document** - retrieve, update or delete a document
* **test_search_document** - search document with tags

#### Manual test with Postman

You are recommended to download and use [Postman](https://www.getpostman.com/apps) app for manual test

Some initial data is loaded for testing purposes and you can use it from below :-

##### confidentiality
```
topsecret, secret, confidential, private, internal, public
```

##### language
```
af, an, ar, ast, be, bg, bn, br, ca, cs, cy, da, de, el, en, es, et, eu, fa,
fi, fr, ga, gl, he, hi, hr, ht, hu, id, is, it, ja, ko, lt, lv, mk, ml, ms,
mt, ne, nl, no, oc, pl, pt, ro, ru, sk, sl, so, sq, sv, sw, th, tl, tr, uk,
ur, vi, zh-cn, zh-tw
```

##### document_type
```
email, excel, others, pdf, powerpoint, word
```

##### user
`admin`

## Endpoints

* http://127.0.0.1:8000/documents/upload/
  - PUT
    - Example 1
        ```
        {
            "confidentiality": "topsecret",
            "language": "en",
            "document_type": "pdf"
            "user": "admin",
            "tags": "tax, audit, 2018"
            "file": <attachfile>,
        }
        ```

* http://127.0.0.1:8000/documents/<id>
  - GET
  - PATCH
    - Example 1
        ```
        {
            "keywords": "2017",
            "document_type": "word"
        }
        ```
  - PUT
    - Example 1
        ```
        {
            "confidentiality": "public",
            "language": "en",
            "document_type": "others"
            "user": "admin",
            "file": <attachfile>,
        }
        ```
  - DELETE

* http://127.0.0.1:8000/documents/search/
  - POST
    - Example 1
        ```
        {
            "keywords": "2018, word",
        }
        ```

    - Example 2
        ```
        {
            "keywords": "2018",
            "document_type": "pdf"
        }
        ```

## Deployment

run `docker-compose up`

## Built With

* [Django](https://www.djangoproject.com/) - The web framework
* [Django REST Framework](https://www.django-rest-framework.org/) - The REST framework for WebAPI
* [Django Extension](https://django-extensions.readthedocs.io/en/latest/) - custom extension for Django
* [Redis](https://redis.io/) - database, cache and message broker
* [Celery](http://www.celeryproject.org/) - asynchronous job queue
* [Django Celery Beat](https://django-celery-beat.readthedocs.io/en/latest/) - periodic task scheduler
