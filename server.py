from app import app
from app.models import connect_to_db, db, User

connect_to_db(app)
app.run(debug=True)
