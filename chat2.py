import streamlit as st
from PotterClass import PotterClass  # Asegúrate de que el archivo esté en el mismo directorio o bien importado correctamente

# Instanciar el chatbot de Potter
chatbot = PotterClass()

# Configura el título de la página
st.set_page_config(
    page_title="TransitIA"
)

# Si no existe en el estado, inicializamos una lista para almacenar la conversación
if "conversation" not in st.session_state:
    st.session_state.conversation = []

# Función para manejar la conversación
def send_message():
    # El mensaje enviado por el usuario
    user_message = st.session_state.user_input
    if user_message:
        # Agregar el mensaje del usuario a la conversación
        st.session_state.conversation.append(f"Usuario: {user_message}")

        # Obtener la respuesta del bot desde el chatbot de Potter
        bot_response = chatbot.chat(user_message)
        st.session_state.conversation.append(f"IA: {bot_response}")

        # Limpiar la caja de texto
        st.session_state.user_input = ""

# Mostrar la conversación
st.write("### Conversación:")
for message in st.session_state.conversation:
    st.write(message)

# Caja de texto para ingresar el mensaje
st.text_input("Escribe tu mensaje:", key="user_input", on_change=send_message)
