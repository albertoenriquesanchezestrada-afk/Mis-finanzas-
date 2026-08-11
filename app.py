import datetime
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Control de Finanzas", page_icon="💰", layout="centered"
)

st.title("💰 Control de Finanzas")
st.write("¡Hola! Tu aplicación está funcionando correctamente.")

# Formulario simple de prueba
with st.form("registro_form"):
    tipo = st.selectbox("Tipo", ["Gasto", "Ingreso"])
    monto = st.number_input("Monto ($)", min_value=0.0)
    categoria = st.text_input("Categoría")
    submit = st.form_submit_button("Guardar")

    if submit:
        st.success(f"Registrado: {tipo} de ${monto} en {categoria}")
