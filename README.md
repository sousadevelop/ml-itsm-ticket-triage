# Triagem Automatica de Chamados de TI

## Resumo
Este repositorio organiza um prototipo academico e profissional de Machine Learning para triagem automatica de chamados de TI em portugues brasileiro. A aplicacao combina um pipeline `Scikit-Learn` treinado sobre tickets sinteticos com uma interface `Streamlit` para classificacao simultanea de categoria e prioridade.

## Problema resolvido
Centrais de suporte frequentemente recebem descricoes curtas, ruidosas e heterogeneas de incidentes e requisicoes. O objetivo deste projeto e reduzir o tempo inicial de roteamento, propondo uma classificacao automatica baseada em palavras-chave tecnicas de ITSM, sem depender de frases completas ou de contexto narrativo extenso.

## Arquitetura da aplicacao
O fluxo principal e composto por:

- entrada textual no `app.py`;
- carregamento do artefato `pipeline_itsm.joblib` com `@st.cache_resource`;
- vetorizacao com `TfidfVectorizer` em unigramas;
- remocao manual de stop words em portugues;
- classificacao multioutput com `MultiOutputClassifier(RandomForestClassifier)`;
- retorno simultaneo de `categoria` e `prioridade`.

O diagrama de arquitetura esta em [assets/diagrams/architecture.mmd](</C:/Users/victt/OneDrive/Documentos/Triagem Automática de Chamados de TI/assets/diagrams/architecture.mmd>).

## Fluxo de classificacao
1. O usuario informa palavras-chave curtas do incidente, como `vpn falha mfa dns`.
2. O texto e normalizado e transformado em vetor TF-IDF.
3. O classificador multioutput estima a categoria operacional e a prioridade do ticket.
4. A interface exibe o resultado imediatamente para apoio ao roteamento inicial.

## Tipos de entrada e saida
Entrada:

- texto livre curto com jargoes de ITSM;
- exemplos: `reset senha ad`, `tela azul memoria`, `outlook erro smtp`.

Saida:

- `categoria`: classe funcional prevista;
- `prioridade`: nivel previsto para tratamento inicial.

Exemplos estruturados estao em [examples/sample_ticket.json](</C:/Users/victt/OneDrive/Documentos/Triagem Automática de Chamados de TI/examples/sample_ticket.json>) e [examples/sample_prediction.json](</C:/Users/victt/OneDrive/Documentos/Triagem Automática de Chamados de TI/examples/sample_prediction.json>).

## Estrutura do repositorio
```text
.
|-- app.py
|-- train.py
|-- requirements.txt
|-- pipeline_itsm.joblib
|-- SECURITY.md
|-- CONTRIBUTING.md
|-- .env.example
|-- examples/
|-- assets/diagrams/
|-- data/
|-- models/
`-- docs/
```

## Instalacao local
```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python train.py
streamlit run app.py
```

## Deploy no Streamlit Cloud
1. Publique o repositorio no GitHub.
2. Configure o app no Streamlit Cloud apontando para `app.py`.
3. Garanta que `requirements.txt` esteja na raiz do projeto.
4. Opcionalmente defina variaveis com base em `.env.example` apenas para ambiente de demonstracao.
5. Refaça o deploy sempre que o pipeline ou dependencias mudarem.

## Metodologia de treinamento
O treinamento usa um conjunto sintetico com jargoes de suporte tecnico e operacoes de TI. O arquivo [train.py](</C:/Users/victt/OneDrive/Documentos/Triagem Automática de Chamados de TI/train.py>) separa explicitamente o texto dos labels, evitando vazamento de dados entre atributos e alvos.

### Representacao textual
O modulo textual foi desenhado para priorizar robustez lexical:

- normalizacao para minusculas;
- remocao de acentos;
- `TfidfVectorizer` com unigramas apenas;
- lista manual de stop words em portugues voltada a conectivos e termos de baixa informacao.

Essa configuracao favorece palavras-chave tecnicas curtas e reduz o vies de classificacao baseado em formulacoes longas ou frases muito especificas.

### Modelo
O classificador utiliza `MultiOutputClassifier` com `RandomForestClassifier`, permitindo inferencia conjunta de categoria e prioridade no mesmo pipeline.

## Resultados
A interface de demonstracao abaixo registra uma classificacao executada localmente pelo aplicativo Streamlit.

![Classificacao Streamlit](assets/screenshots/streamlit-classification.png)

## Limitacoes do modelo

- a base de treinamento e sintetica e nao substitui tickets reais curados;
- nao ha avaliacao estatistica formal com divisao treino-validacao-teste neste estado do projeto;
- o modelo nao incorpora contexto temporal, historico do usuario ou relacoes entre incidentes;
- o comportamento depende fortemente da cobertura do vocabulario tecnico usado na base sintetica.

## Riscos eticos em ambientes de suporte

- classificacoes incorretas podem induzir roteamento inadequado e aumentar tempo de resposta;
- vocabularios sinteticos podem refletir vieses do curador e sub-representar equipes ou servicos;
- previsoes automaticas nao devem substituir analise humana em cenarios criticos;
- logs, exemplos e screenshots devem permanecer sanitizados para evitar exposicao operacional.

## Proximos passos

- adicionar avaliacao quantitativa com metricas por classe;
- introduzir testes automatizados de regressao para o pipeline;
- incorporar configuracao de classes e prioridades por arquivo externo;
- adicionar API de inferencia para integracao com plataformas ITSM;
- avaliar modelos lineares e embeddings leves para comparacao.

## Bibliografia BibTeX
```bibtex
@misc{python,
  author       = {{Python Software Foundation}},
  title        = {Python Language Reference},
  year         = {2026},
  howpublished = {\url{https://www.python.org/}},
  note         = {Accessed 2026-06-07}
}

@misc{numpy,
  author       = {{NumPy Developers}},
  title        = {NumPy},
  year         = {2026},
  howpublished = {\url{https://numpy.org/}},
  note         = {Accessed 2026-06-07}
}

@misc{joblib,
  author       = {{joblib developers}},
  title        = {joblib: Python utilities for lightweight pipelining},
  year         = {2026},
  howpublished = {\url{https://joblib.readthedocs.io/}},
  note         = {Accessed 2026-06-07}
}

@misc{scikit-learn,
  author       = {{Scikit-learn developers}},
  title        = {Scikit-learn: Machine Learning in Python},
  year         = {2026},
  howpublished = {\url{https://scikit-learn.org/}},
  note         = {Accessed 2026-06-07}
}

@misc{streamlit,
  author       = {{Streamlit Inc.}},
  title        = {Streamlit: The fastest way to build and share data apps},
  year         = {2026},
  howpublished = {\url{https://streamlit.io/}},
  note         = {Accessed 2026-06-07}
}
```
