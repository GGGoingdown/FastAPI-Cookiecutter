---
title: "{{ cookiecutter.project_title }} v{{ cookiecutter.project_version }}"
language_tabs:
  - python: Python
language_clients:
  - python: ""
toc_footers: []
includes: []
search: true
highlight_theme: darkula
headingLevel: 2

---

<!-- Generator: Widdershins v4.0.1 -->

<h1 id="-cookiecutter-project_title-">{{ cookiecutter.project_title }} v{{ cookiecutter.project_version }}</h1>

> Scroll down for code samples, example requests and responses. Select a language for code samples from the tabs above or the mobile navigation menu.

{{ cookiecutter.project_description }}

<h1 id="-cookiecutter-project_title--health">Health</h1>

## health_check_health_get

<a id="opIdhealth_check_health_get"></a>

> Code samples

```python
import requests
headers = {
  'Accept': 'application/json'
}

r = requests.get('/health', headers = headers)

print(r.json())

```

`GET /health`

*Health Check*

> Example responses

> 200 Response

```json
null
```

<h3 id="health_check_health_get-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|Successful Response|Inline|

<h3 id="health_check_health_get-responseschema">Response Schema</h3>

<aside class="success">
This operation does not require authentication
</aside>

<h1 id="-cookiecutter-project_title--authentication">Authentication</h1>

## create_jwt_token_auth_jwt_post

<a id="opIdcreate_jwt_token_auth_jwt_post"></a>

> Code samples

```python
import requests
headers = {
  'Content-Type': 'application/x-www-form-urlencoded',
  'Accept': 'application/json'
}

r = requests.post('/auth/jwt', headers = headers)

print(r.json())

```

`POST /auth/jwt`

*Create Jwt Token*

> Body parameter

```yaml
grant_type: string
username: string
password: string
scope: ""
client_id: string
client_secret: string

```

<h3 id="create_jwt_token_auth_jwt_post-parameters">Parameters</h3>

|Name|In|Type|Required|Description|
|---|---|---|---|---|
|body|body|[Body_create_jwt_token_auth_jwt_post](#schemabody_create_jwt_token_auth_jwt_post)|true|none|

> Example responses

> 200 Response

```json
{
  "access_token": "string",
  "token_type": "bearer"
}
```

<h3 id="create_jwt_token_auth_jwt_post-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|Successful Response|[LoginResponse](#schemaloginresponse)|
|401|[Unauthorized](https://tools.ietf.org/html/rfc7235#section-3.1)|Incorrect username or password|[DetailResponse](#schemadetailresponse)|
|422|[Unprocessable Entity](https://tools.ietf.org/html/rfc2518#section-10.3)|Validation Error|[HTTPValidationError](#schemahttpvalidationerror)|

<aside class="success">
This operation does not require authentication
</aside>

# Schemas

<h2 id="tocS_Body_create_jwt_token_auth_jwt_post">Body_create_jwt_token_auth_jwt_post</h2>
<!-- backwards compatibility -->
<a id="schemabody_create_jwt_token_auth_jwt_post"></a>
<a id="schema_Body_create_jwt_token_auth_jwt_post"></a>
<a id="tocSbody_create_jwt_token_auth_jwt_post"></a>
<a id="tocsbody_create_jwt_token_auth_jwt_post"></a>

```json
{
  "grant_type": "string",
  "username": "string",
  "password": "string",
  "scope": "",
  "client_id": "string",
  "client_secret": "string"
}

```

Body_create_jwt_token_auth_jwt_post

### Properties

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|grant_type|string|false|none|none|
|username|string|true|none|none|
|password|string|true|none|none|
|scope|string|false|none|none|
|client_id|string|false|none|none|
|client_secret|string|false|none|none|

<h2 id="tocS_DetailResponse">DetailResponse</h2>
<!-- backwards compatibility -->
<a id="schemadetailresponse"></a>
<a id="schema_DetailResponse"></a>
<a id="tocSdetailresponse"></a>
<a id="tocsdetailresponse"></a>

```json
{
  "detail": "string"
}

```

DetailResponse

### Properties

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|detail|string|true|none|none|

<h2 id="tocS_HTTPValidationError">HTTPValidationError</h2>
<!-- backwards compatibility -->
<a id="schemahttpvalidationerror"></a>
<a id="schema_HTTPValidationError"></a>
<a id="tocShttpvalidationerror"></a>
<a id="tocshttpvalidationerror"></a>

```json
{
  "detail": [
    {
      "loc": [
        "string"
      ],
      "msg": "string",
      "type": "string"
    }
  ]
}

```

HTTPValidationError

### Properties

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|detail|[[ValidationError](#schemavalidationerror)]|false|none|none|

<h2 id="tocS_LoginResponse">LoginResponse</h2>
<!-- backwards compatibility -->
<a id="schemaloginresponse"></a>
<a id="schema_LoginResponse"></a>
<a id="tocSloginresponse"></a>
<a id="tocsloginresponse"></a>

```json
{
  "access_token": "string",
  "token_type": "bearer"
}

```

LoginResponse

### Properties

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|access_token|string|true|none|none|
|token_type|string|false|none|none|

<h2 id="tocS_ValidationError">ValidationError</h2>
<!-- backwards compatibility -->
<a id="schemavalidationerror"></a>
<a id="schema_ValidationError"></a>
<a id="tocSvalidationerror"></a>
<a id="tocsvalidationerror"></a>

```json
{
  "loc": [
    "string"
  ],
  "msg": "string",
  "type": "string"
}

```

ValidationError

### Properties

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|loc|[anyOf]|true|none|none|

anyOf

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|» *anonymous*|string|false|none|none|

or

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|» *anonymous*|integer|false|none|none|

continued

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|msg|string|true|none|none|
|type|string|true|none|none|
