# app/dashboard/routes.py
from flask import Blueprint, render_template, jsonify
from flask_login import login_required
from app.models import ResultadoInferencia
from flask import jsonify

bp = Blueprint("dashboard", __name__)

# --- FUNCIÓN 1: TAREA DE VISTA (Solo carga el HTML y datos estáticos) ---
@bp.route("/")
@login_required
def index():
    # Solo pasamos datos que NO requieren conversión a JSON (como la lista para la tabla HTML)
    recientes = ResultadoInferencia.query.order_by(ResultadoInferencia.created_at.desc()).limit(5).all()
    total = ResultadoInferencia.query.count()
    
    # Renderizamos la vista sin tocar JSON
    return render_template("dashboard/index.html", recientes=recientes, total=total)


# --- FUNCIÓN 2: TAREA DE DATOS (Solo devuelve JSON para el gráfico) ---

@bp.route("/api/datos-grafico")
@login_required
def datos_grafico():
    altos = ResultadoInferencia.query.filter_by(riesgo_clasificado='alto').count()
    medios = ResultadoInferencia.query.filter_by(riesgo_clasificado='medio').count()
    bajos = ResultadoInferencia.query.filter_by(riesgo_clasificado='bajo').count()
    
    return jsonify({
        "labels": ["Alto", "Medio", "Bajo"],
        "data": [altos, medios, bajos]
    })