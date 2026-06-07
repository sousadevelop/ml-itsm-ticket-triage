from pathlib import Path

import numpy as np
from joblib import dump, load
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.multioutput import MultiOutputClassifier
from sklearn.pipeline import Pipeline


BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR / "pipeline_itsm.joblib"
PORTUGUESE_STOP_WORDS = [
    "a",
    "ao",
    "aos",
    "as",
    "com",
    "da",
    "das",
    "de",
    "do",
    "dos",
    "e",
    "em",
    "na",
    "nas",
    "no",
    "nos",
    "o",
    "os",
    "ou",
    "para",
    "por",
    "que",
    "sem",
    "um",
    "uma",
]


def build_synthetic_dataset():
    # Only the free-text description is used as input. Category and priority
    # stay in dedicated labels to avoid feature leakage.
    samples = [
        {
            "texto": "VPN nao conecta no notebook corporativo apos troca de senha do AD",
            "categoria": "rede_seguranca",
            "prioridade": "media",
        },
        {
            "texto": "internet caiu em toda a filial e o wi fi esta oscilando desde cedo",
            "categoria": "rede_seguranca",
            "prioridade": "alta",
        },
        {
            "texto": "firewall bloqueando acesso ao portal do fornecedor pela rede corporativa",
            "categoria": "rede_seguranca",
            "prioridade": "media",
        },
        {
            "texto": "reset de senha para colaborador com login bloqueado no Active Directory",
            "categoria": "acessos_identidade",
            "prioridade": "baixa",
        },
        {
            "texto": "solicitacao de criacao de conta para novo analista no AD e e mail corporativo",
            "categoria": "acessos_identidade",
            "prioridade": "baixa",
        },
        {
            "texto": "usuario da diretoria sem acesso a pasta compartilhada do financeiro no servidor",
            "categoria": "acessos_identidade",
            "prioridade": "alta",
        },
        {
            "texto": "impressora do faturamento nao puxa papel e a fila de impressao parou",
            "categoria": "hardware_impressao",
            "prioridade": "media",
        },
        {
            "texto": "desktop do almoxarifado apresenta tela azul ao iniciar o Windows",
            "categoria": "hardware_impressao",
            "prioridade": "alta",
        },
        {
            "texto": "notebook da recepcao nao liga depois de queda de energia",
            "categoria": "hardware_impressao",
            "prioridade": "alta",
        },
        {
            "texto": "ERP fora do ar impedindo emissao de nota fiscal no fechamento",
            "categoria": "aplicacoes_colaboracao",
            "prioridade": "alta",
        },
        {
            "texto": "Outlook nao envia mensagens externas e retorna erro SMTP",
            "categoria": "aplicacoes_colaboracao",
            "prioridade": "media",
        },
        {
            "texto": "usuario relata que o calendario compartilhado do e mail nao sincroniza",
            "categoria": "aplicacoes_colaboracao",
            "prioridade": "baixa",
        },
        {
            "texto": "erro vpn ip",
            "categoria": "rede_seguranca",
            "prioridade": "media",
        },
        {
            "texto": "vpn dns",
            "categoria": "rede_seguranca",
            "prioridade": "media",
        },
        {
            "texto": "wi fi oscilando",
            "categoria": "rede_seguranca",
            "prioridade": "media",
        },
        {
            "texto": "internet caiu filial",
            "categoria": "rede_seguranca",
            "prioridade": "alta",
        },
        {
            "texto": "dns nao resolve",
            "categoria": "rede_seguranca",
            "prioridade": "alta",
        },
        {
            "texto": "dhcp sem lease",
            "categoria": "rede_seguranca",
            "prioridade": "media",
        },
        {
            "texto": "ip duplicado rede",
            "categoria": "rede_seguranca",
            "prioridade": "media",
        },
        {
            "texto": "switch sem link",
            "categoria": "rede_seguranca",
            "prioridade": "alta",
        },
        {
            "texto": "porta switch down",
            "categoria": "rede_seguranca",
            "prioridade": "alta",
        },
        {
            "texto": "firewall bloqueio acesso",
            "categoria": "rede_seguranca",
            "prioridade": "media",
        },
        {
            "texto": "proxy bloqueado navegador",
            "categoria": "rede_seguranca",
            "prioridade": "media",
        },
        {
            "texto": "mfa vpn falha",
            "categoria": "rede_seguranca",
            "prioridade": "media",
        },
        {
            "texto": "latencia link matriz",
            "categoria": "rede_seguranca",
            "prioridade": "alta",
        },
        {
            "texto": "gateway indisponivel",
            "categoria": "rede_seguranca",
            "prioridade": "alta",
        },
        {
            "texto": "ssid corporativo sem acesso",
            "categoria": "rede_seguranca",
            "prioridade": "media",
        },
        {
            "texto": "roteador sem internet",
            "categoria": "rede_seguranca",
            "prioridade": "alta",
        },
        {
            "texto": "reset senha ad",
            "categoria": "acessos_identidade",
            "prioridade": "baixa",
        },
        {
            "texto": "senha expirada ad",
            "categoria": "acessos_identidade",
            "prioridade": "baixa",
        },
        {
            "texto": "login bloqueado ad",
            "categoria": "acessos_identidade",
            "prioridade": "media",
        },
        {
            "texto": "active directory desbloqueio",
            "categoria": "acessos_identidade",
            "prioridade": "media",
        },
        {
            "texto": "mfa nao valida",
            "categoria": "acessos_identidade",
            "prioridade": "media",
        },
        {
            "texto": "nota fiscal rejeitada erp",
            "categoria": "aplicacoes_colaboracao",
            "prioridade": "alta",
        },
        {
            "texto": "outlook erro smtp",
            "categoria": "aplicacoes_colaboracao",
            "prioridade": "media",
        },
        {
            "texto": "smtp autenticacao falha",
            "categoria": "aplicacoes_colaboracao",
            "prioridade": "media",
        },
        {
            "texto": "outlook nao sincroniza",
            "categoria": "aplicacoes_colaboracao",
            "prioridade": "media",
        },
        {
            "texto": "email fila parada",
            "categoria": "aplicacoes_colaboracao",
            "prioridade": "media",
        },
        {
            "texto": "anexo outlook bloqueado",
            "categoria": "aplicacoes_colaboracao",
            "prioridade": "baixa",
        },
        {
            "texto": "teams sem audio",
            "categoria": "aplicacoes_colaboracao",
            "prioridade": "media",
        },
        {
            "texto": "sharepoint acesso erro",
            "categoria": "aplicacoes_colaboracao",
            "prioridade": "media",
        },
        {
            "texto": "backup falhou servidor",
            "categoria": "aplicacoes_colaboracao",
            "prioridade": "alta",
        },
        {
            "texto": "restauracao backup urgente",
            "categoria": "aplicacoes_colaboracao",
            "prioridade": "alta",
        },
        {
            "texto": "cadastro cliente erp",
            "categoria": "aplicacoes_colaboracao",
            "prioridade": "baixa",
        },
        {
            "texto": "planilha sharepoint bloqueada",
            "categoria": "aplicacoes_colaboracao",
            "prioridade": "baixa",
        },
        {
            "texto": "portal fornecedor indisponivel",
            "categoria": "aplicacoes_colaboracao",
            "prioridade": "media",
        },
        {
            "texto": "sistema fiscal travando",
            "categoria": "aplicacoes_colaboracao",
            "prioridade": "alta",
        },
    ]

    textos = [sample["texto"] for sample in samples]
    labels = np.array(
        [[sample["categoria"], sample["prioridade"]] for sample in samples],
        dtype=object,
    )
    return textos, labels


def build_pipeline():
    return Pipeline(
        steps=[
            (
                "tfidf",
                TfidfVectorizer(
                    lowercase=True,
                    strip_accents="unicode",
                    ngram_range=(1, 1),
                    stop_words=PORTUGUESE_STOP_WORDS,
                ),
            ),
            (
                "classifier",
                MultiOutputClassifier(
                    RandomForestClassifier(
                        n_estimators=200,
                        random_state=42,
                        class_weight="balanced_subsample",
                    )
                ),
            ),
        ]
    )


def main():
    textos, labels = build_synthetic_dataset()
    pipeline = build_pipeline()

    pipeline.fit(textos, labels)
    dump(pipeline, MODEL_PATH)

    reloaded_pipeline = load(MODEL_PATH)
    sample_text = "usuario sem acesso ao VPN e ao portal interno apos bloqueio de conta"
    predicted_category, predicted_priority = reloaded_pipeline.predict([sample_text])[0]

    print(f"modelo_salvo={MODEL_PATH}")
    print(f"predicao_validacao_categoria={predicted_category}")
    print(f"predicao_validacao_prioridade={predicted_priority}")


if __name__ == "__main__":
    main()
