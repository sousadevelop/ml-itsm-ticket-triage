# Triagem Automática de Chamados de TI

## Resumo
Este repositório implementa um protótipo de triagem automática de chamados de tecnologia da informação em português brasileiro, com foco em classificação simultânea de categoria e prioridade a partir de descrições textuais livres. A solução final combina `Scikit-Learn` para o treinamento e persistência do modelo com `Streamlit` para a interface interativa de inferência.

## 1. Visão geral
O fluxo do projeto foi organizado em duas etapas principais:

1. `train.py` cria um conjunto sintético de exemplos em pt-BR, ajusta um pipeline supervisionado e salva o artefato `pipeline_itsm.joblib`.
2. `app.py` carrega o pipeline salvo com `joblib`, expõe a interface via `Streamlit` e executa inferência em tempo real.

Quando o arquivo do modelo não está presente no diretório raiz, o aplicativo usa uma rotina local de demonstração apenas para manter a interface operante. Em condições normais de execução, a predição deve ser feita exclusivamente pelo artefato treinado.

## 2. Arquitetura final
A solução final adota a seguinte cadeia de processamento:

- entrada textual do chamado;
- vetorização com `TfidfVectorizer` em unigramas;
- remoção manual de stop words em português;
- classificação multi-rótulo com `MultiOutputClassifier(RandomForestClassifier)`;
- persistência do pipeline com `joblib.dump`;
- carregamento sob demanda em `Streamlit` com `@st.cache_resource`;
- exibição dos resultados de categoria e prioridade em componentes `metric`.

Em termos práticos, o modelo recebe apenas a descrição do incidente como entrada. Os rótulos de saída são mantidos em colunas separadas para evitar vazamento de informação e preservar a separação entre atributos e alvo.

## 3. Estrutura de arquivos
```text
.
├── app.py
├── train.py
├── pipeline_itsm.joblib
├── README.md
└── .gitignore
```

Observação: o arquivo `pipeline_itsm.joblib` é o artefato treinado consumido pelo aplicativo. O arquivo `.gitignore` foi configurado para isolar ambientes virtuais, caches, dependências temporárias e diretórios de dados brutos.

## 4. Metodologia
### 4.1 Base sintética
O treinamento utiliza um conjunto sintético em português brasileiro contendo descrições típicas de chamados de suporte, com pares de saída para `categoria` e `prioridade`. O objetivo é demonstrar uma cadeia de inferência reproduzível, e não substituir bases institucionais reais.

### 4.2 Representação textual
As descrições são transformadas por `TfidfVectorizer` com:

- normalização para minúsculas;
- remoção de acentuação;
- n-gramas restritos a 1 termo;
- lista manual de stop words em português voltada a conectivos e termos funcionais de baixa informação.

Essa escolha privilegia palavras-chave técnicas curtas e reduz a dependência de frases completas, o que tende a aumentar a robustez frente a variações de redação e a diminuir viés introduzido por conectivos ou formulações genéricas.

### 4.3 Modelo supervisionado
O classificador utilizado é `MultiOutputClassifier` encapsulando `RandomForestClassifier`. Essa combinação permite prever mais de um alvo a partir do mesmo texto de entrada, sem exigir arquiteturas externas para cada rótulo.

### 4.4 Persistência e inferência
Após o ajuste, o pipeline é salvo em disco com `joblib`. O aplicativo Streamlit reutiliza o mesmo artefato, evitando divergência entre treino e uso. O carregamento é memoizado com `@st.cache_resource` para reduzir custo de inicialização.

## 5. Controle de data leakage
O código do treinamento foi estruturado para minimizar vazamento de dados:

- somente o campo textual `texto` é usado como entrada do modelo;
- as saídas `categoria` e `prioridade` permanecem separadas como alvos;
- a vetorização faz parte do pipeline, o que evita reutilização indevida de transformações já ajustadas em dados externos ao fluxo;
- o conjunto empregado é sintético e fechado, sem mistura com dados de teste vindos de produção.

Como limitação metodológica, este repositório não implementa divisão formal em treino, validação e teste, nem validação cruzada. Em uma submissão experimental completa, essa etapa deve ser acrescentada com métricas reportadas de forma separada.

## 6. Execução
### 6.1 Ambiente
Recomenda-se Python 3.11 ou superior, com as bibliotecas:

- `scikit-learn`
- `streamlit`
- `joblib`
- `numpy`

### 6.2 Treinamento
```bash
python train.py
```

Esse comando gera ou atualiza `pipeline_itsm.joblib` no diretório raiz.

### 6.3 Aplicação web
```bash
streamlit run app.py
```

O navegador exibirá um formulário para entrada da descrição do chamado e, em seguida, retornará categoria e prioridade previstas pelo pipeline.

## 7. Resultado
Ao executar o sistema o resultado deverá ser como exibido abaixo:
![Interface de triagem de chamados - Resultado da classificação](assets/screenshots/triage-ticket.jpeg)

Link para visualizar o deploy da PoC oficial via web: https://triage-ai.streamlit.app/

## 8. Limitações
O sistema foi concebido como prova de conceito e apresenta limitações relevantes:

- a base de treinamento é sintética e pequena;
- a generalização para linguagem real de operação ainda não foi mensurada;
- não há calibragem explícita de probabilidades;
- não há integração com fila ITSM, API corporativa ou armazenamento persistente;
- o fallback por mock existe apenas para demonstração, não para uso operacional.

## 9. Reprodutibilidade
Para reprodutibilidade mínima:

- execute `train.py` para gerar o artefato treinado;
- mantenha a mesma versão de Python e das bibliotecas;
- preserve o arquivo `pipeline_itsm.joblib` quando quiser reproduzir a inferência já ajustada;
- registre as versões de dependências em um arquivo de ambiente ou `requirements.txt` caso a submissão exija rastreabilidade adicional.

## 10. Referências BibTeX
```bibtex
@misc{scikit-learn,
  author       = {{Scikit-learn developers}},
  title        = {Scikit-learn: Machine Learning in Python},
  year         = {2026},
  howpublished = {\url{https://scikit-learn.org/}},
  note         = {Acessado em 07 jun. 2026}
}

@misc{streamlit,
  author       = {{Streamlit Inc.}},
  title        = {Streamlit: The fastest way to build and share data apps},
  year         = {2026},
  howpublished = {\url{https://streamlit.io/}},
  note         = {Acessado em 07 jun. 2026}
}

@misc{joblib,
  author       = {{joblib developers}},
  title        = {joblib: Python utilities for lightweight pipelining},
  year         = {2026},
  howpublished = {\url{https://joblib.readthedocs.io/}},
  note         = {Acessado em 07 jun. 2026}
}

@misc{python,
  author       = {{Python Software Foundation}},
  title        = {Python Language Reference},
  year         = {2026},
  howpublished = {\url{https://www.python.org/}},
  note         = {Acessado em 07 jun. 2026}
}
```

## 11. Nota de tradução
A tradução para outro idioma deve ser feita a partir deste README em português, preservando a estrutura modular e as citações BibTeX.
