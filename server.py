from app import app
from app.models import connect_to_db, db, User
from flask_debugtoolbar import DebugToolbarExtension

connect_to_db(app)
# Use the DebugToolbar
DebugToolbarExtension(app)
app.run(debug=True)
