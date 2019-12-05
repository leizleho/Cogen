from app import app
from app.db import db, connect_to_db
from app.ma import ma

connect_to_db(app)
ma.init_app(app)
app.debug = True
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5555)
