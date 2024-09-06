###### MODELO INSIGHTWISE ######

#Instalar as bibliotecas por linha de comando 

# pip install streamlit
# pip install matplotlib
# pip install openpyxl

#Para Executar o projeto comando: streamlit run Modelo.py

import streamlit as st
import pandas as pd
import json
import matplotlib.pyplot as plt


# Carregar dados 1


# Defina o caminho para o arquivo
file_path = r"c:\Users\User\Downloads\preco-medio-por-embalagem.xlsx"
# Carregar dados reais a partir de um arquivo CSV
def load_ideal_data(file_path):
    df_ideal = pd.read_excel(file_path, engine='openpyxl')  # ou a codificação apropriada
    return df_ideal
df_ideal = load_ideal_data(file_path)

# Carregar dados 2

# Defina o caminho para o arquivo
file_path = r"c:\Users\User\Downloads\preco-medio-por-embalagem.xlsx"
# Carregar dados reais a partir de um arquivo CSV
def load_real_data(file_path):
    df_real = pd.read_excel(file_path, engine='openpyxl')  # ou a codificação apropriada
    return df_real
df_real = load_real_data(file_path)

# Comparar os dados ideais e reais
def compare_processes(df_ideal, df_real):
    # Comparar as duas bases (personalize conforme a natureza dos dados)
    comparison = df_ideal.merge(df_real, on='Período', suffixes=('_ideal', '_real'))
    comparison['deviation'] = comparison['Valor PVP (Ambulatório)_real'] - comparison['Valor PVP (Ambulatório)_ideal']
    return comparison

comparison_df = compare_processes(df_ideal, df_real)

# Calcular a porcentagem de similaridade
def calculate_similarity(comparison_df):
    # Calcula a média dos desvios absolutos
    mean_deviation = comparison_df['deviation'].abs().mean()
    # Calcula a média dos valores ideais
    mean_ideal_value = comparison_df['Valor PVP (Ambulatório)_ideal'].mean()
    # Calcula o erro percentual médio
    mean_percentage_error = (mean_deviation / mean_ideal_value) * 100
    # Calcula a porcentagem de similaridade
    similarity_percentage = 100 - mean_percentage_error
    return similarity_percentage

# Visualizar os dados comparados
def plot_comparison(comparison_df, process_name):
    filtered_df = comparison_df[comparison_df['Região_ideal'] == process_name]
    plt.figure(figsize=(10, 6))
    plt.plot(filtered_df['Período'], filtered_df['Valor PVP (Ambulatório)_ideal'], label='Ideal', marker='o')
    plt.plot(filtered_df['Período'], filtered_df['Valor PVP (Ambulatório)_real'], label='Real', marker='x')
    plt.fill_between(filtered_df['Período'], filtered_df['Valor PVP (Ambulatório)_ideal'], filtered_df['Valor PVP (Ambulatório)_real'], color='gray', alpha=0.3)
    plt.title(f'Comparação do Processo: {process_name}')
    plt.xlabel('Período')
    plt.ylabel('Valor PVP (Ambulatório)')
    plt.legend()
    st.pyplot(plt)

# Interface da aplicação Streamlit
st.title('Análise Comparativa de Processos Produtivos')

# Carregar dados
ideal_file = st.file_uploader("Carregar Base de Dados Ideal (Excel)", type=['xlsx'])
if ideal_file:
    df_ideal = load_ideal_data(ideal_file)
    st.write("Dados Ideais:", df_ideal.head())

real_file = st.file_uploader("Carregar Dados Reais (Excel)", type=['xlsx'])
if real_file:
    df_real = load_real_data(real_file)
    st.write("Dados Reais:", df_real.head())

    if 'df_ideal' in locals() and 'df_real' in locals():
        # Realizar a comparação
        comparison_df = compare_processes(df_ideal, df_real)
        st.write("Dados Comparados:", comparison_df.head())

        # Calcular a porcentagem de similaridade
        similarity_percentage = calculate_similarity(comparison_df)
        st.write(f"Porcentagem de Similaridade: {similarity_percentage:.2f}%")

        # Seleção de processo para visualização detalhada
        process_list = comparison_df['Região_ideal'].unique()
        selected_process = st.selectbox("Selecione uma Região para Visualizar", process_list)

        # Plotar a comparação
        plot_comparison(comparison_df, selected_process)

        # Exibir tabela de desvios
        st.write("Desvios Observados:", comparison_df[['Região_ideal', 'Período', 'deviation']])
