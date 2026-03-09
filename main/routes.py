from flask import Blueprint, render_template, request, redirect, url_for, flash, make_response
from flask_login import login_required, current_user
from models import db, Match, Prediction, User, Phase, Comment
from sqlalchemy import func, case
from datetime import datetime, timezone
from auto_backup import backup_on_change  # BACKUP AUTOMÁTICO

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
    
    # Crear respuesta con headers anti-caché
    response = make_response(render_template('main/index.html', 
                                            recent_comments=recent_comments,
                                            next_matches=next_matches,
                                            first_match=first_match))
    
    # Headers para prevenir caché en navegadores (móviles y desktop)
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    
    return response

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
        if match_id is not None and home_goals is not None and away_goals is not None:
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
            # 🔒 BACKUP AUTOMÁTICO después de guardar pronóstico
            backup_on_change("pronostico")
            flash('Pronóstico guardado', 'success')
            return redirect(url_for('main.predictions'))
        # Si POST pero sin datos válidos, redirigir
        return redirect(url_for('main.predictions'))

    # GET: mostrar solo partidos abiertos
    now = datetime.now(timezone.utc)
    matches = Match.query.filter(Match.closes_at > now).order_by(Match.kickoff_at).all()
    # Obtener pronósticos del usuario actual
    user_predictions = {}
    for prediction in current_user.predictions:
        user_predictions[prediction.match_id] = prediction
    return render_template('main/predictions.html', 
                         matches=matches,
                         predictions=user_predictions)


