from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from models import db, Match, Prediction, User, Phase, Comment
from sqlalchemy import func
from datetime import datetime, timezone

main_bp = Blueprint('main', __name__, url_prefix='')

@main_bp.route('/')
def index():
    """Página de inicio"""
    # Obtener últimos 5 comentarios (más recientes primero)
    recent_comments = Comment.query.order_by(Comment.created_at.desc()).limit(5).all()
    
    # Obtener próximos 5 partidos sin resultado
    now = datetime.now(timezone.utc)
    next_matches = Match.query.filter(
        Match.home_goals == None,
        Match.away_goals == None,
        Match.kickoff_at >= now
    ).order_by(Match.kickoff_at).limit(5).all()
    
    # Obtener el primer partido del Mundial (para el countdown)
    first_match = Match.query.order_by(Match.kickoff_at).first()
    
    return render_template('main/index.html', 
                         recent_comments=recent_comments,
                         next_matches=next_matches,
                         first_match=first_match)

@main_bp.route('/predictions', methods=['GET', 'POST'])
@login_required
def predictions():
    """Vista de pronósticos"""
    # Los admins no pueden hacer pronósticos
    if current_user.is_admin:
        flash('Los administradores no pueden hacer pronósticos', 'warning')
        return redirect(url_for('main.index'))
    
    if request.method == 'POST':
        match_id = request.form.get('match_id', type=int)
        home_goals = request.form.get('home_goals')
        away_goals = request.form.get('away_goals')
        
        match = Match.query.get_or_404(match_id)
        
        # Validar que el pronóstico esté abierto (BACKEND)
        if not match.is_open():
            flash('Este pronóstico está cerrado', 'error')
            return redirect(url_for('main.predictions'))
        
        # Validar que ambos campos tengan valores
        if home_goals == '' or away_goals == '':
            flash('Debes ingresar ambos goles para guardar el pronóstico', 'warning')
            return redirect(url_for('main.predictions'))
        
        try:
            home_goals = int(home_goals)
            away_goals = int(away_goals)
        except ValueError:
            flash('Los goles deben ser números válidos', 'error')
            return redirect(url_for('main.predictions'))
        
        if home_goals < 0 or away_goals < 0:
            flash('Los goles no pueden ser negativos', 'error')
            return redirect(url_for('main.predictions'))
        
        # Buscar si ya existe pronóstico
        prediction = Prediction.query.filter_by(
            user_id=current_user.id,
            match_id=match_id
        ).first()
        
        if prediction:
            prediction.home_goals = home_goals
            prediction.away_goals = away_goals
        else:
            prediction = Prediction(
                user_id=current_user.id,
                match_id=match_id,
                home_goals=home_goals,
                away_goals=away_goals
            )
            db.session.add(prediction)
        
        db.session.commit()
        flash('Pronóstico guardado', 'success')
        return redirect(url_for('main.predictions'))
    
    # GET: mostrar pronósticos
    matches = Match.query.order_by(Match.kickoff_at).all()
    
    # Obtener pronósticos del usuario actual
    user_predictions = {}
    for prediction in current_user.predictions:
        user_predictions[prediction.match_id] = prediction
    
    return render_template('main/predictions.html', 
                         matches=matches,
                         predictions=user_predictions)

@main_bp.route('/rankings')
def rankings():
    """Rankings general de usuarios (excluye admins)"""
    # Obtener ranking general: suma de todos los puntos (SIN ADMINS)
    user_stats = db.session.query(
        User.id,
        User.name,
        User.email,
        func.count(Prediction.id).label('total_predictions'),
        func.sum(Prediction.points_awarded).label('total_points')
    ).join(Prediction, User.id == Prediction.user_id, isouter=True)\
     .filter(User.is_admin == False)\
     .group_by(User.id)\
     .order_by(func.coalesce(func.sum(Prediction.points_awarded), 0).desc(), User.name)\
     .all()
    
    return render_template('main/rankings.html', user_stats=user_stats)

@main_bp.route('/rankings/phase/<int:phase_id>')
def rankings_by_phase(phase_id):
    """Rankings por fase específica (excluye admins)"""
    phase = Phase.query.get_or_404(phase_id)
    
    # Obtener puntajes de usuarios SOLO para esta fase
    user_stats = db.session.query(
        User.id,
        User.name,
        User.email,
        func.count(Prediction.id).label('total_predictions'),
        func.sum(Prediction.points_awarded).label('total_points')
    ).join(Prediction, User.id == Prediction.user_id)\
     .join(Match, Prediction.match_id == Match.id)\
     .filter(Match.phase_id == phase_id, User.is_admin == False)\
     .group_by(User.id)\
     .order_by(func.coalesce(func.sum(Prediction.points_awarded), 0).desc(), User.name)\
     .all()
    
    # Obtener todas las fases para el menú
    phases = Phase.query.order_by(Phase.order).all()
    
    return render_template('main/rankings_phase.html', 
                         phase=phase, 
                         user_stats=user_stats,
                         phases=phases)

@main_bp.route('/rankings/matches/<int:match_id>')
def rankings_by_match(match_id):
    """Rankings por partido específico (excluye admins)"""
    match = Match.query.get_or_404(match_id)
    
    # Obtener pronósticos de este partido ordenados por puntos (SIN ADMINS)
    predictions = Prediction.query.join(User)\
                               .filter(Prediction.match_id == match_id,
                                      User.is_admin == False)\
                               .order_by(Prediction.points_awarded.desc())\
                               .all()
    
    return render_template('main/rankings_match.html', 
                     match=match, 
                     predictions=predictions)

@main_bp.route('/all-predictions')
def all_predictions():
    """Ver todos los pronósticos en tabla por fase"""
    phases = Phase.query.order_by(Phase.order).all()
    users = User.query.filter_by(is_admin=False).order_by(User.name).all()

    # precargar pronósticos
    predictions = Prediction.query.all()
    pred_map = {(p.user_id, p.match_id): p for p in predictions}

    phase_data = []
    for phase in phases:
        matches = Match.query.filter_by(phase_id=phase.id).order_by(Match.kickoff_at).all()
        
        if not matches:
            continue

        phase_data.append({
            'phase': phase,
            'matches': matches,
            'users': users,
            'pred_map': pred_map
        })

    return render_template('main/all_predictions.html', phase_data=phase_data)

@main_bp.route('/reglamento')
def reglamento():
    """Reglamento del Prode Mundial 2026"""
    return render_template('main/reglamento.html')

@main_bp.route('/tablon', methods=['GET', 'POST'])
@login_required
def tablon():
    """Página del tablón de comentarios"""
    if request.method == 'POST':
        content = request.form.get('content', '').strip()
        
        if not content:
            flash('El comentario no puede estar vacío', 'error')
            return redirect(url_for('main.tablon'))
        
        if len(content) > 500:
            flash('El comentario no puede exceder 500 caracteres', 'error')
            return redirect(url_for('main.tablon'))
        
        comment = Comment(user_id=current_user.id, content=content)
        db.session.add(comment)
        db.session.commit()
        
        flash('Comentario publicado', 'success')
        return redirect(url_for('main.tablon'))
    
    # Obtener últimos 10 comentarios (más recientes primero)
    comments = Comment.query.order_by(Comment.created_at.desc()).limit(10).all()
    
    return render_template('main/tablon.html', comments=comments)
