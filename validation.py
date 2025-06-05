from datetime import datetime

# Valida o input de prioridade
def validate_priority():
    while True:
        priority = input("Prioridade (alta, média, baixa): ").lower()
        if priority  in ["alta", "média", "baixa"]:
            return priority 
        print("Prioridade inválida. Escolha entre alta, média ou baixa.")

# Valida o input de data
def validate_date():
    while True:
        t_date = input("Prazo de Entrega (AAAA-MM-DD): ")
        try:
            datetime.strptime(t_date, "%Y-%m-%d")
            return t_date
        except ValueError:
            print("Formato de data inválido.")

# Valida o input de status
def validate_status():
    while True:
        status = input("Status (pendente, concluída): ").lower()
        if status  in ["pendente", "concluída"]:
            return status 
        print("Status inválido. Escolha entre pendente, concluída.")