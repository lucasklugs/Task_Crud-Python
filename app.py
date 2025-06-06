from src.connection import get_connection
from src.task import TaskCrud
from datetime import date,datetime
from src.task_repository import TaskRepository

import streamlit as st

conn = get_connection()
if not conn:
    print("Conexão não Encontrada")

task_repository = TaskRepository(conn)
crud = TaskCrud(task_repository)
crud.create_table()

def add_task():
    st.subheader("Adicionar Tarefa")

    priority = st.selectbox("Prioridade", ["", "Baixa", "Média", "Alta"])
    description = st.text_input("Descrição")
    deadline = st.date_input("Prazo de Entrega", min_value=datetime.today())
    status = st.selectbox("Status", ["", "Pendente", "Concluída"])

    if st.button("Salvar Tarefa"):
        if not priority or not description.strip() or not status:
            st.warning("Por favor, preencha todos os campos antes de salvar.")
        else:
            crud.create_task(priority, description, deadline, status)
            st.success("Tarefa adicionada!")
            

def list_task():
    st.subheader("Listar todas as tarefas")
    crud.read_task()

def complete_task():
    st.subheader("Concluir tarefas")
    descriptions = crud.get_pending_descriptions()

    if descriptions:
        task_desc = st.selectbox("Qual tarefa você deseja concluir?", descriptions)
        if st.button("Concluir Tarefa"):
            crud.mark_done_by_description(task_desc)
    else:
        st.info("Não há tarefas pendentes para concluir.")

def edit_task():
    st.subheader("Editar Tarefas")
    descriptions = crud.get_all_descriptions()

    if descriptions:
        actual_task = st.selectbox("Qual tarefa você deseja editar?", [""] + descriptions)
        ed_priority = st.selectbox("Prioridade", ["", "Baixa", "Média", "Alta"])
        ed_desc = st.text_input("Descrição")
        ed_dead = st.date_input("Prazo de Entrega", min_value=datetime.today())
        if st.button("Editar"):
            if not actual_task or not ed_priority or not ed_desc or not ed_dead:
                st.warning("Por favor, preencha todos os campos antes de salvar.")
            else:
                crud.edit_task(actual_task, ed_priority, ed_desc, ed_dead)
    else:
        st.info("Não há tarefas no banco...")

def remove_task():
    st.subheader("Remover tarefas")
    descriptions = crud.get_all_descriptions()

    if descriptions:
        task_desc = st.selectbox("Qual tarefa você deseja editar?",[""] + descriptions)
        if st.button("Excluir"):
            crud.delete_task(task_desc)
    else:
        st.info("Não há tarefas no banco...")

def list_today_bydate():
    st.subheader(f"Tarefas de hoje: ({datetime.today().date().strftime('%Y/%m/%d')})")
    crud.today_tasks()

def deadline_task():
    crud.deadline_task()

def cleardone_task():
    st.subheader("Remover tarefas concluídas")
    if st.button("Excluir"):
        crud.delete_done()

menu_actions = {
    "Adicionar": add_task,
    "Listar": list_task,
    "Editar": edit_task,
    "Remover": remove_task,
    "Concluir": complete_task,
    "Finalizar Concluídas": cleardone_task,
    "Tarefas de Hoje": list_today_bydate,
    "Prazos": deadline_task,
}

# Cria o menu principal
st.title("Gerenciador de Tarefas")
st.write("Organize, acompanhe e conclua suas tarefas de forma simples e eficiente. Nosso sistema permite criar, editar e gerenciar atividades do dia a dia com praticidade e controle total.")

# Cria a barra lateral e um select box para as opções de CRUD
st.sidebar.header("Menu")
menu = st.sidebar.radio("Escolha uma opção:", list(menu_actions.keys()), index=0)
menu_actions[menu]()