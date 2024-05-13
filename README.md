# Todos_FastAPI
This is a fully functional backend API for Todolist, which includes all the CRUD operations and involves role based managing with authentication and authorization of users.

To run and use this code, first clone this repository into your local device.
## Requirements
-> Download all the requirements, run this command in terminal: `pip install -r requirements.txt`

## Procedure
-> First, create a seperate folder called `routers` and add the files `auth, users, admin, todos` to it. These our are main routers and core of our project.
NOTE: Considering you have created a virtual enviroment already. If not, please create one and do all the operations in it.

## To Run
-> There are two options:
            1) Run in terminal - `uvicorn main:app --reload` . Finds host and port, fixes automatically.
            2) Run in terminal - `uvicorn main:app --host x.x.x.x --port yyyy --reload . You can choose the host and port ids.

## Output
-> Instead of going to the localhost link. go to localhost/docs to get the Swagger UI page.
eg: if your server is hosted on `127.0.0.1/5000` => to view swagger ui page: `127.0.0.1/5000/docs`
