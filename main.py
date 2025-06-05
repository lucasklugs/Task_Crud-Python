from connection import get_connection
from task import TaskCrud
from datetime import date,datetime
from task_repository import TaskRepository
from validation import validate_priority, validate_status, validate_date

conn = get_connection()
if not conn:
    print("Conexão não Encontrada")

task_repository = TaskRepository(conn)

crud = TaskCrud(task_repository)
crud.create_table()

# Criando o menu
while True:
    print("|                                                                                                                       |")
    print("|                                      --- Gerenciador de Tarefas ---                                                   |")
    print("|                                       Escreva abaixo um dos comandos                                                  |")
    print("| adicionar | listar | concluir <ID> | remover <ID> | editar <ID> | tasks_hoje | prazos | limpar concluidas | finalizar |")

    opcao = input("Escolha uma opção: ")

# Selecionando opção adicionar
    if opcao == "adicionar":
        priority = validate_priority()
        desc = input("Descrição: ")
        t_date = validate_date()      
        status = validate_status()
        crud.create_task(priority, desc, t_date, status)


# Selecionando opção listar
    elif opcao == "listar":
        crud.read_task()

# Selecionando opção concluir
    elif opcao.startswith("concluir"):
        partes = opcao.split() # Cria a lista partes que divide o comando
        if len(partes) == 2 and partes[1].isdigit(): # Se o comando que foi divido possui duas partes e a segunda é um digito
            task_id = int(partes[1]) 
            crud.mark_done(task_id)
        else:
            print("Uso correto: concluir <ID>")

# Selecionando opção remover
    elif opcao.startswith("remover"):
        partes = opcao.split()
        if len(partes) == 2 and partes[1].isdigit():
            task_id = int(partes[1])
            crud.delete_task(task_id)
        else:
            print("Uso correto: remover <ID>")

# Selecionando opção editar
    elif opcao.startswith("editar"):
        partes = opcao.split()
        if len(partes) == 2 and partes[1].isdigit():
            task_id = int(partes[1])
            task_pr = validate_priority()
            task_desc = input("Qual a descrição? ")
            crud.edit_task(task_pr, task_desc, task_id)
        else:
            print("Uso correto: editar <ID>")

# Selecionando opção de listar as tarefas para hoje
    elif opcao == "tasks_hoje":
        crud.today_tasks()

# Selecionando opção de listar as tarefas por data
    elif opcao == "prazos":
        crud.deadline_task()

# Selecionando opção deletar concluidos
    elif opcao == "limpar concluidas":
        crud.delete_done()

# Selecionando opção deletar concluidos
    elif opcao == "finalizar":
        break