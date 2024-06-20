import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

arbitros = pd.ExcelFile('arbitros_br24.xlsx')
abas = arbitros.sheet_names
# Criar um DataFrame para cada aba
dfs = {aba: pd.read_excel(arbitros, sheet_name=aba) for aba in abas}

# Definindo o dicionário de mapeamento de renomeação
rename_mapping = {
    'Competição_1': 'Campeonato',
    'Competição_2': 'Jogos',
    'Utilizações': 'Amarelos',
    'Column1': 'Segundo_amarelo',
    '_3': 'Vermelho',
    '_4': 'Penalt'
}

# Loop para renomear as colunas em cada dicionário da lista
for key, df in dfs.items():
    dfs[key] = df.rename(columns=rename_mapping)


for nome_df, df in dfs.items():
    globals()[nome_df] = df

for nome_df in dfs.keys():
    globals()[nome_df] = globals()[nome_df].iloc[1:]


# Lista de todos os DataFrames
dfs_arbitros = [Ramon_Abatti, Braulio, Anderson_Daronco, Raphael_Claus, Bruno_Arleu,
       Rafael_Klein, Wilton_Sampaio, Paulo_Cesar_Zanovelli, Rodrigo_Jose_Pereira_de_Lima,
       Flavio_Rodrigues_de_Souza, Felipe_Fernandes, Marcelo_de_Lima_Henrique, Luiz_Flávio_de_Oliveira,
       Lucas_Paulo_Torezin, Alex_Gomes_Stefano, Jonathan_Benkenstein_Pinheiro, Bruno_Pereira_Vasconcelos,
       João_Vitor_Gobi, Gustavo_Ervino_Bauermann, Matheus_Delgado_Candançan, Wagner_do_Nascimento_Magalhães,
       Caio_Max_Augusto_Vieira, Savio_Pereira_Sampaio, Edina_Alves_Batista, Jefferson_Ferreira_Moraes,
       Emerson_Ricardo, André_Luiz_Skettino_Policarpo_B, Fábio_Augusto_Santos_Sá_Júnior,
       Anderson_Ribeiro_Gonçalves, Maguielson_Lima_Barbosa, Yuri_Elino_Ferreira_da_Cruz,
       Paulo_Belence_Alves_dos_Prazere, Arthur_Gomes_Rabelo, Davi_de_Oliveira_Lacerda,
       Bruno_Mota_Correia, Kleber_Ariel_Gonçalves_da_Silva]



lista_arbitros = ['Alex Gomes Stefano', 'Anderson Daronco', 'Anderson Ribeiro Gonçalves', 
                  'André Luiz Skettino Policarpo B', 'Arthur Gomes Rabelo', 'Braulio', 
                  'Bruno Arleu', 'Bruno Mota Correia', 'Bruno Pereira Vasconcelos', 
                  'Caio Max Augusto Vieira', 'Davi de Oliveira Lacerda', 'Edina Alves Batista', 
                  'Emerson Ricardo', 'Fábio Augusto Santos Sá Júnior', 'Felipe Fernandes', 
                  'Flavio Rodrigues de Souza', 'Gustavo Ervino Bauermann', 
                  'Jefferson Ferreira Moraes', 'João Vitor Gobi', 'Jonathan Benkenstein Pinheiro', 
                  'Kleber Ariel Gonçalves da Silva', 'Lucas Paulo Torezin', 'Luiz Flávio de Oliveira', 
                  'Maguielson Lima Barbosa', 'Marcelo de Lima Henrique', 'Matheus Delgado Candançan', 
                  'Paulo Belence Alves dos Prazere', 'Paulo Cesar Zanovelli', 'Rafael Klein', 
                  'Ramon Abatti', 'Rodrigo Jose Pereira de Lima', 
                  'Savio Pereira Sampaio', 'Wagner do Nascimento Magalhães', 
                  'Wilton Sampaio', 'Yuri Elino Ferreira da Cruz']




