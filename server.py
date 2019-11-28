from app import app
from app.db import db, connect_to_db
from app.ma import ma
from flask_debugtoolbar import DebugToolbarExtension

connect_to_db(app)
ma.init_app(app)
app.debug = True
# DebugToolbarExtension(app)
app.run()
