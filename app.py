#app.py
from models import Model, User
from flask import jsonify
from datetime import datetime
from flask import Flask, render_template, session, redirect, url_for, request, jsonify
import requests
from models import F1Team, db
from operator import itemgetter


app = Flask(__name__)
app.secret_key = 'secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db.init_app(app)
app.app_context().push()
with app.app_context():
    db.create_all()
    # db.drop_all()


@app.route('/')
def home():
    logged_in = 'username' in session
    return render_template('index.html', logged_in=logged_in)


def get_last_race_results():
    try:
        response = requests.get('https://ergast.com/api/f1/2024/results')
        response.raise_for_status()  # Lève une exception pour les codes d'état HTTP >= 400
        data = response.json()  # Tentative de décodage de la réponse JSON
        return data
    except requests.exceptions.RequestException as e:
        print("Failed to retrieve last race results:", e)
        return None
    except ValueError as e:
        print("Failed to parse JSON:", e)
        return None

@app.route('/dernier_resultat')
def dernier_resultat():
    last_race_results = get_last_race_results()
    if last_race_results:
        # Traitement des résultats de la course
        # Vous pouvez passer ces résultats à votre modèle de rendu
        return render_template('dernier_resultat.html', last_race_results=last_race_results)
    else:
        # Gérer le cas où les résultats de la course ne peuvent pas être récupérés
        return jsonify({'error': 'Failed to retrieve last race results'}), 500


@app.route('/drivers')
def index():
    response = requests.get('https://api.openf1.org/v1/drivers')
    if response.status_code == 200:
        drivers_data = response.json()

        unique_drivers_dict = {}

        for driver in drivers_data:
            full_name = driver['full_name']
            if full_name not in unique_drivers_dict:
                unique_drivers_dict[full_name] = driver

        unique_drivers_list = list(unique_drivers_dict.values())

        return render_template('drivers.html', pilotes=unique_drivers_list)
    else:
        print("Failed to retrieve driver data")


@app.route('/drivers')
def drivers():
    response = requests.get('https://api.openf1.org/v1/drivers')

    if response.status_code == 200:
        pilotes = response.json()
        return render_template('drivers.html', pilotes=pilotes)  # Utilisation de "pilotes" comme nom de variable
    else:
        return jsonify({"error": "Failed to retrieve driver data"}), 500


@app.route('/liste_ecurie')
def liste_ecurie():
    if 'username' not in session:
        return redirect(url_for('register'))

    user = User.query.filter_by(username=session['username']).first()
    teams = user.teams

    return render_template('liste_ecurie.html', teams=teams)


@app.route('/create_team', methods=['GET', 'POST'])
def create_team():
    if 'username' not in session:
        return redirect(url_for('register'))

    if request.method == 'POST':
        team_name = request.form['team_name']
        driver1 = request.form['driver1']
        driver2 = request.form['driver2']
        circuit = request.form['circuit']

        # Récupérer l'utilisateur à partir de la session
        user = User.query.filter_by(username=session['username']).first()

        # Vérifier si l'utilisateur existe
        if user:
            # Créer une nouvelle équipe associée à l'utilisateur actuel
            new_team = F1Team(team_name=team_name, driver1=driver1, driver2=driver2, circuit=circuit, user_id=user.id)
            db.session.add(new_team)
            db.session.commit()

            return redirect(url_for('liste_ecurie'))
        else:
            # Gérer le cas où l'utilisateur n'existe pas
            return "Utilisateur non trouvé", 404
    else:
        names = Model.get_available_teams()
        drivers = Model.get_available_drivers()
        circuits = Model.get_available_circuits()
        return render_template('create_team.html', names=names, drivers=drivers, circuits=circuits)


@app.route('/edit_team/<int:team_id>', methods=['GET', 'POST'])
def edit_team(team_id):

    team = F1Team.query.get_or_404(team_id)

    if request.method == 'POST':
        team.team_name = request.form['team_name']
        team.driver1 = request.form['driver1']
        team.driver2 = request.form['driver2']
        team.circuit = request.form['circuit']

        db.session.commit()

        return redirect(url_for('liste_ecurie'))
    else:
        return render_template('edit_team.html', team=team)


@app.route('/delete_team/<int:team_id>', methods=['POST'])
def delete_team(team_id):

    team = F1Team.query.get_or_404(team_id)
    db.session.delete(team)
    db.session.commit()
    return redirect(url_for('liste_ecurie'))


@app.route('/prediction', methods=['GET', 'POST'])
def prediction():
    if 'username' not in session:
        return redirect(url_for('register'))
    drivers = ["Lewis Hamilton", "Valtteri Bottas", "Max Verstappen", "Sergio Perez"]
    teams = ["Mercedes", "Red Bull Racing", "McLaren", "Ferrari"]
    circuits = ["Circuit de Barcelone-Catalogne", "Circuit de Monaco", "Circuit Paul Ricard", "Red Bull Ring"]

    if request.method == 'POST':
        driver1 = request.form['driver1']
        driver2 = request.form['driver2']
        circuit = request.form['circuit']
        winner = request.form['winner']
        pole_position = request.form['pole_position']
        best_lap = request.form['best_lap']
        laps_led = request.form['laps_led']
        pit_stops = request.form['pit_stops']
        winning_team = request.form['winning_team']
        weather = request.form['weather']
        final_rankings = request.form['final_rankings']

        return render_template('prediction.html', prediction={
            'driver1': driver1,
            'driver2': driver2,
            'circuit': circuit,
            'winner': winner,
            'pole_position': pole_position,
            'best_lap': best_lap,
            'laps_led': laps_led,
            'pit_stops': pit_stops,
            'winning_team': winning_team,
            'weather': weather,
            'final_rankings': final_rankings
        }, drivers=drivers, teams=teams, circuits=circuits)

    return render_template('prediction.html', drivers=drivers, teams=teams, circuits=circuits)


@app.route('/circuits')
def circuits():
    response = requests.get('https://api.openf1.org/v1/meetings')

    if response.status_code == 200:
        meetings_data = response.json()

        circuits_info = []

        for meeting in meetings_data:
            circuit_name = meeting['circuit_short_name']
            country_name = meeting['country_name']
            location = meeting['location']
            image_filename = circuit_name.replace(" ", "_") + ".png"
            image_url = url_for('static', filename='circuits/' + image_filename)

            circuits_info.append({
                'name': circuit_name,
                'country': country_name,
                'location': location,
                'image_url': image_url
            })

        return render_template('circuits.html', circuits=circuits_info)
    else:
        return 'Failed to retrieve circuit data', 500

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            error_message = 'Ce nom d\'utilisateur est déjà pris. Veuillez en choisir un autre.'
            return render_template('register.html', error=error_message)

        new_user = User(username=username, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('login'))
    else:
        return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username, password=password).first()

        if user:
            session['username'] = username
            return redirect(url_for('home'))
        else:
            error_message = 'Nom d\'utilisateur ou mot de passe incorrect.'
            return render_template('login.html', error=error_message)
    else:
        return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)