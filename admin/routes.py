from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from admin.decorators import admin_required
from models import db, Match, Prediction, User, Comment
from datetime import datetime, timezone

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.route('/dashboard')
@login_required
@admin_required
def dashboard():
    """Panel principal de administrador"""
    matches_count = Match.query.count()
    predictions_count = Prediction.query.count()
    users_count = User.query.filter_by(is_admin=False).count()  # ← Solo usuarios NO admin
    
    recent_matches = Match.query.order_by(Match.kickoff_at.desc()).limit(10).all()
    
    return render_template('admin/dashboard.html',
                         matches_count=matches_count,
                         predictions_count=predictions_count,
                         users_count=users_count,
                         recent_matches=recent_matches)

@admin_bp.route('/matches')
@login_required
@admin_required
def list_matches():
    """Listar todos los partidos"""
    matches = Match.query.order_by(Match.kickoff_at).all()
    now = datetime.now(timezone.utc)
    
    # Agregar flag a cada partido indicando si ya comenzó
    for match in matches:
        kickoff = match.kickoff_at
        if kickoff.tzinfo is None:
            kickoff = kickoff.replace(tzinfo=timezone.utc)
        match.has_started = now >= kickoff
        match.minutes_until_start = int((kickoff - now).total_seconds() // 60) if not match.has_started else 0
    
    return render_template('admin/matches.html', matches=matches)

@admin_bp.route('/matches/new', methods=['GET', 'POST'])
@login_required
@admin_required
def create_match():
    """Crear un nuevo partido"""
    if request.method == 'POST':
        home_team = request.form.get('home_team', '').strip()
        away_team = request.form.get('away_team', '').strip()
        phase_id = request.form.get('phase_id', type=int)
        
        if not home_team or not away_team:
            flash('Ambos equipos son requeridos', 'error')
            return redirect(url_for('admin.create_match'))
        
        if not phase_id:
            flash('Debes seleccionar una fecha', 'error')
            return redirect(url_for('admin.create_match'))
        
        if home_team.lower() == away_team.lower():
            flash('Los equipos no pueden ser iguales', 'error')
            return redirect(url_for('admin.create_match'))
        
        try:
            kickoff_str = request.form.get('kickoff_at')
            kickoff_at = datetime.fromisoformat(kickoff_str).replace(tzinfo=timezone.utc)
            
            closes_str = request.form.get('closes_at')
            closes_at = datetime.fromisoformat(closes_str).replace(tzinfo=timezone.utc)
        except ValueError:
            flash('Formato de fecha inválido', 'error')
            return redirect(url_for('admin.create_match'))
        
        if closes_at >= kickoff_at:
            flash('El cierre debe ser antes del kickoff', 'error')
            return redirect(url_for('admin.create_match'))
        
        # Verificar que no exista un partido igual
        existing = Match.query.filter_by(
            home_team=home_team,
            away_team=away_team,
            kickoff_at=kickoff_at
        ).first()
        
        if existing:
            flash('Este partido ya existe', 'error')
            return redirect(url_for('admin.create_match'))
        
        match = Match(
            home_team=home_team,
            away_team=away_team,
            kickoff_at=kickoff_at,
            closes_at=closes_at,
            phase_id=phase_id
        )
        
        db.session.add(match)
        db.session.commit()
        
        flash(f'Partido "{home_team} vs {away_team}" creado exitosamente', 'success')
        return redirect(url_for('admin.list_matches'))
    
    # GET: Obtener todas las fases para el dropdown
    from models import Phase
    phases = Phase.query.order_by(Phase.order).all()
    return render_template('admin/create_match.html', phases=phases)

@admin_bp.route('/matches/<int:match_id>/edit', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_match(match_id):
    """Editar un partido"""
    match = Match.query.get_or_404(match_id)
    
    if request.method == 'POST':
        match.home_team = request.form.get('home_team', '').strip()
        match.away_team = request.form.get('away_team', '').strip()
        
        try:
            kickoff_str = request.form.get('kickoff_at')
            match.kickoff_at = datetime.fromisoformat(kickoff_str).replace(tzinfo=timezone.utc)
            
            closes_str = request.form.get('closes_at')
            match.closes_at = datetime.fromisoformat(closes_str).replace(tzinfo=timezone.utc)
        except ValueError:
            flash('Formato de fecha inválido', 'error')
            return redirect(url_for('admin.edit_match', match_id=match_id))
        
        db.session.commit()
        flash(f'Partido {match.home_team} vs {match.away_team} actualizado', 'success')
        return redirect(url_for('admin.list_matches'))
    
    return render_template('admin/edit_match.html', match=match)

@admin_bp.route('/matches/<int:match_id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_match(match_id):
    """Eliminar un partido"""
    match = Match.query.get_or_400(match_id)
    
    # Guardar nombre del partido antes de eliminarlo
    match_name = f"{match.home_team} vs {match.away_team}"
    
    # Eliminar todos los pronósticos asociados
    Prediction.query.filter_by(match_id=match_id).delete()
    
    # Eliminar el partido
    db.session.delete(match)
    db.session.commit()
    
    flash(f'Partido "{match_name}" eliminado correctamente', 'success')
    return redirect(url_for('admin.list_matches'))

@admin_bp.route('/matches/<int:match_id>/result', methods=['POST'])
@login_required
@admin_required
def set_result(match_id):
    """Cargar resultado de un partido y calcular puntos"""
    match = Match.query.get_or_404(match_id)

    # Bloquear carga si el partido aún no comenzó
    now = datetime.now(timezone.utc)
    kickoff = match.kickoff_at
    if kickoff.tzinfo is None:
        kickoff = kickoff.replace(tzinfo=timezone.utc)

    if now < kickoff:
        flash('No puedes cargar el resultado antes del kickoff', 'error')
        return redirect(url_for('admin.list_matches'))

    try:
        home_goals = int(request.form.get('home_goals', 0))
        away_goals = int(request.form.get('away_goals', 0))
    except ValueError:
        flash('Goles inválidos', 'error')
        return redirect(url_for('admin.list_matches'))

    if home_goals < 0 or away_goals < 0:
        flash('Los goles no pueden ser negativos', 'error')
        return redirect(url_for('admin.list_matches'))

    match.home_goals = home_goals
    match.away_goals = away_goals
    db.session.commit()

    predictions = Prediction.query.filter_by(match_id=match_id).all()
    for prediction in predictions:
        prediction.points_awarded = prediction.calculate_points()

    db.session.commit()

    flash(f'Resultado: {match.home_team} {home_goals} - {away_goals} {match.away_team}. Puntos calculados.', 'success')
    return redirect(url_for('admin.list_matches'))

# ==================== RUTAS DE USUARIOS ====================

@admin_bp.route('/users')
@login_required
@admin_required
def manage_users():
    """Gestionar usuarios (excluye admins)"""
    # Obtener SOLO usuarios que NO son admin
    users = User.query.filter_by(is_admin=False).all()
    
    return render_template('admin/users.html', users=users)

@admin_bp.route('/users/<int:user_id>')
@login_required
@admin_required
def view_user(user_id):
    """Ver detalles de un usuario"""
    user = User.query.get_or_404(user_id)
    predictions = Prediction.query.filter_by(user_id=user_id).all()
    return render_template('admin/view_user.html', user=user, predictions=predictions)

@admin_bp.route('/users/<int:user_id>/toggle', methods=['POST'])
@login_required
def toggle_user(user_id):
    """Habilitar/deshabilitar usuario"""
    if not current_user.is_admin:
        flash('No tienes permiso', 'error')
        return redirect(url_for('main.index'))
    
    user = User.query.get_or_404(user_id)
    
    # No permitir cambiar estado de admins
    if user.is_admin:
        flash('No puedes modificar admins', 'error')
        return redirect(url_for('admin.manage_users'))
    
    user.is_enabled = not user.is_enabled
    db.session.commit()
    
    status = 'habilitado' if user.is_enabled else 'deshabilitado'
    flash(f'Usuario {status}', 'success')
    return redirect(url_for('admin.manage_users'))

@admin_bp.route('/users/<int:user_id>/delete', methods=['POST'])
@login_required
def delete_user(user_id):
    """Eliminar usuario"""
    if not current_user.is_admin:
        flash('No tienes permiso', 'error')
        return redirect(url_for('main.index'))
    
    user = User.query.get_or_404(user_id)
    
    # No permitir eliminar admins
    if user.is_admin:
        flash('No puedes eliminar admins', 'error')
        return redirect(url_for('admin.manage_users'))
    
    # Eliminar pronósticos asociados primero
    Prediction.query.filter_by(user_id=user_id).delete()
    db.session.delete(user)
    db.session.commit()
    
    flash(f'Usuario {user.name} eliminado', 'success')
    return redirect(url_for('admin.manage_users'))

@admin_bp.route('/users/<int:user_id>/edit', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_user(user_id):
    """Editar información del usuario"""
    user = User.query.get_or_404(user_id)
    
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        
        if not name:
            flash('El nombre es requerido', 'error')
            return redirect(url_for('admin.edit_user', user_id=user_id))
        
        if not email:
            flash('El email es requerido', 'error')
            return redirect(url_for('admin.edit_user', user_id=user_id))
        
        # Verificar si el email ya existe (excepto el del usuario actual)
        existing = User.query.filter_by(email=email).filter(User.id != user_id).first()
        if existing:
            flash('Este email ya está registrado', 'error')
            return redirect(url_for('admin.edit_user', user_id=user_id))
        
        user.name = name
        user.email = email
        db.session.commit()
        
        flash(f'Usuario {name} actualizado correctamente', 'success')
        return redirect(url_for('admin.manage_users'))
    
    return render_template('admin/edit_user.html', user=user)

# ==================== RUTAS DE COMENTARIOS ====================

@admin_bp.route('/comments')
@login_required
@admin_required
def manage_comments():
    """Gestionar comentarios del tablón"""
    comments = Comment.query.order_by(Comment.created_at.desc()).all()
    return render_template('admin/comments.html', comments=comments)

@admin_bp.route('/comments/<int:comment_id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_comment(comment_id):
    """Eliminar comentario"""
    comment = Comment.query.get_or_404(comment_id)
    user_name = comment.user.name
    
    db.session.delete(comment)
    db.session.commit()
    
    flash(f'Comentario de {user_name} eliminado', 'success')
    return redirect(url_for('admin.manage_comments'))

