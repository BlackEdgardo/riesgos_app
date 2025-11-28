from datetime import datetime
from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from app.extensions import db
from app.models import ModeloBN, Evidencia, ResultadoInferencia
# Ya no necesitamos importar json para conversiones, SQLAlchemy lo hace solo.

bp = Blueprint("inference", __name__, url_prefix="/inferencia")

# --- FUNCIÓN MOCKUP DEL MOTOR BAYESIANO ---
def motor_inferencia_simulado(evidencia_dict):
    """
    Simula el cálculo. Retorna un DICCIONARIO PURO.
    """
    riesgo_alto = 0.1
    # Lógica simple para la demo
    for k, v in evidencia_dict.items():
        if v and ("Fallo" in v or "Caido" in v or "Inestable" in v):
            riesgo_alto += 0.3
    
    riesgo_alto = min(riesgo_alto, 0.99)
    riesgo_bajo = 1.0 - riesgo_alto
    
    clasificacion = "bajo"
    if riesgo_alto > 0.33: clasificacion = "medio"
    if riesgo_alto > 0.66: clasificacion = "alto"

    # Retornamos dict, NO string
    return {
        "detalles": {
            "Disponibilidad": {
                "Baja": round(riesgo_alto, 2),
                "Media": 0.05, 
                "Alta": round(riesgo_bajo - 0.05, 2)
            }
        },
        "clasificacion": clasificacion,
        "probabilidad_riesgo": round(riesgo_alto, 2)
    }

@bp.route("/", methods=["GET"])
@login_required
def index():
    modelos = ModeloBN.query.order_by(ModeloBN.id.asc()).all()
    return render_template("inference/index.html", modelos=modelos)

@bp.route("/<int:modelo_id>", methods=["GET", "POST"])
@login_required
def ejecutar_inferencia(modelo_id):
    modelo = ModeloBN.query.get_or_404(modelo_id)

    # 1. PREPARAR INPUT
    # CORRECCIÓN: Al ser db.JSON, esto YA ES un diccionario. No usar json.loads()
    nodos_para_input = modelo.cpts_json if modelo.cpts_json else {}

    resultado_db = None
    resultado_detalles = None

    if request.method == "POST":
        # 2. CAPTURAR EVIDENCIA
        evidencia_capturada = {}
        for key, value in request.form.items():
            # Filtramos tokens y vacíos
            if key != "csrf_token" and value and value.strip() != "":
                evidencia_capturada[key] = value
        
        if not evidencia_capturada:
            flash("Debes seleccionar al menos una evidencia.", "warning")
        else:
            try:
                # 3. GUARDAR EVIDENCIA
                # CORRECCIÓN: Pasamos el diccionario directo. SQLAlchemy lo serializa solo.
                nueva_evidencia = Evidencia(
                    modelo_id=modelo.id,
                    usuario_id=current_user.id,
                    evidencia_json=evidencia_capturada, 
                    created_at=datetime.now()
                )
                db.session.add(nueva_evidencia)
                db.session.flush()

                # 4. MOTOR
                calculo = motor_inferencia_simulado(evidencia_capturada)

                # 5. GUARDAR RESULTADO
                # CORRECCIÓN: Pasamos el diccionario directo.
                nuevo_resultado = ResultadoInferencia(
                    modelo_id=modelo.id,
                    evidencia_id=nueva_evidencia.id,
                    resultado_json=calculo["detalles"],
                    riesgo_clasificado=calculo["clasificacion"],
                    created_at=datetime.now()
                )
                db.session.add(nuevo_resultado)
                db.session.commit()
                
                resultado_db = nuevo_resultado
                # Al leerlo de vuelta, SQLAlchemy lo convierte a dict automáticamente
                resultado_detalles = nuevo_resultado.resultado_json 
                
                flash("Inferencia completada exitosamente.", "success")

            except Exception as e:
                db.session.rollback()
                flash(f"Error interno: {str(e)}", "danger")
                print(f"DEBUG ERROR: {e}")

    return render_template(
        "inference/ejecutar.html",
        modelo=modelo,
        nodos_para_input=nodos_para_input,
        resultado=resultado_db,
        resultado_detalles=resultado_detalles
    )