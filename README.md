# Projeto de Integração de Dados da API

Este projeto realiza a integração de dados provenientes de uma API externa com dados internos armazenados em um arquivo CSV. Ele processa e limpa esses dados para gerar relatórios e agrupamentos em formato Excel.

## Funcionalidades

1. **Funções de Limpeza e Preparação de Dados**:
   - `up(data)`: Normaliza os nomes das colunas para letras maiúsculas.
   - `clean_cpf(df, column_name)`: Limpa e formata o campo CPF.
   - `clean_sheet_name(name)`: Remove caracteres especiais do nome da planilha.

2. **Integração com a API**:
   - `fetch_data(token)`: Obtém dados da API usando o token de autenticação.
   - `prepare_dataframes(dataframes)`: Prepara os DataFrames para processamento.
   - `prepare_combined_dataframe(dataframes)`: Combina os DataFrames em um único DataFrame.

3. **Geração de Relatórios**:
   - Filtragem de dados com base no status de matrícula.
   - Geração de arquivos Excel contendo os resultados processados.

## Como Utilizar

1. **Configuração Inicial**:
   - Defina os tokens de autenticação da API no dicionário `dados_api`. Substitua as credenciais de cada escola pelo seu token real.

2. **Leitura e Processamento de Dados**:
   - O arquivo CSV contendo os dados internos (lex) é lido e filtrado.
   - Os dados da API são obtidos, processados e combinados com os dados locais.

3. **Exportação de Resultados**:
   - Os dados finais são exportados para arquivos Excel, contendo os registros filtrados e agrupados.

## Pré-requisitos

- Python 3.x
- Bibliotecas Python: `requests`, `pandas`, `numpy`

```bash
pip install requests pandas numpy


## Licença
Este projeto está licenciado sob a MIT License
