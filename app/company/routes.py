from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required
from app.extensions import db
from app.models import Empresa

# Definimos el Blueprint
bp = Blueprint("company", __name__, url_prefix="/empresas")

# 1. RUTA VISTA: Solo renderiza el HTML vacío (Vue lo llenará)
@bp.route("/", methods=["GET"])
@login_required
def lista_empresas():
    return render_template("company/lista.html")

# 2. ENDPOINT API: Devuelve los datos en JSON
@bp.route("/json", methods=["GET"])
@login_required
def empresas_json():
    empresas = Empresa.query.order_by(Empresa.id.desc()).all()
    data = []
    for e in empresas:
        data.append({
            "id": e.id,
            "nombre": e.nombre,
            "ruc": e.ruc,
            "sector": e.sector
        })
    return jsonify(data)

# 3. ENDPOINT: Crear
@bp.route("/nuevo", methods=["POST"])
@login_required
def nueva_empresa():
    nombre = request.form.get("nombre", "").strip()
    ruc = request.form.get("ruc", "").strip()
    sector = request.form.get("sector", "").strip()

    if not nombre:
        flash("El nombre de la empresa es obligatorio.", "danger")
        return redirect(url_for("company.lista_empresas"))

    nueva = Empresa(nombre=nombre, ruc=ruc, sector=sector)
    db.session.add(nueva)
    db.session.commit()
    
    flash("Empresa creada correctamente.", "success")
    return redirect(url_for("company.lista_empresas"))

# 4. ENDPOINT: Editar
@bp.route("/<int:id>/editar", methods=["POST"])
@login_required
def editar_empresa(id):
    empresa = Empresa.query.get_or_404(id)
    
    empresa.nombre = request.form.get("nombre", "").strip()
    empresa.ruc = request.form.get("ruc", "").strip()
    empresa.sector = request.form.get("sector", "").strip()
    
    db.session.commit()
    flash("Empresa actualizada correctamente.", "success")
    return redirect(url_for("company.lista_empresas"))

# 5. ENDPOINT: Eliminar
@bp.route("/<int:id>/eliminar", methods=["POST"])
@login_required
def eliminar_empresa(id):
    empresa = Empresa.query.get_or_404(id)
    
    # Opcional: Verificar si tiene modelos asociados antes de borrar
    # if empresa.modelos: ...
    
    db.session.delete(empresa)
    db.session.commit()
    flash("Empresa eliminada correctamente.", "success")
    return redirect(url_for("company.lista_empresas"))