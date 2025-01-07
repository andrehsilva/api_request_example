import requests
import pandas as pd
import numpy as np
from datetime import date

def up(data):
    data.columns = data.columns.str.upper()
    for columns in data.columns:
        if data[columns].dtype == 'object':
            data[columns] = data[columns].str.upper()
    return data

def clean_cpf(df, column_name):
    df[column_name] = df[column_name].apply(lambda x: x.replace('.', '').replace('-', '') if pd.notnull(x) else x)

def clean_sheet_name(name):
    return ''.join(e for e in name if e.isalnum())

# Funções da API (dados ocultos)
def fetch_data(token):
    response = requests.get(f'https://endereco_da_api/?token={token}')
    return response.json()

def prepare_dataframes(dataframes):
    prepared_dfs = {}
    for nome_escola, df in dataframes.items():
        sheet_name = clean_sheet_name(nome_escola.split(":")[1])
        prepared_dfs[sheet_name] = df
    return prepared_dfs

def prepare_combined_dataframe(dataframes):
    combined_df = pd.concat(
        [df.assign(escola=nome_escola) for nome_escola, df in dataframes.items()],
        ignore_index=True
    )
    return combined_df

# Substitua as credenciais de API abaixo
dados_api = {
    "ESCOLA_1": "SEU_TOKEN_AQUI",
    "ESCOLA_2": "SEU_TOKEN_AQUI",
    "ESCOLA_3": "SEU_TOKEN_AQUI",
    # Adicione outras escolas e tokens conforme necessário
}

# Configuração inicial
today = date.today().strftime('%d-%m-%Y')
caminho = '/content/drive/MyDrive/Colab Notebooks/Conexia/api_hello'

"""LEX"""

lex = pd.read_csv(f'{caminho}/input/select_lex.csv', sep=',')
lex = lex[lex['general_registration_status']=='ATIVO']
#del(lex['general_registration_status'])
lex.head(1)

lex[lex['user_name']=='LUANA ARRUDA MENDES']

lex[lex['school_id']=='ALUNO'].count()

lex[lex['user_name'].str.contains('AGATHA', na=False)]

lex.to_excel(f'{caminho}/output/lex.xlsx', index=False)

df_lex = lex.copy()
up(df_lex)
df_lex.head(2)

df_lex = df_lex.rename(columns={'BIRTH_DATE': 'BIRTHDATE','SCHOOL_NAME':'SCHOOLNAME','USER_ID':'ID','USER_NAME':'NAME','SCHOOL_ID':'IS_STUDENT'})
df_lex['BIRTHDATE'] = pd.to_datetime(df_lex['BIRTHDATE'], errors='coerce') # Use df_lex here

# Format 'birth_date' to 'YYYY-MM-DD'
df_lex['BIRTHDATE'] = df_lex['BIRTHDATE'].dt.strftime('%Y-%m-%d')

# Convert 'CPF' column to string type before applying the lambda function
df_lex['CPF'] = df_lex['CPF'].astype(str).apply(lambda x: x.replace('.', '').replace('-', '') if pd.notnull(x) else x)

df_lex['NAMEBIRTHDATE'] = df_lex['NAME'] + df_lex['BIRTHDATE']
df_lex = df_lex[['SCHOOLNAME','ID','CPF','IS_STUDENT','NAME','BIRTHDATE','EMAIL','NAMEBIRTHDATE']]
df_lex['DATAFRAME'] = 'LEX'

df_lex = df_lex[df_lex['IS_STUDENT'].isin(['RESPONSÁVEL', 'ALUNO'])]

df_lex['IS_STUDENT'] = df_lex['IS_STUDENT'].apply(lambda x: True if x == 'ALUNO' else False)

df_lex.head(2)

lex[lex['user_name'].str.contains('LUANA ARRUDA', na=False)]

df_lex.ID.count()

############ API

dataframes = {nome_escola: pd.DataFrame(fetch_data(token)) for nome_escola, token in dados_api.items()}
dataframes = prepare_dataframes(dataframes)
hello = prepare_combined_dataframe(dataframes)

