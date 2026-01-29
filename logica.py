import joblib
import pandas as pd

# Carregamento dos modelos
try:
    modelo = joblib.load('./models/modelo_sono_rf.pkl')
    metricas = joblib.load('./models/metricas_normalizacao.pkl')
except Exception as e:
    print(f"Erro ao carregar modelos: {e}")
    modelo, metricas = None, None

def processar_pressao(texto_pressao):
    try:
        sistole, diastole = texto_pressao.split('/')
        return int(sistole), int(diastole)
    except:
        return 120, 80

def preparar_dados_para_modelo(dados_front):
    # Mapeamentos (Texto -> Numérico/Coluna)
    mapa_bmi = {"Normal": 1, "Sobrepeso": 2, "Obeso": 3}
    mapa_profissoes = {
        "Enfermeiro(a)": "Occ_Nurse",
        "Médico(a)": "Occ_Doctor",
        "Engenheiro(a)": "Occ_Engineer",
        "Advogado(a)": "Occ_Lawyer",
        "Professor(a)": "Occ_Teacher",
        "Contador(a)": "Occ_Accountant",
        "Vendedor(a)": "Occ_Salesperson"
    }
    
    # Dados base numéricos
    dados_modelo = {
        'Age': dados_front['idade'],
        'BMI Category': mapa_bmi.get(dados_front['bmi'], 1),
        'Systolic': dados_front['sistole'],
        'Diastolic': dados_front['diastole'],
        'Stress Level': dados_front['stress'],
        'Sleep Duration': dados_front['sono_duracao'],
        'Heart Rate': dados_front['freq_cardiaca'],
        'Physical Activity Level': dados_front['ativ_fisica'],
        'Quality of Sleep': dados_front['qualidade_sono'],
        'Gender_Male': 1 if dados_front['genero'] == 'Homem' else 0,
        'Gender_Female': 1 if dados_front['genero'] == 'Mulher' else 0
    }

    # One-Hot Encoding manual da profissão
    prof_key = mapa_profissoes.get(dados_front['ocupacao'])
    if prof_key:
        dados_modelo[prof_key] = 1
        
    return dados_modelo

def classificar_risco(dados_paciente):
    if modelo is None:
        return {"Erro": 0.0, "Modelo não carregado": 0.0}

    # 1. Preparar e criar DataFrame
    dados_prontos = preparar_dados_para_modelo(dados_paciente)
    df = pd.DataFrame([dados_prontos])
    
    # 2. Normalização
    try:
        for col in metricas['numeric_cols']:
            if col in df.columns:
                df[col] = (df[col] - metricas['norm'][col]['mean']) / metricas['norm'][col]['std']
    except Exception as e:
        print(f"Aviso na normalização: {e}")

    # 3. Reindexar e Predizer
    df = df.reindex(columns=metricas['columns_order'], fill_value=0)
    probs = modelo.predict_proba(df)[0]
    
    # 4. Formatar Saída
    classes = {0: "Saudável (Sem Distúrbio)", 1: "Apneia do Sono", 2: "Insônia"}
    resultado_bruto = {classes[i]: prob for i, prob in enumerate(probs)}
    
    return dict(sorted(resultado_bruto.items(), key=lambda item: item[1], reverse=True))
