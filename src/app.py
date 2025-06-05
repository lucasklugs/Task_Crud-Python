from connection import get_connection
from task import TaskCrud
from datetime import date,datetime
from task_repository import TaskRepository
import streamlit as st

conn = get_connection()
if not conn:
    print("Conexão não Encontrada")

task_repository = TaskRepository(conn)
crud = TaskCrud(task_repository)
crud.create_table()

# Cria o menu principal
st.title("Gerenciador de Tarefas")
st.write("Organize, acompanhe e conclua suas tarefas de forma simples e eficiente. Nosso sistema permite criar, editar e gerenciar atividades do dia a dia com praticidade e controle total.")

# Cria a barra lateral e um select box para as opções de CRUD
menu = st.sidebar.selectbox("Menu", ["Adicionar", "Listar", "Concluir", "Editar", "Remover", "Tarefas de Hoje", "Prazos", "Limpar Concluídas"])

if menu == "Adicionar":
    st.subheader("Adicionar Tarefa")
    priority = st.selectbox("Prioridade", ["Baixa", "Média", "Alta"])
    description = st.text_input("Descrição")
    deadline = st.date_input("Prazo de Entrega", min_value=datetime.today())
    status = st.selectbox("Status", ["Pendente", "Em andamento", "Concluída"])
    if st.button("Salvar Tarefa"):
        crud.create_task(priority, description, deadline.isoformat(), status)
        st.success("Tarefa adicionada!")

if menu == "Listar":
    st.subheader("Listar todas as tarefas")
    crud.read_task()

if menu == "Concluir":
    st.subheader("Concluir tarefas")
    descriptions = crud.get_pending_descriptions()

    if descriptions:
        task_desc = st.selectbox("Qual tarefa você deseja concluir?", descriptions)
        if st.button("Concluir Tarefa"):
            crud.mark_done_by_description(task_desc)
    else:
        st.info("Não há tarefas pendentes para concluir.")

if menu == "Editar":
    st.subheader("Editar Tarefas")
    descriptions = crud.get_all_descriptions()

    if descriptions:
        actual_task = st.selectbox("Qual tarefa você deseja editar?", descriptions)
        ed_priority = st.selectbox("Prioridade", ["Baixa", "Média", "Alta"])
        ed_desc = st.text_input("Descrição")
        ed_dead = st.date_input("Prazo de Entrega", min_value=datetime.today())
        if st.button("Editar"):
            crud.edit_task(actual_task, ed_priority, ed_desc, ed_dead)
    else:
        st.info("Não há tarefas no banco...")

if menu == "Remover":
    st.subheader("Remover tarefas")
    descriptions = crud.get_all_descriptions()

    if descriptions:
        task_desc = st.selectbox("Qual tarefa você deseja editar?", descriptions)
        if st.button("Excluir"):
            crud.delete_task(task_desc)
    else:
        st.info("Não há tarefas no banco...")

if menu == "Tarefas de Hoje":
    st.subheader("Tarefas de hoje:")
    crud.today_tasks()

if menu == "Prazos":
    st.subheader("Prazos")
    crud.deadline_task()

if menu == "Limpar Concluídas":
    st.subheader("Remover tarefas concluídas")
    if st.button("Excluir"):
        crud.delete_done()