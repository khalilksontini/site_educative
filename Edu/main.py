from fastapi import FastAPI
import pymysql
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000","http://localhost:4200"],
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"], 
)


def get_connection():
    return pymysql.connect(
        host="localhost",
        user="root",
        password="",
        database="edudb123",
        port=3306,
        cursorclass=pymysql.cursors.DictCursor
    )


@app.get("/users")
async def fetch_all():
    try:
        connection = get_connection()
        with connection:
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM users")
                users = cursor.fetchall()
        return {"users": users}
    except Exception as e:
        return {"error": str(e)}


@app.post("/users")
async def create_user(formData: dict):
    name = formData["name"]
    email = formData["email"]
    password = formData["password"]
    departement = formData["departement"] 
    if not name or not email or not password:
        return {"error": "Name, email, and password are required"}
    try:
        connection = get_connection()
        with connection:
            with connection.cursor() as cursor:
                cursor.execute("INSERT INTO users (name, email, password, departement) VALUES (%s, %s, %s, %s)", (name, email, password, departement))
            connection.commit()
        return {"message": "User created successfully"}
    except Exception as e:
        return {"error": str(e)}





@app.post("/login")
async def login_user(formData: dict):
    email = formData.get("email", "").strip()
    password = formData.get("password", "").strip()

    if not email or not password:
        return {"error": "L'email et le mot de passe sont obligatoires"}

    try:
        connection = get_connection()
        with connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT * FROM users WHERE email = %s AND password = %s",
                    (email, password)
                )
                user = cursor.fetchone()

        if user:
            return {"message": "Connexion réussie", "user": user}
        else:
            return {"error": "Email ou mot de passe incorrect"}
    except Exception as e:
        return {"error": str(e)}
