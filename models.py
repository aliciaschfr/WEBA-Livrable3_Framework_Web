from flask import Flask
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()
app = Flask(__name__)


class F1Team(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    team_name = db.Column(db.String(100), nullable=False)
    driver1 = db.Column(db.String(100), nullable=False)
    driver2 = db.Column(db.String(100), nullable=False)
    circuit = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    teams = db.relationship('F1Team', backref='user', lazy=True)
class Model:
    @staticmethod
    def get_available_drivers():
        return [
            "Charles Leclerc",
            "Lewis Hamilton",
            "Valtteri Bottas",
            "Max Verstappen",
            "Sergio Perez",
            "Daniel Ricciardo",
            "Lando Norris",
            "Carlos Sainz",
            "Sebastian Vettel",
            "Lance Stroll",
            "Fernando Alonso",
            "Esteban Ocon",
            "Pierre Gasly",
            "Yuki Tsunoda",
        ]

    @staticmethod
    def get_available_circuits():
        return [
            "Circuit de Monaco",
            "Circuit de Barcelone-Catalunya",
            "Circuit Paul Ricard",
            "Red Bull Ring",
            "Silverstone Circuit",
            "Hungaroring",
            "Circuit de Spa-Francorchamps",
            "Autodromo Nazionale Monza",
            "Sochi Autodrom",
            "Circuit de Suzuka",
            "Circuit of the Americas",
            "Autódromo José Carlos Pace (Interlagos)",
            "Yas Marina Circuit",
            "Bahrain International Circuit",
            "Baku City Circuit",
            "Hockenheimring",
            "Zandvoort Circuit",
            "Algarve International Circuit",
            "Circuit de Catalunya",
            "Circuit Zolder",
            "Imola Circuit",
            "Autódromo Hermanos Rodríguez",
            "Jeddah Street Circuit",
            "Melbourne Grand Prix Circuit",
            "Adelaide Street Circuit",
        ]

    @staticmethod
    def get_available_teams():
        return [
            "Scuderia Ferrari",
            "Mercedes-AMG Petronas Formula One Team",
            "Red Bull Racing",
            "McLaren F1 Team",
            "Alpine F1 Team",
            "Aston Martin Cognizant Formula One Team",
            "Scuderia AlphaTauri",
            "Alfa Romeo Racing ORLEN",
            "Uralkali Haas F1 Team",
            "Williams Racing"
        ]
