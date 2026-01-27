import streamlit as st
import time

# Configuração da Página
st.set_page_config(page_title="Sleep Health AI", page_icon="😴")

# Título e Descrição
st.title("Triagem de Distúrbios do Sono 🩺")
st.write("Preencha os dados biométricos do paciente para análise de risco.")

# Formulário (Inputs)
with st.form("ficha_paciente"):
    st.subheader("Dados Clínicos")
    
    col1, col2 = st.columns(2)
    
    with col1:
        idade = st.number_input("Idade", min_value=18, max_value=100, value=30)
        genero = st.selectbox("Gênero", ["Masculino", "Feminino"])
        pressao = st.text_input("Pressão Arterial (ex: 120/80)", "120/80")
        
    with col2:
        duracao_sono = st.slider("Duração do Sono (horas/dia)", 0.0, 12.0, 7.0, step=0.1)
        nivel_stress = st.slider("Nível de Estresse (1-10)", 1, 10, 5)
        bmi = st.selectbox("Categoria de IMC", ["Normal", "Sobrepeso", "Obeso"])

    st.subheader("Estilo de Vida")
    passos_diarios = st.number_input("Passos Diários", min_value=0, value=5000)
    
    # Botão de Envio
    submitted = st.form_submit_button("Calcular Risco")

# Ação do Botão (Simulação)
if submitted:
    with st.spinner('Processando dados com IA...'):
        time.sleep(2) # Fingindo que está pensando
        
        # AQUI É ONDE VAMOS CONECTAR O MODELO DEPOIS
        # Por enquanto, é uma lógica "fake" só pra testar o visual
        st.success("Análise Concluída!")
        
        if duracao_sono < 5 or nivel_stress > 7:
            st.error("🚨 Resultado: Risco de INSÔNIA detectado.")
            st.write("**Recomendação:** Encaminhar para especialista do sono.")
        elif bmi == "Obeso":
            st.warning("⚠️ Resultado: Risco de APNEIA DO SONO detectado.")
        else:
            st.balloons()
            st.info("✅ Resultado: Paciente SAUDÁVEL.")