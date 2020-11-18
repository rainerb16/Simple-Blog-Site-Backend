import mariadb
from flask import Flask, request, Response
import json
import dbcreds
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


@app.route('/blogs', methods=['GET', 'POST', 'PATCH', 'DELETE'])
def blogPost():
    if request.method == 'GET':
        conn = None
        cursor = None
        blog_posts = None
        try:
            conn = mariadb.connect(host = dbcreds.host, password = dbcreds.password, user = dbcreds.user, port = dbcreds.port, database = dbcreds.database)
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM posts")
            blog_posts = cursor.fetchall()
        except Exception as error:
            print("Something went wrong (not good practice): ")
            print(error)
        finally:
            if(cursor != None):
                cursor.close()
            if(conn != None):
                conn.rollback()
                conn.close()
            if(blog_posts != None):
                return Response(json.dumps(blog_posts, default = str), mimetype = "application/json", status = 200)
            else:
                return Response("Something went wrong...please try again", mimetype = "text/html", status = 500)
    elif request.method == 'POST':
        conn = None
        cursor = None
        blog_content = request.json.get("content")
        blog_created_at = request.json.get("created_at")
        blog_title = request.json.get("blog_title")
        rows = None
        try:
            conn = mariadb.connect(host = dbcreds.host, password = dbcreds.password, user = dbcreds.user, port = dbcreds.port, database = dbcreds.database)
            cursor = conn.cursor()
            cursor.execute("INSERT INTO posts(content, created_at, blog_title) VALUES(?, ?, ?)", [blog_content, blog_created_at, blog_title,])
            conn.commit()
            rows = cursor.rowcount
        except Exception as error:
            print("Something went wrong (not good practice): ")
            print(error)
        finally:
            if(cursor != None):
                cursor.close()
            if(conn != None):
                conn.rollback()
                conn.close()
            if(rows == 1):
                return Response("Blog post success!", mimetype = "text/html", status = 201)
            else:
                return Response("Something went wrong... please try again", mimetype = "text/html", status = 500)
    elif request.method == 'PATCH':
        conn = None
        cursor = None
        rows = None
        blog_content = request.json.get("content")
        blog_title = request.json.get("blog_title")
        post_id = request.json.get("id")
        try:
            conn = mariadb.connect(host = dbcreds.host, password = dbcreds.password, user = dbcreds.user, port = dbcreds.port, database = dbcreds.database)
            cursor = conn.cursor()
            if(blog_content != "" and blog_content != None):
                cursor.execute("UPDATE posts SET content = ? WHERE id = ?", [blog_content, post_id,])
            if(blog_title != "" and blog_title != None):
                cursor.execute("UPDATE posts SET blog_title = ? WHERE id = ?", [blog_title, post_id,])
            conn.commit()
            rows = cursor.rowcount
        except Exception as error:
            print("Something went wrong (not good practice): ")
            print(error)
        finally:
            if(cursor != None):
                cursor.close()
            if(conn != None):
                conn.rollback()
                conn.close()
            if(rows == 1):
                return Response("Blog post has been updated!", mimetype = "text/html", status = 204)
            else:
                return Response("Something went wrong... please try again", mimetype = "text/html", status = 500)
    elif request.method == 'DELETE':
        conn = None
        cursor = None
        rows = None
        post_id = request.json.get("id")
        try:
            conn = mariadb.connect(host = dbcreds.host, password = dbcreds.password, user = dbcreds.user, port = dbcreds.port, database = dbcreds.database)
            cursor = conn.cursor()
            cursor.execute("DELETE FROM posts WHERE id = ?", [post_id,])
            conn.commit()
            rows = cursor.rowcount
        except Exception as error:
            print("Something went wrong (not good practice): ")
            print(error)
        finally:
            if(cursor != None):
                cursor.close()
            if(conn != None):
                conn.rollback()
                conn.close()
            if(rows == 1):
                return Response("Blog post has been deleted!", mimetype = "text/html", status = 200)
            else:
                return Response("Something went wrong... please try again", mimetype = "text/html", status = 500)