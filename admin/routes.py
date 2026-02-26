from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from admin.decorators import admin_required
from models import db, Match, Prediction, User, Comment, AllowedEmail
from datetime import datetime, timezone
from auto_backup import backup_on_change  # BACKUP AUTOMÁTICO

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.route('/dashboard')
@login_required
@admin_required
def dashboard():
    """Panel principal de administrador"""
    # Obtener TODOS los partidos para el dashboard
    matches = Match.query.order_by(Match.kickoff_at).all()
    now = datetime.now(timezone.utc)
    
    # Agregar flag a cada partido indicando si ya comenzó
    for match in matches:
        kickoff = match.kickoff_at
        if kickoff.tzinfo is None:
            kickoff = kickoff.replace(tzinfo=timezone.utc)
        match.has_started = now >= kickoff
        match.minutes_until_start = int((kickoff - now).total_seconds() // 60) if not match.has_started else 0
    
    return render_template('admin/dashboard.html', matches=matches)

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
        
        # Actualizar phase_id
        phase_id = request.form.get('phase_id', type=int)
        if phase_id:
            match.phase_id = phase_id
        
        try:
            kickoff_str = request.form.get('kickoff_at')
            match.kickoff_at = datetime.fromisoformat(kickoff_str).replace(tzinfo=timezone.utc)
            
            closes_str = request.form.get('closes_at')
            match.closes_at = datetime.fromisoformat(closes_str).replace(tzinfo=timezone.utc)
        except ValueError:
            flash('Formato de fecha inválido', 'error')
            return redirect(url_for('admin.edit_match', match_id=match_id))
        
        # Procesar home_goals y away_goals si vienen en el formulario
        home_goals_str = request.form.get('home_goals', '').strip()
        away_goals_str = request.form.get('away_goals', '').strip()
        
        if home_goals_str and away_goals_str:
            try:
                home_goals = int(home_goals_str)
                away_goals = int(away_goals_str)
                
                if home_goals < 0 or away_goals < 0:
                    flash('Los goles no pueden ser negativos', 'error')
                    return redirect(url_for('admin.edit_match', match_id=match_id))
                
                # Actualizar goles
                match.home_goals = home_goals
                match.away_goals = away_goals
                
                # Recalcular puntos de todos los pronósticos
                for prediction in match.predictions:
                    prediction.points_awarded = prediction.calculate_points()
                
                # 🔒 BACKUP AUTOMÁTICO después de cargar resultado
                db.session.commit()
                backup_on_change("resultado")
                
                flash(f'Resultado cargado: {match.home_team} {home_goals} - {away_goals} {match.away_team}. Puntos recalculados.', 'success')
            except ValueError:
                flash('Formato de goles inválido', 'error')
                return redirect(url_for('admin.edit_match', match_id=match_id))
        else:
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
    
    # 🔒 BACKUP AUTOMÁTICO después de cargar resultado
    backup_on_change("resultado")

    flash(f'Resultado: {match.home_team} {home_goals} - {away_goals} {match.away_team}. Puntos calculados.', 'success')
    return redirect(url_for('admin.list_matches'))

@admin_bp.route('/matches/<int:match_id>/delete-result', methods=['POST'])
@login_required
@admin_required
def delete_result(match_id):
    """Borrar resultado de un partido y recalcular puntos"""
    match = Match.query.get_or_404(match_id)

    if match.home_goals is None and match.away_goals is None:
        flash('Este partido no tiene resultado cargado', 'warning')
        return redirect(url_for('admin.edit_match', match_id=match_id))

    # Guardar nombre del partido para el mensaje
    match_name = f"{match.home_team} vs {match.away_team}"
    
    # Borrar el resultado
    match.home_goals = None
    match.away_goals = None
    db.session.commit()

    # Resetear los puntos de todas las predicciones de este partido
    predictions = Prediction.query.filter_by(match_id=match_id).all()
    for prediction in predictions:
        prediction.points_awarded = prediction.calculate_points()  # Devuelve 0 si no hay resultado
    
    db.session.commit()

    flash(f'Resultado de "{match_name}" borrado. Puntos recalculados a 0.', 'success')
    return redirect(url_for('admin.edit_match', match_id=match_id))

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
        
        # Actualizar is_admin e is_enabled
        user.is_admin = request.form.get('is_admin') == 'true'
        user.is_enabled = request.form.get('is_enabled') == 'true'
        
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

@admin_bp.route('/allowed-emails', methods=['GET', 'POST'])
@login_required
@admin_required
def allowed_emails():
    """Gestionar emails habilitados (sin registrar aún)"""
    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        if not email:
            flash('El email es requerido', 'error')
            return redirect(url_for('admin.allowed_emails'))

        existing = AllowedEmail.query.filter_by(email=email).first()
        if existing:
            flash('Ese email ya está habilitado', 'warning')
            return redirect(url_for('admin.allowed_emails'))

        db.session.add(AllowedEmail(email=email))
        db.session.commit()
        flash('Email habilitado', 'success')
        return redirect(url_for('admin.allowed_emails'))

    # Obtener emails habilitados que NO tienen usuario registrado
    allowed = db.session.query(AllowedEmail).outerjoin(
        User, AllowedEmail.email == User.email
    ).filter(User.id == None).all()
    
    return render_template('admin/allowed_emails.html', emails=allowed)

@admin_bp.route('/allowed-emails/<int:email_id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_allowed_email(email_id):
    """Eliminar email habilitado"""
    item = AllowedEmail.query.get_or_404(email_id)
    db.session.delete(item)
    db.session.commit()
    flash('Email eliminado', 'success')
    return redirect(url_for('admin.allowed_emails'))


@admin_bp.route('/agregar-fase4')
@login_required
@admin_required
def agregar_fase4():
    """Página de confirmación para agregar los 32 partidos de Fase 4"""
    return render_template('admin/agregar_fase4.html')


@admin_bp.route('/agregar-fase4/ejecutar')
@login_required
@admin_required
def ejecutar_agregar_fase4():
    """Ejecuta la acción de agregar los 32 partidos de Fase 4 en producción"""
    from models import Phase
    from datetime import timedelta
    
    # Partidos de Fase 4
    PARTIDOS_FASE4 = [
        ("1A", "2B", "2026-06-29 19:00"), ("1C", "2D", "2026-06-29 22:00"),
        ("1E", "2F", "2026-06-30 19:00"), ("1G", "2H", "2026-06-30 22:00"),
        ("1B", "2A", "2026-07-01 19:00"), ("1D", "2C", "2026-07-01 22:00"),
        ("1F", "2E", "2026-07-02 19:00"), ("1H", "2G", "2026-07-02 22:00"),
        ("1I", "2J", "2026-07-03 19:00"), ("1K", "2L", "2026-07-03 22:00"),
        ("1J", "2I", "2026-07-04 19:00"), ("1L", "2K", "2026-07-04 22:00"),
        ("1A", "3C/D/E", "2026-07-05 19:00"), ("1B", "3A/C/D", "2026-07-05 22:00"),
        ("1C", "3A/B/E", "2026-07-06 19:00"), ("1D", "3A/B/C", "2026-07-06 22:00"),
        ("W1", "W2", "2026-07-09 19:00"), ("W3", "W4", "2026-07-09 22:00"),
        ("W5", "W6", "2026-07-10 19:00"), ("W7", "W8", "2026-07-10 22:00"),
        ("W9", "W10", "2026-07-11 19:00"), ("W11", "W12", "2026-07-11 22:00"),
        ("W13", "W14", "2026-07-12 19:00"), ("W15", "W16", "2026-07-12 22:00"),
        ("W17", "W18", "2026-07-14 22:00"), ("W19", "W20", "2026-07-15 22:00"),
        ("W21", "W22", "2026-07-16 22:00"), ("W23", "W24", "2026-07-17 22:00"),
        ("L25", "L26", "2026-07-18 19:00"), ("W25", "W26", "2026-07-18 22:00"),
        ("L27", "L28", "2026-07-19 19:00"), ("W27", "W28", "2026-07-19 22:00"),
    ]
    
    try:
        fase4 = Phase.query.filter_by(name='Fecha 4 - Eliminación Directa').first()
        if not fase4:
            flash('❌ ERROR: No se encontró la Fase 4 en la base de datos', 'error')
            return redirect(url_for('admin.dashboard'))
        
        total_antes = Match.query.count()
        partidos_agregados = 0
        
        for home, away, kickoff_str in PARTIDOS_FASE4:
            existing = Match.query.filter_by(home_team=home, away_team=away, phase_id=fase4.id).first()
            if existing:
                continue
            
            kickoff = datetime.strptime(kickoff_str, "%Y-%m-%d %H:%M").replace(tzinfo=timezone.utc)
            closes = kickoff - timedelta(minutes=10)
            
            match = Match(home_team=home, away_team=away, kickoff_at=kickoff, closes_at=closes, phase_id=fase4.id)
            db.session.add(match)
            partidos_agregados += 1
        
        db.session.commit()
        total_despues = Match.query.count()
        
        flash(f'✅ {partidos_agregados} partidos de Fase 4 agregados! Total: {total_antes} → {total_despues}', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'❌ Error: {str(e)}', 'error')
    
    return redirect(url_for('admin.dashboard'))