@main_bp.route('/predictions/delete/<int:match_id>', methods=['POST'])
@login_required
def delete_prediction(match_id):
    """Borrar pronóstico de un partido para el usuario actual"""
    prediction = Prediction.query.filter_by(user_id=current_user.id, match_id=match_id).first()
    if prediction:
        db.session.delete(prediction)
        db.session.commit()
        db.session.expunge_all()
        backup_on_change("pronostico")
        flash('Pronóstico eliminado', 'info')
    else:
        flash('No hay pronóstico para borrar', 'warning')
    return redirect(url_for('main.predictions'))

    if request.method == 'POST':
        match_id = request.form.get('match_id', type=int)
        home_goals = request.form.get('home_goals')
        away_goals = request.form.get('away_goals')
        if match_id is not None and home_goals is not None and away_goals is not None:
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
            # Eliminar cualquier duplicado antes de crear
            existing = Prediction.query.filter_by(user_id=current_user.id, match_id=match_id).first()
            if existing:
                existing.home_goals = home_goals
                existing.away_goals = away_goals
                db.session.commit()
            else:
                # Por seguridad, eliminar cualquier predicción zombie
                Prediction.query.filter_by(user_id=current_user.id, match_id=match_id).delete()
                db.session.commit()
                db.session.expunge_all()
                prediction = Prediction(
                    user_id=current_user.id,
                    match_id=match_id,
                    home_goals=home_goals,
                    away_goals=away_goals
                )
                db.session.add(prediction)
                db.session.commit()
            # 🔒 BACKUP AUTOMÁTICO después de guardar pronóstico
            backup_on_change("pronostico")
            flash('Pronóstico guardado', 'success')
            return redirect(url_for('main.predictions'))
        # Si POST pero sin datos válidos, redirigir
        return redirect(url_for('main.predictions'))
    
    # GET: mostrar solo partidos abiertos
    from datetime import datetime, timezone
    now = datetime.now(timezone.utc)
    matches = Match.query.filter(Match.closes_at > now).order_by(Match.kickoff_at).all()
    
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
    user_stats_raw = db.session.query(
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
    
    # Agregar manualmente el conteo de predicciones para partidos finalizados
    user_stats = []
    for stat in user_stats_raw:
        # Contar pronósticos que hizo este usuario PARA partidos que tienen resultado cargado
        preds_for_finished = db.session.query(func.count(Prediction.id))\
            .join(Match, Prediction.match_id == Match.id)\
            .filter(Prediction.user_id == stat.id, Match.home_goals.isnot(None))\
            .scalar() or 0
        
        # Crear tupla con el campo adicional
        from collections import namedtuple
        StatWithPoints = namedtuple('StatWithPoints', ['id', 'name', 'email', 'total_predictions', 'total_points', 'predictions_with_points'])
        user_stats.append(StatWithPoints(stat.id, stat.name, stat.email, stat.total_predictions, stat.total_points, preds_for_finished))
    
    # Calcular cuántos partidos tienen resultado cargado hasta ahora
    matches_with_result = Match.query.filter(Match.home_goals.isnot(None)).count()
    
    return render_template('main/rankings.html', 
                         user_stats=user_stats,
                         matches_with_result=matches_with_result,
                         zip=zip)

@main_bp.route('/rankings/phase/<int:phase_id>')
def rankings_by_phase(phase_id):
    """Rankings por fase específica (excluye admins)"""
    phase = Phase.query.get_or_404(phase_id)
    # Mostrar 'Fecha 4' en vez de 'Fecha 4 - Eliminación directa'
    phase_name = phase.name
    if phase_name.strip().lower().startswith('fecha 4'):
        phase_name = 'Fecha 4'
    

    # Obtener puntajes de usuarios SOLO para esta fase
    user_stats = (
        db.session.query(
            User.id,
            User.name,
            User.email,
            func.count(Prediction.id).label('total_predictions'),
            func.sum(Prediction.points_awarded).label('total_points')
        )
        .join(Prediction, User.id == Prediction.user_id)
        .join(Match, Prediction.match_id == Match.id)
        .filter(Match.phase_id == phase_id, User.is_admin == False)
        .group_by(User.id)
        .order_by(func.coalesce(func.sum(Prediction.points_awarded), 0).desc(), User.name)
        .all()
    )

    # Si no hay user_stats (ej. fecha 4 sin partidos jugados), mostrar todos los usuarios no-admin con 0 puntos
    if not user_stats:
        users = User.query.filter_by(is_admin=False).order_by(User.name).all()
        from collections import namedtuple
        StatWithPoints = namedtuple('StatWithPoints', ['id', 'name', 'email', 'total_predictions', 'total_points', 'predictions_with_points'])
        user_stats = [StatWithPoints(u.id, u.name, u.email, 0, 0, 0) for u in users]

    # Obtener todas las fases para el menú
    phases = Phase.query.order_by(Phase.order).all()
    # Generar lista de nombres corregidos para el menú (siempre 'Fecha N')
    phase_names = []
    for p in phases:
        n = p.name
        if n.strip().lower().startswith('fecha'):
            import re
            m = re.match(r'fecha\s*(\d+)', n.strip().lower())
            if m:
                n = f'Fecha {m.group(1)}'
            else:
                n = 'Fecha'
        phase_names.append(n)

    return render_template('main/rankings_phase.html', 
                         phase=phase, 
                         phase_name=phase_name,
                         user_stats=user_stats,
                         phases=phases,
                         phase_names=phase_names,
                         zip=zip)

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
    users = User.query.filter_by(is_admin=False).order_by(User.id).all()

    # precargar pronósticos
    predictions = Prediction.query.all()
    pred_map = {(p.user_id, p.match_id): p for p in predictions}

    phase_data = []
    for phase in phases:
        matches = Match.query.filter_by(phase_id=phase.id).order_by(Match.kickoff_at).all()
        if not matches:
            continue

        # Calcular porcentaje de aciertos (batacazo) para cada partido
        batacazo_percentages = []
        total_participants = len(users)
        for match in matches:
            if match.home_goals is None or match.away_goals is None or total_participants == 0:
                batacazo_percentages.append(None)
                continue
            match_result = None
            if match.home_goals > match.away_goals:
                match_result = 'home'
            elif match.home_goals < match.away_goals:
                match_result = 'away'
            else:
                match_result = 'draw'

            # Contar cuántos usuarios acertaron el ganador/empate
            correct_count = 0
            for user in users:
                p = pred_map.get((user.id, match.id))
                if not p:
                    continue
                # Solo cuenta si el usuario pronosticó
                if p.home_goals > p.away_goals:
                    user_result = 'home'
                elif p.home_goals < p.away_goals:
                    user_result = 'away'
                else:
                    user_result = 'draw'
                if user_result == match_result:
                    correct_count += 1
            percent = (correct_count / total_participants) * 100 if total_participants > 0 else 0
            batacazo_percentages.append(percent)

        # Reemplazar nombre de fase 4
        phase_name = phase.name
        if phase_name.strip().lower().startswith('fecha 4'):
            phase_name = 'Fecha 4'

        phase_data.append({
            'phase': phase,
            'phase_name': phase_name,
            'matches': matches,
            'users': users,
            'pred_map': pred_map,
            'batacazo_percentages': batacazo_percentages
        })

    return render_template('main/all_predictions.html', phase_data=phase_data)

@main_bp.route('/reglamento')
def reglamento():
    """Reglamento del Prode Mundial 2026"""
    return render_template('main/reglamento.html')

@main_bp.route('/azar')
def azar():
    """Información sobre el participante Azar"""
    return render_template('main/azar.html')

@main_bp.route('/glosario')
def glosario():
    """Glosario de países del Mundial 2026 - Genera dinámicamente desde FIFA_COUNTRIES (211 países)"""
    from fifa_countries import FIFA_COUNTRIES
    
    # Convertir a lista ordenada por código FIFA
    countries = [
        {'code': code, 'iso2': iso2, 'name': name}
        for code, (iso2, name) in sorted(FIFA_COUNTRIES.items())
    ]
    
    return render_template('main/glosario.html', countries=countries)

@main_bp.route('/tablon', methods=['GET', 'POST'])
def tablon():
    """Página del tablón de comentarios (visible sin login, pero agregar comentario requiere login)"""
    if request.method == 'POST':
        # Para agregar comentarios se requiere autenticación
        if not current_user.is_authenticated:
            flash('Debes iniciar sesión para publicar comentarios', 'error')
            return redirect(url_for('auth.login'))
        
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
