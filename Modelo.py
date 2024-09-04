import streamlit as st
import pandas as pd
import json
import matplotlib.pyplot as plt

# Carregar base de dados de processos ideais
@st.cache
def load_ideal_data(file_path):
    df_ideal = pd.read_csv(file_path)
    return df_ideal

# Carregar dados reais de processos produtivos do JSON
def load_real_data(json_file):
    with open(json_file) as f:
        data = json.load(f)
    df_real = pd.DataFrame(data)
    return df_real

# Comparar os dados ideais e reais
def compare_processes(df_ideal, df_real):
    # Comparar as duas bases (você pode customizar isso de acordo com a natureza dos dados)
    comparison = df_ideal.merge(df_real, on='process_id', suffixes=('_ideal', '_real'))
    comparison['deviation'] = comparison['value_real'] - comparison['value_ideal']
    return comparison

# Visualizar os dados comparados
def plot_comparison(comparison_df, process_name):
    filtered_df = comparison_df[comparison_df['process_name'] == process_name]
    plt.figure(figsize=(10, 6))
    plt.plot(filtered_df['step'], filtered_df['value_ideal'], label='Ideal', marker='o')
    plt.plot(filtered_df['step'], filtered_df['value_real'], label='Real', marker='x')
    plt.fill_between(filtered_df['step'], filtered_df['value_ideal'], filtered_df['value_real'], color='gray', alpha=0.3)
    plt.title(f'Comparação do Processo: {process_name}')
    plt.xlabel('Etapas')
    plt.ylabel('Valor')
    plt.legend()
    st.pyplot(plt)

# Interface da aplicação Streamlit
st.title('Análise Comparativa de Processos Produtivos')

# Carregar dados
ideal_file = st.file_uploader("Carregar Base de Dados Ideal (CSV)", type=['csv'])
if ideal_file:
    df_ideal = load_ideal_data(ideal_file)
    st.write("Dados Ideais:", df_ideal.head())

json_file = st.file_uploader("Carregar Dados Reais (JSON)", type=['json'])
if json_file:
    df_real = load_real_data(json_file)
    st.write("Dados Reais:", df_real.head())

    # Realizar a comparação
    comparison_df = compare_processes(df_ideal, df_real)
    st.write("Dados Comparados:", comparison_df.head())

    # Seleção de processo para visualização detalhada
    process_list = comparison_df['process_name'].unique()
    selected_process = st.selectbox("Selecione um Processo para Visualizar", process_list)

    # Plotar a comparação
    plot_comparison(comparison_df, selected_process)

    # Exibir tabela de desvios
    st.write("Desvios Observados:", comparison_df[['process_name', 'step', 'deviation']])
