from flask import Flask,render_template,request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, date

app=Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///customer_details.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db=SQLAlchemy(app)

class CustomerDetails(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    customer_name=db.Column(db.String(255),nullable=False)
    contact_number=db.Column(db.String(15),nullable=False)
    number_of_items=db.Column(db.Integer,nullable=False)
    amount=db.Column(db.Integer,nullable=False)
    date_of_purchase=db.Column(db.Date,nullable=False)

@app.route('/details',methods=['GET','POST'])
def details():
    if request.method=='POST':
        try:
            username=request.form.get('username','Unknown')
            contact_number=request.form.get('contact_number','0000000000')
            number_of_items=int(request.form.get('number_of_items',0))
            amount=int(request.form.get('amount',0))
            current_date=request.form.get('current_date',str(date.today()))

            current_date=datetime.strptime(current_date,'%Y-%m-%d').date()

            customer=CustomerDetails(
                customer_name=username,
                contact_number=contact_number,
                number_of_items=number_of_items,
                amount=amount,
                date_of_purchase=current_date
            )
            db.session.add(customer)
            db.session.commit()
            return render_template('index.html',message="Customer Details Successfully Added")
        except Exception as e:
            return render_template('winner.html',username=None,contact_number=None)

@app.route('/winner',methods=['GET','POST'])
def winner():
    today=date.today()
    winner=CustomerDetails.query.filter_by(date_of_purchase=today).order_by(
        CustomerDetails.total_amount.desc()
    ).first()
    if winner:
        return render_template('winner.html', username=winner.customer_name,contact_number=winner.contact_number)
    else:
        return render_template('winner.html',username=None,contact_number=None)

@app.route('/')
def index():
    return render_template('index.html')

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080,debug=True)
            