# app/bayes/engine.py
from pgmpy.models import BayesianModel
from pgmpy.inference import VariableElimination

def build_bn_from_json(estructura_json, cpts_json):
    """
    estructura_json: {"edges": [["CorteElectrico","Energia"], ["Energia","Servidor"], ...]}
    cpts_json: {"Servidor": {...}, "Disponibilidad": {...}, ...}
    """
    edges = estructura_json["edges"]
    model = BayesianModel(edges)

    # Aquí construyes las CPDs a partir de cpts_json (tablas CPT)
    from pgmpy.factors.discrete import TabularCPD
    for node, cpt_data in cpts_json.items():
        cpd = TabularCPD(
            variable=node,
            variable_card=len(cpt_data["states"]),
            values=cpt_data["values"],
            evidence=cpt_data.get("evidence"),
            evidence_card=cpt_data.get("evidence_card")
        )
        model.add_cpds(cpd)

    model.check_model()
    return model


def inferir_riesgo(estructura_json, cpts_json, evidencia):
    """
    evidencia: dict, ej. {"CorteElectrico": "SI", "FallaHardware": "NO"}
    """
    model = build_bn_from_json(estructura_json, cpts_json)
    infer = VariableElimination(model)

    # nodo objetivo, por ejemplo: "RiesgoDisponibilidad"
    target = "RiesgoDisponibilidad"
    posterior = infer.query(variables=[target], evidence=evidencia)

    distrib = posterior[target].values.tolist()
    estados = model.get_cpds(target).state_names[target]

    resultado = {estado: float(prob) for estado, prob in zip(estados, distrib)}

    # Clasificación bajo/medio/alto según rangos
    max_estado = max(resultado, key=resultado.get)
    return resultado, max_estado