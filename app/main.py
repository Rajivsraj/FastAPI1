from fastapi import FastAPI, status
import psycopg
from pydantic import BaseModel


app = FastAPI()

while True:
    try:
        conn = psycopg.connect("dbname='fastapi1' user='postgres' host='localhost' password='Admin@123'")
        cur = conn.cursor()
        # print("Connected to PostgreSQL")
        break
    except Exception as err:
        print("Unable to connect to PostgreSQL")
        print("Error ", err)


class Post(BaseModel):
    title: str
    content: str
    published: bool = True


@app.get("/")
async def read_root():
    return {"Hello": "World"}


# get all posts
@app.get("/posts")
def read_posts():
    cur.execute("""SELECT * FROM posts""")
    posts = cur.fetchall()
    print(posts)
    return {"data": posts}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    cur.execute("""insert into posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """, (post.title, post.content, post.published))
    new_post = cur.fetchall()
    conn.commit()
    return {"data": new_post}


@app.get("/posts/{id}")
def read_post(id: int):
    print("Hello")
    cur.execute("""select * from posts where id = %s""", (str(id),))
    test_post = cur.fetchall()
    print(test_post)
    return {"data": test_post}