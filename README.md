# Samba
<img src="static/images/simba.png" width="250">

### Filtering InspectorBudget entries
#### `GET` request examples:
```angular2
http://192.168.1.111:8000/inspectorbudget/entries/?date=2019-10-31
http://127.0.0.1:8000/inspectorbudget/entries/?year=2019&month=11
```

### Pagination
Example request:
```json
curl -X GET http://127.0.0.1:8000/api/example/?page=2
```

### Authentication
#### Retrieve token:
```json
curl -X POST --data "username=user&password=secret" http://localhost:8000/api-token-auth/
```
response:
```json
{
  "token": "9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b"
}
```
Token can be also created in django admin.

#### Use token
Example:
```json
curl -X GET http://127.0.0.1:8000/api/example/ -H 'Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b'
```

