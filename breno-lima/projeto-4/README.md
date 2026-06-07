# Projeto 4

**Aluno**: Breno Queiroz Lima
**Matrícula**: 211063069

# Como executar

Crie um `.env` com a APIKEY do Gemini.
Siga o arquivo de exemplo `./pipeline/.env.dev`

```
docker compose up -d --build
```

- API para consulta dos dados em `localhost:8080`
- PDFs baixados e processados podem ser visualizados no Rustfs `localhost:9001`. Credenciais `rustfsadmin`
- Banco de dados com os dados extraidos em `localhost:8081`

# Scraper

Existe dois scrapers

- Itausa
- MRV

# CronJob

Pipeline é executada periodicamente.

# Pipeline

- Scraper - download dos documentos em PDF.
- Documentos são salvos no RustFS
- PDF é convertido para markdown utilizando `pymupdf`.
- A versão em markdown também é salvo no RustFS
- Tabelas são extraídas utilizando expressões regulares.
- Conteúdo é enviado para LMM que processa os dados usando os contratos semanticos `pydantic`
- Dados extraídos são salvos do banco de dados