df_hello = hello.copy()
up(df_hello)
df_hello.head(2)

df_hello = df_hello.rename(columns={'BIRTH_DATE': 'BIRTHDATE','DOCUMENT':'CPF','ESCOLA':'SCHOOLNAME','USER_ID':'ID_TELLME','USER_EXTERNAL_ID':'ID'})

df_hello['BIRTHDATE'] = pd.to_datetime(df_hello['BIRTHDATE'], errors='coerce')

# Format 'birth_date' to 'YYYY-MM-DD'
df_hello['BIRTHDATE'] = df_hello['BIRTHDATE'].dt.strftime('%Y-%m-%d')
df_hello['CPF'] = df_hello['CPF'].apply(lambda x: x.replace('.', '').replace('-', '') if pd.notnull(x) else x)

df_hello['NAMEBIRTHDATE'] = df_hello['NAME'] + df_hello['BIRTHDATE']
df_hello = df_hello[['SCHOOLNAME','ID','CPF','IS_STUDENT','NAME','BIRTHDATE','EMAIL','NAMEBIRTHDATE','ID_TELLME']]
df_hello['DATAFRAME'] = np.where(df_hello['ID'].str.len() < 6, 'SPONTE', 'HELLO')
df_hello = df_hello[['SCHOOLNAME','ID','CPF','IS_STUDENT','NAME','BIRTHDATE','EMAIL','NAMEBIRTHDATE','DATAFRAME','ID_TELLME']]
df_hello.head(2)

# prompt: fazer um join com o df_hello e o df_lex, com o resultado do que há a mais no df_lex, ollhar por NAMEBIRTHDATE ou ID

# Merge the two dataframes based on 'NAMEBIRTHDATE' and 'ID'
merged_df = pd.merge(df_lex, df_hello, on=['NAMEBIRTHDATE', 'ID'], how='left', indicator=True)

# Filter the merged dataframe to show rows that are only present in df_lex
df_lex_only = merged_df[merged_df['_merge'] == 'left_only']

# Remove the '_merge' column
df_lex_only = df_lex_only.drop('_merge', axis=1)
df_lex_only
df_lex_only.to_excel(f'{caminho}/output/df_lex_only.xlsx', index=False)

df_hello = df_hello[df_hello['DATAFRAME']=='HELLO']

### Pesquisas

df_hello.ID.count()

df_groupby = df.groupby('ID').agg({'ID': 'count'}).rename(columns={'ID': 'ID_count'}).reset_index()
df_groupby
#The 'ID' column resulting from the aggregation is first renamed to 'ID_count' to avoid the conflict.

df_groupby = df.groupby('ID').agg({'ID': 'count', 'NAMEBIRTHDATE':',' .join,'SCHOOLNAME':',' .join,'DATAFRAME' : ',' .join}).rename(columns={'ID': 'ID_count'}).reset_index()
df_groupby
#The 'ID' column resulting from the aggregation is first renamed to 'ID_count' to avoid the conflict.

df_groupby.to_excel(f'{caminho}/output/df_groupby.xlsx', index=False)

cpf_vazios = df['CPF'].isnull().sum()
print(f"Número de registros de CPF vazios: {cpf_vazios}")

# prompt: fazer um join com o df_hello e o df_lex, com o resultado do que há a mais no df_hello, ollhar por NAMEBIRTHDATE ou ID

# Merge the two dataframes based on 'NAMEBIRTHDATE' or 'ID', keeping only rows present in df_hello
merged_df = pd.merge(df_hello, df_lex, on=['NAMEBIRTHDATE', 'ID'], how='left', indicator=True)

# Filter the merged dataframe to show rows that are only present in df_hello
df_hello_only = merged_df[merged_df['_merge'] == 'left_only']

# Remove the '_merge' column
df_hello_only = df_hello_only.drop('_merge', axis=1)

# Display the resulting dataframe
df_hello_only
df_hello.to_excel(f'{caminho}/output/df_hello_only.xlsx', index=False)
