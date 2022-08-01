---
title: FastAPI Application v0.0.1
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

<h1 id="fastapi-application">FastAPI Application v0.0.1</h1>

> Scroll down for code samples, example requests and responses. Select a language for code samples from the tabs above or the mobile navigation menu.

FastAPI Base Application

<h1 id="fastapi-application-health">Health</h1>

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
