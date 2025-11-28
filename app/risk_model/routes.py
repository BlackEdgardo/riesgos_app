from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user # Importar current_user
from app.extensions import db
from app.models import ModeloBN, Empresa, User # Importar Empresa y User
from datetime import datetime

bp = Blueprint("risk_model", __name__, url_prefix="/modelos-bn")

@bp.route("/", methods=["GET"])
@login_required
def lista_modelos():
    return render_template("modelos/lista.html")

# --- NUEVA RUTA: Para llenar el dropdown de empresas en Vue ---
@bp.route("/empresas/json", methods=["GET"])
@login_required
def empresas_json():
    empresas = Empresa.query.order_by(Empresa.nombre.asc()).all()
    data = [{"id": e.id, "nombre": e.nombre} for e in empresas]
    return jsonify(data)

@bp.route("/json", methods=["GET"])
@login_required
def modelos_json():
    # Hacemos join para obtener nombres en lugar de solo IDs
    modelos = ModeloBN.query.order_by(ModeloBN.id.asc()).all()
    
    data = []
    for m in modelos:
        # Obtenemos nombre de empresa y creador de forma segura
        empresa_nombre = Empresa.query.get(m.empresa_id).nombre if m.empresa_id else "Sin asignar"
        creador_email = User.query.get(m.creado_por).email if m.creado_por else "Desconocido"

        data.append({
            "id": m.id,
            "nombre": m.nombre,
            "descripcion": m.descripcion,
            "empresa_id": m.empresa_id,
            "empresa_nombre": empresa_nombre, # Nuevo campo para mostrar
            "creado_por_id": m.creado_por,
            "creado_por_email": creador_email, # Nuevo campo para mostrar
            "estructura_json": m.estructura_json,
            "cpts_json": m.cpts_json,
            "created_at": m.created_at.isoformat() if m.created_at else None,
        })

    return jsonify(data)

@bp.route("/nuevo", methods=["POST"])
@login_required
def nuevo_modelo():
    nombre = request.form.get("nombre", "").strip()
    descripcion = request.form.get("descripcion", "").strip()
    empresa_id = request.form.get("empresa_id") # Capturar empresa

    if not nombre:
        flash("El nombre del modelo es obligatorio", "danger")
        return redirect(url_for("risk_model.lista_modelos"))

    # Estructuras vacías por defecto
    dummy_estructura = {"nodes": [], "edges": []}
    dummy_cpts = {}

    modelo = ModeloBN(
        nombre=nombre,
        descripcion=descripcion or None,
        empresa_id=empresa_id if empresa_id else None,
        estructura_json=dummy_estructura,
        cpts_json=dummy_cpts,
        creado_por=current_user.id, # Asignar usuario actual
        created_at=datetime.utcnow(),
    )
    db.session.add(modelo)
    db.session.commit()
    flash("Modelo creado correctamente", "success")
    return redirect(url_for("risk_model.lista_modelos"))

@bp.route("/<int:modelo_id>/editar", methods=["POST"])
@login_required
def editar_modelo(modelo_id):
    modelo = ModeloBN.query.get_or_404(modelo_id)
    
    modelo.nombre = request.form.get("nombre", "").strip()
    modelo.descripcion = request.form.get("descripcion", "").strip() or None
    
    empresa_id = request.form.get("empresa_id")
    modelo.empresa_id = empresa_id if empresa_id else None
    
    db.session.commit()
    flash("Modelo actualizado correctamente", "success")
    return redirect(url_for("risk_model.lista_modelos"))

# ... (El resto de rutas eliminar/detalle se mantienen igual) ...
@bp.route("/<int:modelo_id>/eliminar", methods=["POST"])
@login_required
def eliminar_modelo(modelo_id):
    modelo = ModeloBN.query.get_or_404(modelo_id)
    db.session.delete(modelo)
    db.session.commit()
    flash("Modelo eliminado correctamente", "success")
    return redirect(url_for("risk_model.lista_modelos"))

@bp.route("/<int:modelo_id>", methods=["GET"])
@login_required
def detalle_modelo(modelo_id):
    modelo = ModeloBN.query.get_or_404(modelo_id)
    return render_template("modelos/detalle.html", modelo=modelo)