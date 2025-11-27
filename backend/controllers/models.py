from controllers.database import db
from flask_security import UserMixin, RoleMixin

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(255), unique = True, nullable = False)
    password = db.Column(db.String(255), nullable = False)
    active = db.Column(db.Boolean, default = True)

    fs_uniquifier = db.Column(db.String(255), unique = True, nullable=False)
    fs_token_uniquifier = db.Column(db.String(255), unique = True, nullable = False)

    roles = db.relationship("Role", secondary="user_roles", backref=db.backref("users", lazy="dynamic"))

class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True)
    description = db.Column(db.String(255))


class UserRoles(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    role_id = db.Column(db.Integer, db.ForeignKey("role.id"))

class Doctor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    age = db.Column(db.Integer)
    gender = db.Column(db.String(50))
    phone = db.Column(db.String(20))
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), unique=True)
    specialization = db.Column(db.String(255), nullable = False)
    availability = db.Column(db.JSON)
    description = db.Column(db.String(255))
    is_active = db.Column(db.Boolean, default = True)

    user = db.relationship("User", backref="doctor_profile")

    def __repr__(self):
        return f"<Doctor {self.name}>"

    
class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), unique=True)

    name = db.Column(db.String(255), nullable=False)
    age = db.Column(db.Integer)
    gender = db.Column(db.String(50))
    phone = db.Column(db.String(20))
    address = db.Column(db.String(255))

    user = db.relationship("User", backref="patient_profile")

    def __repr__(self):
        return f"<Patient {self.name}>"


class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key = True)

    patient_id = db.Column(db.Integer, db.ForeignKey("patient.id"))
    doctor_id = db.Column(db.Integer, db.ForeignKey("doctor.id"))

    date = db.Column(db.String(200))
    time = db.Column(db.String(200))
    status = db.Column(db.String(20), default = "Booked")

    patient = db.relationship("Patient", backref="patient_appointments")
    doctor = db.relationship("Doctor", backref="doctor_appointments")



class Treatment(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    appointment_id = db.Column(db.Integer, db.ForeignKey("appointment.id"))
    diagnosis = db.Column(db.String(500))
    prescription = db.Column(db.String(500))
    notes = db.Column(db.String(500))
    next_visit = db.Column(db.String(200))

    appointment = db.relationship("Appointment", backref="treatment")