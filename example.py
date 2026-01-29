import joblib
import pandas as pd

# 1. Carregar os artefatos
modelo = joblib.load('./models/modelo_sono_rf.pkl')
m = joblib.load('./models/metricas_normalizacao.pkl')

def sistema_triagem_sono(dados_brutos):
    # Criar DataFrame e Normalizar
    df = pd.DataFrame([dados_brutos])
    for col in m['numeric_cols']:
        df[col] = (df[col] - m['norm'][col]['mean']) / m['norm'][col]['std']
    
    # Organizar colunas na ordem que o modelo aprendeu
    df = df.reindex(columns=m['columns_order'], fill_value=0)
    print(df.columns.tolist())
    # Obter probabilidades (o Softmax ou Random Forest fazem isso)
    probs = modelo.predict_proba(df)[0]
    
    # Mapeamento de nomes para exibição
    classes = {0: "Saudável (Sem Distúrbio)", 1: "Apneia do Sono", 2: "Insônia"}
    
    # Criar um ranking organizado
    ranking = sorted(
        [(classes[i], prob * 100) for i, prob in enumerate(probs)],
        key=lambda x: x[1],
        reverse=True
    )
    
    print("=== RELATÓRIO DE TRIAGEM IA ===")
    for doenca, porcentagem in ranking:
        print(f"{doenca}: {porcentagem:.2f}%")
    
    print("\nNota: Este resultado é uma análise estatística de triagem e não substitui consulta médica.")

# --- Simulação de uso no seu PoC ---
paciente_teste = {
    'Age': 33,
    'BMI Category': 1,
    'Gender_Female': 1,
    'Systolic': 128,
    'Diastolic': 85,
    'Stress Level': 6,
    'Sleep Duration': 6.2,
    'Heart Rate': 76,
    'Physical Activity Level': 50,
    'Occ_Other': 1
}

sistema_triagem_sono(paciente_teste)