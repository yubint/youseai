
# YouseAI Project

A project made for YouseAI internship


## API Reference

#### Register the user

```http
  POST /register/
```

| Parameter | Type     | 
| :-------- | :------- | 
| `username` | `string` | 
| `email` | `string` | 
| `password` | `string` | 

Password Requirement: Minimum of 8 characters with one of lowercase, uppercase, number and special character each
#### Login the User

```http
  POST /login/
```

| Parameter | Type     | 
| :-------- | :------- | 
| `username` | `string` | 
| `password` | `string` | 

### Requires Authentication
Authenticated through knox Authtoken in Headers. Token is provided in Login

```
{
    'Authorization':'Token {key}'
}
```
#### View the User

```http
  GET /profile/
```

#### Update the user

```http
  PUT /profile/
```
| Parameter | Type     | 
| :-------- | :------- | 
| `username` | `string` | 
| `email` | `string` | 
| `password` | `string` |

#### Logout
```http
  POST /logout/
```


## Run Locally

To run this project locally

```bash
  git clone https://github.com/yubint/youseai
```
```bash
  cd youseai
```

```bash
  pip install -r requirements.txt
```
```bash
  python manage.py runserver
```



