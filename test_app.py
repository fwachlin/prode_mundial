from flask import Flask, render_template_string
from extensions import db
from models import User, Match, Prediction, Phase

app = Flask(__name__, instance_relative_config=True)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///prode.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'test'
db.init_app(app)

TEMPLATE = """
<!DOCTYPE html>
<html>
<head><title>Test</title></head>
<body>
<h1>Test All Predictions</h1>

<p>Phase data blocks: {{ phase_data|length }}</p>

{% for block in phase_data %}
    <h2>{{ block.phase.name }}</h2>
    <p>Partidos: {{ block.matches|length }}</p>
    <p>Usuarios: {{ block.users|length }}</p>
    
    <table border="1">
        <tr>
            <th>Usuario</th>
            {% for match in block.matches[:3] %}
                <th>{{ match.home_team }} vs {{ match.away_team }}</th>
            {% endfor %}
        </tr>
        {% for user in block.users %}
        <tr>
            <td>{{ user.name }}</td>
            {% for match in block.matches[:3] %}
                {% set p = block.pred_map.get((user.id, match.id)) %}
                <td>{% if p %}{{ p.home_goals }}-{{ p.away_goals }}{% else %}—{% endif %}</td>
            {% endfor %}
        </tr>
        {% endfor %}
    </table>
    <br>
{% endfor %}

</body>
</html>
"""

@app.route('/test')
def test():
    phases = Phase.query.order_by(Phase.order).all()
    users = User.query.filter(User.is_admin == False).order_by(User.name).all()
    predictions = Prediction.query.all()
    pred_map = {(p.user_id, p.match_id): p for p in predictions}
    
    phase_data = []
    for phase in phases:
        if 'Eliminación Directa' in phase.name or phase.name == 'Fecha 4':
            continue
        matches = Match.query.filter_by(phase_id=phase.id).order_by(Match.kickoff_at).all()
        if not matches:
            continue
        phase_data.append({
            'phase': phase,
            'matches': matches,
            'users': users,
            'pred_map': pred_map
        })
    
    return render_template_string(TEMPLATE, phase_data=phase_data)

if __name__ == '__main__':
    app.run(debug=True, port=5001)
