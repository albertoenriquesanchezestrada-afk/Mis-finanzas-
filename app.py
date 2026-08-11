import datetime
import os
import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

# Configuración de página
st.set_page_config(
    page_title="Control de Finanzas", page_icon="💰", layout="centered"
)

ARCHIVO_DATOS = "finanzas.csv"


# Cargar datos desde CSV local
def cargar_datos():
    if os.path.exists(ARCHIVO_DATOS):
        try:
            return pd.read_csv(ARCHIVO_DATOS)
        except Exception:
            pass
    return pd.DataFrame(
        columns=["Fecha", "Tipo", "Categoría", "Monto", "Descripción"]
    )


df = cargar_datos()

st.title("💰 Control de Finanzas")

# --- REGISTRO DE TRANSACCIONES ---
st.header("📝 Registrar Transacción")

with st.form("registro_form", clear_on_submit=True):
    col_tipo, col_monto = st.columns(2)
    with col_tipo:
        tipo = st.selectbox("Tipo", ["Gasto", "Ingreso"])
    with col_monto:
        monto = st.number_input("Monto ($)", min_value=0.0, step=10.0)

    categoria = st.text_input(
        "Categoría", placeholder="Ej. Comida, Escuela, Transporte"
    ).strip()
    descripcion = st.text_input(
        "Descripción", placeholder="Ej. Almuerzo o colegiatura"
    ).strip()

    submit = st.form_submit_button("Guardar Registro")

    if submit:
        if monto > 0 and categoria:
            nueva_fila = pd.DataFrame(
                [
                    {
                        "Fecha": datetime.date.today().strftime("%Y-%m-%d"),
                        "Tipo": tipo.lower(),
                        "Categoría": categoria.capitalize(),
                        "Monto": monto,
                        "Descripción": descripcion,
                    }
                ]
            )

            df = pd.concat([df, nueva_fila], ignore_index=True)
            df.to_csv(ARCHIVO_DATOS, index=False)

            st.success(f"✅ {tipo} de ${monto:,.2f} guardado correctamente.")
            st.rerun()
        else:
            st.error("❌ Ingresa un monto mayor a 0 y una categoría.")

st.divider()

# --- RESUMEN Y GRÁFICOS ---
st.header("📊 Resumen Financiero")

if not df.empty and "Tipo" in df.columns and "Monto" in df.columns:
    df["Monto"] = pd.to_numeric(df["Monto"], errors="coerce").fillna(0)

    ingresos = df[df["Tipo"] == "ingreso"]["Monto"].sum()
    gastos = df[df["Tipo"] == "gasto"]["Monto"].sum()
    balance = ingresos - gastos

    col1, col2, col3 = st.columns(3)
    col1.metric("Ingresos", f"${ingresos:,.2f}")
    col2.metric("Gastos", f"${gastos:,.2f}")
    col3.metric("Saldo", f"${balance:,.2f}")

    # Gráfico de pastel para gastos
    df_gastos = df[df["Tipo"] == "gasto"]
    if not df_gastos.empty:
        st.subheader("Gastos por Categoría")
        gastos_cat = df_gastos.groupby("Categoría")["Monto"].sum()

        fig, ax = plt.subplots(figsize=(6, 4))
        ax.pie(
            gastos_cat,
            labels=gastos_cat.index,
            autopct="%1.1f%%",
            startangle=90,
        )
        ax.axis("equal")
        st.pyplot(fig)

    st.subheader("📋 Historial de Transacciones")
    st.dataframe(df, use_container_width=True)
else:
    st.info("Aún no tienes registros guardados.")



