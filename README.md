
This is a dummy social networking API (RESTful Web Service). It provides several functionalities - 
1. Creating a user
2. Getting a user by id
3. Login user
4. Creating a post 
5. Getting all posts
6. Getting post by id
7. Updating post - allowed only for the owner/creator of the posts
8. Deleting post - allowed only for the owner/creator of the posts

For point 4 to 8 - authorization granted only after successful login. Authentication done using JWT token.

Framework - FastAPI
Database - PostgreSQL
Database Migration tool - Alembic

Staring command:  uvicorn app.main:app --host 0.0.0.0 --port 10000

Hosted on render. Find the documentation at - https://social-nw-fastapi-js.onrender.com/docs
