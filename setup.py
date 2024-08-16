from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///project.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(1000), nullable=False)

    def __repr__(self) -> str:
        return f"Product {self.name} - {self.id}"

@app.route("/")
def hello_world():
    todo = Product(name="Todo", price=10.99, description="A description of the todo product")
    db.session.add(todo)
    db.session.commit()
    return render_template("index.html")

@app.route("/products")
def products():
    return "<p>Hello</p>"

if __name__ == "__main__":
    # Create the database and tables if they don't exist
    with app.app_context():
        db.create_all()  # Creates the SQLite database and Product table

    # Run the Flask app
    app.run(debug=True, port=8000)
