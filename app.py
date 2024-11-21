import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
patio_dados = "C:\\Users\\ana\\OneDrive\\Área de Trabalho\\IBMEC\\Semestre 2\\Programação Estruturada\\projeto_final\\Trabalho Daiso\\Arquivos\\DAISO PATIO VENDA DE PRODUTO.xlsx"
taguatinga_dados = "C:\\Users\\ana\\OneDrive\\Área de Trabalho\\IBMEC\\Semestre 2\\Programação Estruturada\\projeto_final\\Trabalho Daiso\\Arquivos\\DAISO TAGUATINGA VENDA DE PRODUTO.xlsx"
terraco_dados = "C:\\Users\\ana\\OneDrive\\Área de Trabalho\\IBMEC\\Semestre 2\\Programação Estruturada\\projeto_final\\Trabalho Daiso\\Arquivos\\DAISO TERRACO VENDA DE PRODUTO.xlsx"
asasul_dados = "C:\\Users\\ana\\OneDrive\\Área de Trabalho\\IBMEC\\Semestre 2\\Programação Estruturada\\projeto_final\\Trabalho Daiso\\Arquivos\\Cópia de DAISO_ASA_SUL_VENDA_DE_PRODUTO(1).xlsx"

df_patio = pd.read_excel(patio_dados)
df_tagua = pd.read_excel(taguatinga_dados)
df_terraco = pd.read_excel(terraco_dados)
df_asasul = pd.read_excel(asasul_dados)

df_lojas= [df_patio, df_tagua, df_terraco, df_asasul]

# Função para criar filtros e ordenações
def display_filtered_table(title, df):
    # Título da tabela com destaque e cor personalizada
    st.markdown(
        f"<h3 style='color: #d9017f;'>{title}</h3>",
        unsafe_allow_html=True
    )

    # Filtros
    produto_filter = st.text_input(f"Filtrar por produto ({title}):")
    nome_filter = st.text_input(f"Filtrar por nome ({title}):")
    
    filtered_df = df.copy()
    if produto_filter:
        filtered_df = filtered_df[filtered_df["Produto"].str.contains(produto_filter, case=False, na=False)]
    if nome_filter:
        filtered_df = filtered_df[filtered_df["Nome"].str.contains(nome_filter, case=False, na=False)]

    # Ordenação
    sort_column = st.selectbox(f"Ordenar por coluna ({title}):", df.columns)
    sort_order = st.radio(f"Ordem ({title}):", ["Crescente", "Decrescente"])
    ascending = sort_order == "Crescente"
    
    filtered_df = filtered_df.sort_values(by=sort_column, ascending=ascending)

    # Exibição
    st.dataframe(filtered_df)

# Título principal em destaque
st.markdown(
    "<h1 style='text-align: center; color: #d9017f;'>UMA ANÁLISE ESTRATÉGICA DE DADOS NO VAREJO - DAISO</h1>",
    unsafe_allow_html=True
)

# Subtítulo
st.title("Tabela de vendas 2024")

# Exibição das tabelas com filtros e ordenações
display_filtered_table("LOJA DAISO PÁTIO", df_patio)
display_filtered_table("LOJA DAISO TAGUATINGA", df_tagua)
display_filtered_table("LOJA DAISO TERRAÇO", df_terraco)
display_filtered_table("LOJA DAISO ASA SUL", df_asasul)

def faturamento_total(dataframe):
    return dataframe["Total"].sum()

faturamento_loja_patio =  faturamento_total(df_patio)
print(faturamento_loja_patio)
faturamento_loja_tagua =  faturamento_total(df_tagua)
print(faturamento_loja_tagua)
faturamento_loja_terraco = faturamento_total(df_terraco)
print(faturamento_loja_terraco)
faturamento_loja_asasul = faturamento_total(df_asasul)

lojas = ['Pátio', 'Taguatinga', 'Terraço', 'Asa Sul']
faturamentos = [faturamento_loja_patio/3.45367, faturamento_loja_tagua/3.45367, faturamento_loja_terraco/3.45367, faturamento_loja_asasul/3.45367]

fig, ax = plt.subplots(figsize=(8, 6))
ax.bar(lojas, faturamentos, color='#d9017f')
ax.set_title("Faturamento Total por Loja")
ax.set_xlabel("Loja")
ax.set_ylabel("Faturamento em 2024 (R$)")

# Exibindo o gráfico no Streamlit
st.title("Comparação Entre As Lojas 2024")
st.pyplot(fig)
st.markdown("Observada a grande divergência de faturamentos entre as unidades, visto que a Asa Sul apresenta valores muito mais expressivos.")

mensal_asasul = "C:\\Users\\ana\\OneDrive\\Área de Trabalho\\IBMEC\\Semestre 2\\Programação Estruturada\\projeto_final\\Trabalho Daiso\\Arquivos\\Faturamento Mensal Daiso Asa Sul.xlsx"
df_mensal_asasul = pd.read_excel(mensal_asasul)

