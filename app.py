import streamlit as st
import time

st.set_page_config(page_title="Sleep Health AI", page_icon="😴", layout="centered")

lista_profissoes_raw = [
    "Médico(a)", 
    "Professor(a)", 
    "Enfermeiro(a)", 
    "Engenheiro(a)", 
    "Contador(a)", 
    "Advogado(a)", 
    "Vendedor(a)"
]
profissoes_finais = sorted(lista_profissoes_raw) + ["Outro"]

lista_genero = ["Homem", "Mulher"]
lista_bmi = ["Normal", "Sobrepeso", "Obeso"]

st.title("Triagem de Distúrbios do Sono 🩺")
st.markdown("### PoC - Análise Probabilística")
st.write("Preencha os dados biométricos para calcular as probabilidades dos distúrbios.")

with st.form("ficha_paciente"):
    st.subheader("1. Perfil e Dados Clínicos")
    
    col1, col2 = st.columns(2)
    
    with col1:
        genero = st.selectbox("Gênero", lista_genero)
        idade = st.number_input("Idade", min_value=1, max_value=150, value=30)
        ocupacao = st.selectbox("Profissão", profissoes_finais)
        pressao = st.text_input("Pressão Arterial (ex: 120/80)", "120/80")
        
    with col2:
        bmi = st.selectbox("Categoria de IMC", lista_bmi)
        ativ_fisica = st.number_input("Atividade Física (min/dia)", min_value=0, max_value=300, value=45, step=5)
        freq_cardiaca = st.number_input("Frequência Cardíaca (bpm)", min_value=40, max_value=200, value=72)

    st.markdown("---")
    st.subheader("2. Indicadores de Sono e Estresse")
    
    col3, col4 = st.columns(2)
    with col3:
        duracao_sono = st.slider("Duração do Sono (horas/dia)", 4.0, 10.0, 7.0, step=0.1)
    with col4:
        nivel_stress = st.slider("Nível de Estresse (3 a 8)", 3, 8, 5)

    submitted = st.form_submit_button("Calcular Probabilidades", use_container_width=True)

if submitted:
    with st.spinner('Processando dados com IA...'):
        time.sleep(1.5) 
        
        if nivel_stress > 6 or duracao_sono < 5.5:
             probs = {"Sem distúrbio": 0.20, "Insônia": 0.65, "Apneia do sono": 0.15}
        elif bmi == "Obeso":
             probs = {"Sem distúrbio": 0.30, "Insônia": 0.20, "Apneia do sono": 0.50}
        else:
             probs = {"Sem distúrbio": 0.85, "Insônia": 0.10, "Apneia do sono": 0.05}

        probs_ordenadas = dict(sorted(probs.items(), key=lambda item: item[1], reverse=True))

        st.markdown("### 📊 Resultado da Análise")
        
        for diagnostico, probabilidade in probs_ordenadas.items():
            percentual = int(probabilidade * 100)
            
            if diagnostico == "Sem distúrbio":
                st.success(f"**{diagnostico}**: {percentual}%")
                st.progress(percentual)
            else:
                if percentual > 50:
                    st.error(f"**{diagnostico}**: {percentual}% (Alerta Crítico)")
                else:
                    st.warning(f"**{diagnostico}**: {percentual}%")
                st.progress(percentual)

        try:
            sistole, diastole = pressao.split('/')
        except:
            sistole, diastole = 0, 0

        with st.expander("Ver dados técnicos enviados ao modelo"):
            st.json({
                "Gender": genero,
                "Age": idade,
                "Occupation": ocupacao,
                "Sleep Duration": duracao_sono,
                "Quality of Sleep": "?", 
                "Physical Activity Level": ativ_fisica,
                "Stress Level": nivel_stress,
                "BMI Category": bmi,
                "Heart Rate": freq_cardiaca,
                "Blood Pressure (Sys)": sistole,
                "Blood Pressure (Dia)": diastole
            })