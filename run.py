from app import create_app
# from app.utils.bg_jobs import 
# import atexit


app = create_app()
# atexit.register(lambda: scheduler.shutdown(wait=False))

if __name__ == '__main__':
    app.run(debug=True, threaded=True)