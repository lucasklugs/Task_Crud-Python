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
    print("\n--- Gerenciador de Tarefas ---")
    print("Escreva abaixo um dos comandos")
    print("add | list | done <ID> | remove <ID> | edit <ID> | clear-done")

    opcao = input("Escolha uma opção: ")

# Selecionando opção adicionar
    if opcao == "add":
        priority = validate_priority()
        desc = input("Descrição: ")
        t_date = validate_date()      
        status = validate_status()
        crud.create_task(priority, desc, t_date, status)


# Selecionando opção listar
    elif opcao == "list":
        crud.read_task()

# Selecionando opção concluir
    elif opcao.startswith("done"):
        partes = opcao.split() # Cria a lista partes que divide o comando
        if len(partes) == 2 and partes[1].isdigit(): # Se o comando que foi divido possui duas partes e a segunda é um digito
            task_id = int(partes[1]) 
            crud.mark_done(task_id)
        else:
            print("Uso correto: done <ID>")

# Selecionando opção remover
    elif opcao.startswith("remove"):
        partes = opcao.split()
        if len(partes) == 2 and partes[1].isdigit():
            task_id = int(partes[1])
            crud.delete_task(task_id)
        else:
            print("Uso correto: remove <ID>")

# Selecionando opção editar
    elif opcao.startswith("edit"):
        partes = opcao.split()
        if len(partes) == 2 and partes[1].isdigit():
            task_id = int(partes[1])
            task_pr = input("Qual a prioridade da tarefa? ")
            task_desc = input("Qual a descrição? ")
            crud.edit_task(task_pr, task_desc, task_id)
        else:
            print("Uso correto: edit <ID>")

# Selecionando opção deletar concluidos
    elif opcao == "clear-done":
        crud.delete_done()