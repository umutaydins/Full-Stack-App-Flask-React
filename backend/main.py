from flask import request, jsonify
from config import app, db
from models import Contact
#create
# - first_name , -last_name, -email
#localhost:3000/create_contact


@app.route("/contacts", methods=["GET"])
def get_contacts():
    contacts = Contact.query.all()
    json_contacts = list(map(lambda x: x.to_json(), contacts))
    return jsonify({"contacts": json_contacts}), 200


@app.route("/create_contact", methods=["POST"])
def create_contact():
    first_name = request.json.get("firstName")
    last_name = request.json.get("lastName")
    email = request.json.get("email")
    


    if not first_name or not last_name or not email:
        return (
            jsonify({"error": "Missing data"}), 400,
            )
    new_contact = Contact(first_name=first_name, last_name=last_name, email=email)
    
    try:
        db.session.add(new_contact)
        db.session.commit()
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    return jsonify({"message": "User is created"}), 201

@app.route("/update_contact/<int:user_id>")
def update_contact(user_id):
    #contact.query.filter_by(id=user_id).update(dict(first_name="new_first_name"))
     contact =Contact.quary.get(user_id)
     if not contact:
         return jsonify({"massage": "contact not fount"}),404
     
     data =request.json
     contact.first_name = data.get("first_name")
     contact.last_name = data.get("last_name")
     contact.email = data.get("email")

     db.session.commit()
     
     return jsonify({"massage": "contact updated"}),200


@app.route("/delete_contact/<int:id>", methods=["DELETE"])
def delete_contact(user_id):
    contact = Contact.quary.get(user_id)
    if not contact:
        return jsonify({"error: contact not found"}), 404
    db.session.delete(contact)
    db.session.commit()

    return jsonify({"massage":"contact deleted"}),200


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)