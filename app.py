from __future__ import annotations

from pathlib import Path
from typing import Any

import joblib
import streamlit as st


BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR / "pipeline_itsm.joblib"


st.set_page_config(
    page_title="Triagem Automatica de Chamados",
    page_icon="🎫",
    layout="centered",
)


@st.cache_resource(show_spinner=False)
def load_model() -> Any:
    if not MODEL_PATH.exists():
        return None
    return joblib.load(MODEL_PATH)


def mock_inference(text: str) -> dict[str, str]:
    normalized = text.lower()

    if any(term in normalized for term in ("senha", "login", "acesso", "permiss")):
        return {"categoria": "Acessos/Sistemas", "prioridade": "Media"}
    if any(term in normalized for term in ("rede", "internet", "vpn", "wi-fi", "wifi")):
        return {"categoria": "Infraestrutura/Redes", "prioridade": "Alta"}
    if any(term in normalized for term in ("impressora", "mouse", "teclado", "tela azul", "nao liga")):
        return {"categoria": "Hardware/Equipamentos", "prioridade": "Media"}

    return {"categoria": "Geral", "prioridade": "Baixa"}


def normalize_prediction(raw: Any) -> dict[str, str]:
    if isinstance(raw, dict):
        category = raw.get("categoria") or raw.get("category") or raw.get("classe") or raw.get("label")
        priority = raw.get("prioridade") or raw.get("priority") or raw.get("sla")
        return {
            "categoria": str(category or "Nao informado"),
            "prioridade": str(priority or "Nao informado"),
        }

    if isinstance(raw, (list, tuple)) and len(raw) >= 2:
        return {"categoria": str(raw[0]), "prioridade": str(raw[1])}

    if hasattr(raw, "tolist"):
        values = raw.tolist()
        if isinstance(values, list) and values:
            first = values[0]
            if isinstance(first, (list, tuple)) and len(first) >= 2:
                return {"categoria": str(first[0]), "prioridade": str(first[1])}
            if len(values) >= 2 and not isinstance(first, (list, tuple)):
                return {"categoria": str(values[0]), "prioridade": str(values[1])}

    text = str(raw)
    separators = ["|", ";", "/", " - ", ","]
    for sep in separators:
        if sep in text:
            parts = [part.strip() for part in text.split(sep) if part.strip()]
            if len(parts) >= 2:
                return {"categoria": parts[0], "prioridade": parts[1]}

    return {"categoria": text, "prioridade": "Nao informado"}


def predict_ticket(text: str) -> dict[str, str]:
    model = load_model()
    if model is None:
        return mock_inference(text)

    prediction = model.predict([text])
    first = prediction[0] if hasattr(prediction, "__len__") and len(prediction) else prediction
    return normalize_prediction(first)


if "ticket_text" not in st.session_state:
    st.session_state.ticket_text = ""

if "result" not in st.session_state:
    st.session_state.result = None

st.title("Triagem automatica de chamados")
st.caption("Digite palavras-chave curtas do erro ou incidente para obter categoria e prioridade.")

if not MODEL_PATH.exists():
    st.info("pipeline_itsm.joblib nao encontrado no diretorio raiz. O app vai usar um mock local apenas para demonstracao.")

with st.form("ticket_form", clear_on_submit=False):
    ticket_text = st.text_area(
        "Descricao do chamado",
        value=st.session_state.ticket_text,
        height=180,
        placeholder="Ex: vpn nao conecta, senha expirada, impressora offline",
    )
    submitted = st.form_submit_button("Classificar")

if submitted:
    cleaned_text = ticket_text.strip()
    st.session_state.ticket_text = ticket_text

    if not cleaned_text:
        st.session_state.result = None
        st.warning("Digite a descricao do chamado antes de classificar.")
    else:
        st.session_state.result = predict_ticket(cleaned_text)

result = st.session_state.result
if result:
    col1, col2 = st.columns(2)
    col1.metric("Categoria", result["categoria"])
    col2.metric("Prioridade", result["prioridade"])
elif submitted and st.session_state.ticket_text.strip():
    st.info("Nenhum resultado retornado.")