# Itera sobre a lista de árbitros e DataFrames
for nome_arbitro, df_arbitro in zip(lista_arbitros, dfs_arbitros):
    # Adiciona a coluna "arbitro" com o nome do árbitro ao DataFrame correspondente
    df_arbitro['arbitro'] = nome_arbitro


# Concatenando todos os DataFrames da lista dfs
arbitragem_br24 = pd.concat(dfs_arbitros, ignore_index=True)

arbitragem_br24 = arbitragem_br24.drop(columns=['Competição', '_5', ' '])








# Configuração STREAMLIT
st.title('Análise de Estatísticas por Critério')
st.sidebar.title('Filtros')

# Opções de filtro
filtro_arbitro = st.sidebar.selectbox('Selecione o Árbitro:', arbitragem_br24['arbitro'].unique())
filtro_cartao = st.sidebar.selectbox('Selecione o Tipo de Cartão:', ['Amarelos', 'Segundo_amarelo', 'Vermelho'])

# Filtrar o DataFrame pelo árbitro selecionado
df_arbitro = arbitragem_br24[arbitragem_br24['arbitro'] == filtro_arbitro]

# Obter os campeonatos que o árbitro apitou
campeonatos_arbitro = df_arbitro['Campeonato'].unique()

# Opções de filtro para o tipo de campeonato (limitadas aos campeonatos do árbitro)
filtro_campeonato = st.sidebar.selectbox('Selecione o Tipo de Campeonato:', campeonatos_arbitro)

# Filtrar o DataFrame pelo árbitro selecionado e tipo de campeonato
df_arbitro_campeonato = df_arbitro[df_arbitro['Campeonato'] == filtro_campeonato]

# Filtrar apenas as colunas numéricas para calcular a média
colunas_numericas = df_arbitro_campeonato.select_dtypes(include='number').columns
df_arbitro_campeonato_numeric = df_arbitro_campeonato[colunas_numericas]

# Calcular as estatísticas do árbitro selecionado
estatisticas_arbitro = df_arbitro_campeonato_numeric.mean()

# Calcular a média dos outros árbitros para o mesmo tipo de cartão e tipo de campeonato
outros_arbitros = arbitragem_br24[(arbitragem_br24['arbitro'] != filtro_arbitro) & (arbitragem_br24['Campeonato'] == filtro_campeonato)]
media_outros_arbitros = outros_arbitros.groupby('arbitro')[filtro_cartao].mean().mean()

# Calcular as estatísticas do árbitro selecionado em porcentagem
estatisticas_arbitro_percent = (estatisticas_arbitro[filtro_cartao] / 90) * 100  # Supondo 90 minutos de jogo

# Exibir as estatísticas do árbitro selecionado em comparação com a média dos outros
st.header(f'Estatísticas do Árbitro {filtro_arbitro} no {filtro_campeonato}')
st.write(f'Média do Árbitro {filtro_arbitro} para {filtro_cartao} (em porcentagem): {estatisticas_arbitro_percent:.2f}%')

st.header(f'Média dos Outros Árbitros para {filtro_cartao} no {filtro_campeonato}')
st.write(f'Média dos Outros Árbitros para {filtro_cartao} (em porcentagem): {media_outros_arbitros:.2f}%')

# Comparar as estatísticas do árbitro selecionado com a média dos outros em um gráfico
fig, ax = plt.subplots(figsize=(8, 6))
ax.bar(['Árbitro Selecionado', 'Média Outros Árbitros'], [estatisticas_arbitro_percent, media_outros_arbitros], color=['skyblue', 'orange'])
#ax.set_xlabel('Grupo')
ax.set_ylabel(f'{filtro_cartao} (%)')
ax.set_title(f'Comparação do Árbitro {filtro_arbitro} com a Média dos Outros Árbitros \npara {filtro_cartao} no {filtro_campeonato}')
st.pyplot(fig)
