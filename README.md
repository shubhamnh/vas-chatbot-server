# Virtual Assistant for Students (Chatbot) - Backend

A chatbot for students to get info related to exam results, time table, etc.

This is the server application.

The client app can be found [here](https://github.com/shubhamnh/vas-chatbot-client/)

**Contents**

* [Environment Variables](#environment-variables)
* [API Reference](#api-reference)
* [TODO](#todo)

## Environment Variables

To run this project, you will need to add the following environment variables to your `.env` file. Sample present in `.env_sample`.

* `SECRET_KEY`
Generate the secret key by running the following from the command line:

`python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
`

* `DATABASE_URL`

* `WP_PRIVATE_KEY`

* `WP_CLAIMS_EMAIL`

  
## API Reference

**Student** 

* [Obtain Auth Tokens (Login)](#obtain-auth-tokens-login) : `POST /api-token-auth/`
* [Verify Auth Tokens](#verify-auth-tokens) : `POST /api-token-auth/`
* [User Information](#user-information) : `GET /login/info/[rollno]/`
* [Querying](#querying) : `POST /login/query/`
* [Get Group Notifications](#get-group-notifications) : `GET /login/notif/`
* [Get Personal Notifications](#get-personal-notifications) : `GET /login/personal/`
* [Support / Feedback](#support--feedback) : `POST /login/support/`

**Admin / Professor**

* Post Group Notifications : `POST /login/notif/`
* Post Personal Notifications : `POST /login/personal/`

### Obtain Auth Tokens (Login)

**URL** : `/api/token-auth/`

**Method** : `POST`

**Auth required** : NO

**Request body**

```json
{
    "username": "[valid username/rollnumber]",
    "password": "[password in plain text]"
}
```

#### Success Response

**Code** : `200 OK`

**Response body**

```json
{
  "refresh": "[refresh_token]",
  "access": "[access_token]"
}
```

### Verify Auth Tokens

**URL** : `/api/token-verify/`

**Method** : `POST`

**Auth required** : NO

**Request body**

```json
{
    "token": "[access token]",
}
```

#### Success Response

**Code** : `200 OK`

**Response body**

```json
{}
```


### User Information

**URL** : `/api/profile/`

**Methods** : `GET`

**Auth required** : YES

#### Success Response

**Code** : `200 OK`

**Response body**

```json
{
  "rno": "[username/roll number]",
  "name": "[Name]",
  "batch": 3
}
```

### Querying

**URL** : `/api/query/`

**Method** : `POST`

**Auth required** : YES

**Request body**

```json
{
    "query": "[query in plain text]"
}
```

#### Success Response

**Code** : `200 OK`

**Response body**

```json
{
  "response": "[
      {
          text: "Hey! How you doin?"
      },
      ...
  ]"
}
```

### Get Group Notifications

**URL** : `/api/groupnotif/`

**Methods** : `GET`

**Auth required** : YES

#### Success Response

**Code** : `200 OK`

**Response body**

```json
[
    {
        "teacher":"Prof. Sagan",
        "subject":"Voyager 1",
        "notice":"Pale Blue Dot",
        "interest":"Astrophysics",
        "creation_date":"2021-01-19"
    }
]

```

### Get Personal Notifications

**URL** : `/api/individualnotif/`

**Methods** : `GET`

**Auth required** : YES

#### Success Response

**Code** : `200 OK`

**Response body**

```json
[
    {
        "teacher":"Prof. Feynman",
        "subject":"Fun to Imagine",
        "notice":"The Oxygen atoms snap in to the Carbon atoms to create a Catastrophe! 🔥",
        "creation_date":"2021-01-19"
    }
]
```

### Support / Feedback

**URL** : `/api/feedback/`

**Method** : `POST`

**Auth required** : YES

**Request body**

```json
{
  "subject": "[Subject]",
  "details": "[Feedback]"
}
```

#### Success Response

**Code** : `201 OK`

**Response body**

```json
{
  "subject": "[Subject]",
  "details": "[Feedback]",
}
```

## TODO

- API reference for Push Notifications and Admin side endpoints (POST Notifitions)

- Installation, Features and screenshots
  