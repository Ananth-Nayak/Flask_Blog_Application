from flask import Flask, render_template, request, redirect, url_for
from config import Config
import uuid

app = Flask(__name__)

app.config.from_object(Config)

posts = [
    {'id': 1, 'title':'First Post', 'content':'This is the first post.'},
    {'id':2, 'title':'Second Post', 'content': 'This is the second post.'}
]

@app.route("/")
def index():
    return render_template('index.html',posts = posts)

@app.route("/create", methods = ['GET', 'POST'])
def create_post():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        post_id = str(uuid.uuid4())
        new_post = {'id':post_id, 'title':title, 'content':content}
        posts.append(new_post)
        return redirect('/')
    return render_template('create_post.html')

@app.route('/edit/<string:post_id>', methods = ['GET','POST'])
def edit_post(post_id):
    post = next((p for p in posts if p['id'] == post_id), None)
    if post is None:
        return 'Post not found', 404
    if request.method =='POST':
        post['title'] = request.form['title']
        post['content'] = request.form['content']
        return redirect('/')
    return render_template('edit_post.html', post = post)

@app.route('/delete/<string:post_id>')
def delete_post(post_id):
    post = next((p for p in posts if p['id'] == post_id), None)
    if post is None:
        return 'Post not found', 404
    posts.remove(post)
    return redirect('/')



if __name__ == '__main__':
    app.run()