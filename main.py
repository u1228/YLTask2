from flask import Flask, render_template
from data import db_session, jobs, users
from datetime import datetime

app = Flask(__name__, template_folder="template/")
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


@app.route("/")
def index():
    global actions
    return render_template("works.html", actions=actions, enumerate=enumerate)


def main():
    global actions
    try:
        db_session.global_init("db/blogs.sqlite")
    
        session = db_session.create_session()

        Jobs = jobs.Jobs
        User = users.User
        
        actions = []
        
        for job in session.query(Jobs).all():
            user = session.query(User).filter(User.id == job.team_leader).first()
            actions.append((job.job, ' '.join([user.name, user.surname]), job.work_size, job.collaborators, job.is_finished))
    
        app.run(debug=False)
    except Exception as s:
        input(s)


actions = None

if __name__ == '__main__':
    main()