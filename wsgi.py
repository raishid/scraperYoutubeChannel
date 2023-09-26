from app.main import app as application

if __name__ == "__main__":
    application.run(async_mode='gevent_uwsgi')
    # application.run(debug=True, port=5000)
