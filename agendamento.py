import streamlit as st
import csv
from datetime import datetime, timedelta
import os

# Função para carregar os agendamentos existentes do arquivo CSV
def carregar_agendamentos():
    if not os.path.exists("agendamentos.csv") or os.stat("agendamentos.csv").st_size == 0:
        return []

    with open("agendamentos.csv", mode="r", newline="") as file:
        reader = csv.reader(file)
        if os.stat("agendamentos.csv").st_size > 0:
            next(reader)  # Ignorar a primeira linha (cabeçalho)
        return list(reader)

# Função para verificar se há conflitos de horário
def verifica_conflitos(data, horario):
    agendamentos = carregar_agendamentos()
    horario_agendamento = datetime.combine(data, horario)

    for agendamento in agendamentos:
        data_formatada = datetime.strptime(agendamento[0], "%Y-%m-%d")
        horario_formatado = datetime.strptime(agendamento[1], "%H:%M:%S")

        # Verificar se o horário do novo agendamento entra em conflito com agendamentos existentes
        if abs((horario_agendamento - (data_formatada + timedelta(hours=1))).total_seconds()) < 3600:
            return True

    return False

# Função para a página de Agendar
def pagina_agendar():
    st.title("Agendar")
    nome_cliente = st.text_input("Nome do Cliente:", "")
    horario = st.time_input("Horário do Agendamento:", key="horario")
    data = st.date_input("Data do Agendamento:", key="data")
    botao_agendar = st.button("Agendar")

    if botao_agendar:
        if nome_cliente and horario and data:
            if verifica_conflitos(data, horario):
                st.warning("Conflito de horário. Escolha outro horário.")
            else:
                # Formatar data e hora
                data_hora = datetime.combine(data, horario)
                data_formatada = data_hora.strftime("%Y-%m-%d")
                hora_formatada = data_hora.strftime("%H:%M:%S")

                # Verificar se o arquivo CSV está vazio
                arquivo_csv_vazio = os.stat("agendamentos.csv").st_size == 0

                # Adicionar os dados ao arquivo CSV
                with open("agendamentos.csv", mode="a", newline="") as file:
                    writer = csv.writer(file)
                    if arquivo_csv_vazio:  # Adicionar nomes das colunas se o arquivo estiver vazio
                        writer.writerow(["Data", "Hora", "Cliente"])
                    writer.writerow([data_formatada, hora_formatada, nome_cliente])
                st.success("Agendamento realizado com sucesso!")
        else:
            st.warning("Preencha todos os campos para agendar.")

# Função para a página de Ver Agendamentos
def pagina_ver_agendamentos():
    st.title("Ver Agendamentos")

    senha = st.sidebar.text_input("Senha para Acesso à Página:", type="password")

    if senha == "1234":
        botao_limpar = st.button("Limpar Agendamentos")  # Botão para limpar a planilha

        if botao_limpar:
            if os.path.exists("agendamentos.csv"):
                os.remove("agendamentos.csv")
                open("agendamentos.csv", "w").close()  # Cria um novo arquivo CSV vazio
                st.success("Lista de agendamentos e arquivo CSV limpos.")
            else:
                st.warning("O arquivo de agendamentos não existe.")

        # Carregar e exibir os agendamentos existentes
        agendamentos = carregar_agendamentos()
        if len(agendamentos) > 0:
            st.write("### Agendamentos Existentes:")
            st.table(agendamentos)
        else:
            st.write("### Nenhum agendamento existente.")
    elif senha != "":
        st.error("Senha incorreta. Você não tem acesso à página de ver agendamentos.")

# Função principal
def main():
    st.title("Agendamento de Barbearia/Cabeleireiro")

    # Adicione um radio button para selecionar a página
    pagina_selecionada = st.radio("Selecione a página:", ("Agendar", "Ver Agendamentos"))

    if pagina_selecionada == "Agendar":
        pagina_agendar()
    elif pagina_selecionada == "Ver Agendamentos":
        pagina_ver_agendamentos()

if __name__ == "__main__":
    main()