# Supondo que o DataFrame tenha uma coluna de datas e uma coluna de valores
# Substitua 'Data' e 'Valor' pelos nomes reais das colunas no seu arquivo Excel
df_mensal_asasul['Meses'] = pd.to_datetime(df_mensal_asasul['Meses'])  # Converte a coluna de data para o tipo datetime
df_mensal_asasul = df_mensal_asasul.sort_values(by='Meses')  # Ordena por data, caso necessário

# Configurar o gráfico de linha
plt.figure(figsize=(10, 6))
plt.plot(df_mensal_asasul['Meses'], df_mensal_asasul['Faturamento'], color='#d9017f', marker='o', linestyle='-', linewidth=2, markersize=4)
plt.xlabel('Data')
plt.ylabel('Valor')
plt.title('Faturamento 2023-2024')

# Exibir o gráfico no Streamlit
st.title("Faturamento Mensal Asa Sul 08/2023 - 08/2024")
st.pyplot(plt)
st.markdown("Observada a grande influência do mês natalino nas vendas, demonstrando sazonalidade perceptível.")

import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

# Função para processar o gráfico de Pareto
def process_pareto_chart(df, product_col, revenue_col):
    """
    Processa os dados para criar um gráfico de Pareto.
    """
    # Agrupar por produto e somar o faturamento
    df_sorted = df.groupby(product_col, as_index=False)[revenue_col].sum()
    
    # Ordenar os dados por faturamento em ordem decrescente
    df_sorted = df_sorted.sort_values(by=revenue_col, ascending=False)
    
    # Calcular a porcentagem acumulada do faturamento
    df_sorted['Porcentagem Acumulada'] = df_sorted[revenue_col].cumsum() / df_sorted[revenue_col].sum() * 100
    
    return df_sorted

# Lista de DataFrames já carregados
# Exemplo de DataFrames (substitua por seus DataFrames reais)
dataframes = {
    "Pátio Brasil": df_patio,  # df1, df2, etc., são os DataFrames que você já carregou
    "Terraço": df_terraco,
    "Taguatinga": df_tagua,
    "Asa Sul": df_asasul
}

# Configuração do Streamlit
st.title('Gráfico de Pareto para Faturamento de Produtos')

# Iterar sobre os DataFrames e exibir os gráficos
for nome_loja, df in dataframes.items():
    st.subheader(f"Gráfico de Pareto para {nome_loja}")

    # Definir as colunas de produto e faturamento
    product_col = 'Nome'  # Nome da coluna de produtos
    revenue_col = 'Total'  # Nome da coluna de faturamento
    
    # Verificar se as colunas existem no DataFrame
    if product_col not in df.columns or revenue_col not in df.columns:
        st.error(f"O DataFrame '{nome_loja}' não contém as colunas '{product_col}' e/ou '{revenue_col}'.")
        continue
    
    # Processar os dados usando a função de Pareto
    df_sorted = process_pareto_chart(df, product_col, revenue_col)

    # Plotar o gráfico de Pareto estilizado
    fig, ax1 = plt.subplots(figsize=(12, 6))

    # Gráfico de barras para faturamento
    ax1.bar(df_sorted[product_col], df_sorted[revenue_col], color='#d9017f', label='Faturamento')
    ax1.set_xlabel('Nome')
    ax1.set_ylabel('Total', color='#d9017f')
    ax1.tick_params(axis='y', labelcolor='#d9017f')

    # Gráfico de linha para a porcentagem acumulada
    ax2 = ax1.twinx()
    ax2.plot(df_sorted[product_col], df_sorted['Porcentagem Acumulada'], color='#d9017f', label='Porcentagem Acumulada')
    ax2.set_ylabel('Porcentagem Acumulada (%)', color='#d9017f')
    ax2.tick_params(axis='y', labelcolor='#d9017f')

    # Adicionar uma linha de referência de 80%
    ax2.axhline(80, color='#d9017f', linestyle='--', linewidth=1)
    ax2.text(len(df_sorted) * 0.8, 80, '80%', color='#d9017f', fontsize=12, verticalalignment='bottom')

    plt.title(f'Gráfico de Pareto - {nome_loja}')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()

    # Exibir o gráfico no Streamlit
    st.pyplot(fig)

    df_sorted['Total'] = df_sorted['Total'] / 3.45367

    # Exibir produtos que representam 80% do faturamento
    produtos_80 = df_sorted[df_sorted['Porcentagem Acumulada'] <= 80]
    # Exibir título em rosa e sem negrito
    st.markdown("""
<div style="font-size:20px; color:#d9017f; font-weight:bold;">
    Produtos que representam aproximadamente 80% do faturamento:
</div>
""", unsafe_allow_html=True)
    st.write(produtos_80)
