### Filtering InspectorBudget entries
#### `GET` request examples:
```angular2
http://192.168.1.111:8000/inspectorbudget/entries/?date=2019-10-31
http://127.0.0.1:8000/inspectorbudget/entries/?year=2019&month=11
```

## Authentication
Example:
```json
curl -X GET http://127.0.0.1:8000/api/example/ -H 'Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b'
```
Token must be created in django admin.
