from flask import Flask, request, render_template, jsonify
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from flask_cors import CORS
from models import db
from family import Family

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['DEBUG'] = True
app.config['ENV'] = 'development'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://username:password@ipserver/database'

db.init_app(app)
Migrate(app, db)
CORS(app)
manager = Manager(app)
manager.add_command("db", MigrateCommand) # init, migrate, upgrade
fam = Family('Rodriguez')

@app.route('/')
def root():
    return render_template('index.html')

@app.route('/family/member', methods=['POST'])
def create():
    request_body = request.json
    if is_member_valid(request_body):
        fam.add_member(request_body)
        return jsonify({'status_code':'201','done':'true'}),201

    return jsonify({'status_code':'400'}),400

@app.route('/family/member/<int:member_id>', methods=['GET'])
def get_one(member_id):
    member = fam.get_member(member_id)
    if member is None:
        return jsonify({'error':'Member does not exist'})

    return jsonify(member)

@app.route('/family/member', methods=['GET'])
def index():
    all_members = fam.get_all_members()
        
    return jsonify(all_members)

@app.route('/family/member/<int:member_id>', methods=['DELETE'])
def delete(member_id):
    member = fam.delete_member(member_id)
    if member == []:
        return jsonify({'error':'Member does not exist'})

    return jsonify({'status_code':'200', 'done': 'true'})


def is_member_valid(member):
    valid_member = (member != None and member != {} and 'name' in member and member['name'] != '' and 
    'age' in member and member['age'] > 0 and
    'lucky_numbers' in member and type(member['lucky_numbers']) == list)

    return valid_member
    
if __name__ == '__main__':
    manager.run()