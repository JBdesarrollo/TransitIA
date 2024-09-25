import chromadb
import dotenv
import os
from llama_index.core import VectorStoreIndex
from llama_index.core.chat_engine import SimpleChatEngine
from llama_index.llms.gemini import Gemini
from llama_index.vector_stores.chroma import ChromaVectorStore
import streamlit as st


# Cargar las variables de entorno desde el archivo .env
dotenv.load_dotenv()

class PotterClass:
    def __init__(self):
        # Obtener la clave API de Gemini del archivo .env
        gemini_api_key = os.getenv("GEMINI")

        # Crear una instancia del modelo Gemini usando la clave API
        self.llm = Gemini(model_name="models/gemini-pro", api_key=gemini_api_key)
        self.index = self.cargar_indice()

        # Si no existe en session_state, crear el chat engine
        if "chat_engine" not in st.session_state:
            st.session_state.chat_engine = self.index.as_chat_engine(
                chat_mode='react',
                similarity_top_k=5,
                system_prompt=(
                    "Eres un abogado experto en el código de tránsito de Colombia. Respondes formal y educadamente a preguntas      relacionadas con temas de transito de Colombia basándote sólo en la información suministrada y no contestas temas que no estén relacionados"
                )
            )

    def cargar_indice(self):
        # Cargar la base de datos ChromaDB
        db2 = chromadb.PersistentClient(path="./crhoma_db")
        chroma_collection = db2.get_collection("transito")
        vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
        index = VectorStoreIndex.from_vector_store(
            vector_store,
            embed_model=self.llm
        )
        return index

    def chat(self, consulta):
        # Realizar una consulta al chatbot usando el chat_engine del estado
        respuesta = st.session_state.chat_engine.chat(consulta)
        return respuesta
