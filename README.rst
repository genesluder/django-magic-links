=============================
django-magic-links
=============================


Example Usage:
==============

```bash
curl -X POST -d “email=drwho@tardis.com&source=ios” localhost:8000/api/auth/email/
```

The user drwho@tardis.com receives an email

```
    Follow this link to sign in: myapp://login/?token=$2b$12$Pc9ugN5DwsC3jNYwpfG.XOxUuwybmJu1HTvfpPCyGk/I3BkFLZDsq&email=drwho@tardis.com
```

At this point, the client can use the supplied token to request a DRF auth token

```bash
curl -X POST -d “email=drwho@tardis.com&token=$2b$12$Pc9ugN5DwsC3jNYwpfG.XOxUuwybmJu1HTvfpPCyGk/I3BkFLZDsq” localhost:8000/api/auth/token/

{
    "token": "3d247ac9a67630932bb6b5e08cb24c0c7760f37a"
}
```



WORK IN PROGRESS
================
Current
----
* DRF token auth
  * Request magic link
  * Get auth token from link token
  * Happy path verified 


To Do
----

* DRF token auth: Non-happy path testing and error handling
* Django view auth
* Tests

