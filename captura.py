import psutil as p
import time as t
from datetime import datetime
import mysql.connector
from rich import print

MAQUINA_ID = 1

cnx = mysql.connector.connect(user="aluno",
                              password="sptech",
                              host="localhost",
                              port=3306,
                              database="MonFire")

cursor = cnx.cursor(buffered=True)

ids_configuracao = {}

SQL_BUSCAR_CONFIG = """
    SELECT cm.id
    FROM configuracao_maquina cm
    JOIN componente c ON c.id = cm.fk_componente
    JOIN tipo_componente t ON t.id = c.fk_tipo_componente
    JOIN metrica_componente m ON m.id = t.fk_metrica_componente
    WHERE cm.fk_maquina = %s AND t.nome = %s AND m.nome = %s
"""


def buscar_configuracao(tipo, metrica):
    chave = (tipo, metrica)

    if chave not in ids_configuracao:
        cursor.execute(SQL_BUSCAR_CONFIG, (MAQUINA_ID, tipo, metrica))
        linha = cursor.fetchone()

        if linha is None:
            return None

        ids_configuracao[chave] = linha[0]

    return ids_configuracao[chave]


def banco(tipo, metrica, valor):
    fk_configuracao = buscar_configuracao(tipo, metrica)

    if fk_configuracao is None:
        print(f"[bold red]Configuração não encontrada: máquina {MAQUINA_ID}, {tipo}, {metrica}[/bold red]")
        return

    cursor.execute("INSERT INTO captura (valor, fk_configuracao_maquina) VALUES (%s, %s)",
                   (valor, fk_configuracao))
    cnx.commit()


def CPU():

    print('\n')
    porcentagem_de_uso_cpu = p.cpu_percent(interval=0.1)
    frequencia = p.cpu_freq().current

    if porcentagem_de_uso_cpu >= 80 :
        print(f"Alerta o uso da sua CPU está em: [bold red]{porcentagem_de_uso_cpu}% [/bold red]")

    elif porcentagem_de_uso_cpu >= 50 :
        print(f"Alerta o uso da sua CPU está em: [bold yellow]{porcentagem_de_uso_cpu}% [/bold yellow]")

    else :
        print(f"Porcentagem de uso da CPU: [bold green] {porcentagem_de_uso_cpu}% [/bold green]")

    if frequencia >= 1700 :
        print(f"Alerta a frequência da sua CPU está em: [bold red]{frequencia}Hz [/bold red]")

    elif frequencia >= 1500 :
        print(f"Alerta a frequência da sua CPU está em: [bold yellow]{frequencia}Hz [/bold yellow]")

    else :
        print(f"A frequência da sua CPU está em: [bold green] {frequencia}Hz [/bold green]")

    print('\n')

    banco('CPU', 'Uso', porcentagem_de_uso_cpu)
    # psutil retorna MHz; o banco guarda em GHz
    banco('CPU', 'Frequência', round(frequencia / 1000, 2))


def RAM() :

    porcentagem_de_uso_ram = p.virtual_memory().percent
    memoria_total = round(p.virtual_memory().total / (1024**3))
    memoria_disponivel = round(p.virtual_memory().available / (1024**3))
    memoria_utilizada = round(p.virtual_memory().used / (1024**3))

    if porcentagem_de_uso_ram >= 80 :
        print(f"Alerta o uso da sua RAM está em: [bold red]{porcentagem_de_uso_ram}% [/bold red]")

    elif porcentagem_de_uso_ram >= 65 :
        print(f"Alerta o uso da sua RAM está em: [bold yellow]{porcentagem_de_uso_ram}% [/bold yellow]")

    else :
        print(f"Porcentagem de uso da RAM: [green] {porcentagem_de_uso_ram}% [/green]")


    print(f"Memória RAM total: [bold green]{memoria_total}Gb [/bold green]")

    if memoria_disponivel < 5.5 :
        print(f"Alerta você só tem: [bold red]{memoria_disponivel}Gb da sua RAM dísponivel [/bold red]")

    elif memoria_disponivel < 7 :
        print(f"Alerta você só tem: [bold yellow]{memoria_disponivel}Gb da sua RAM dísponivel [/bold yellow]")

    else :
        print(f"[bold green] {memoria_disponivel}Gb [/bold green]")

    if memoria_utilizada >= 7 :
        print(f"Alerta você está usando: [bold red]{memoria_utilizada}Gb da sua RAM [/bold red]")

    elif memoria_utilizada >= 5.5 :
        print(f"Alerta você está usando: [bold yellow]{memoria_utilizada}Gb da sua RAM [/bold yellow]")

    else :
        print(f"Gigabytes de uso da RAM: [bold green] {memoria_utilizada}Gb [/bold green]")


    print('\n')


    banco('RAM', 'Uso', porcentagem_de_uso_ram)
    banco('RAM', 'Total', memoria_total)
    banco('RAM', 'Disponível', memoria_disponivel)
    banco('RAM', 'Em uso', memoria_utilizada)


def Disco() :

    porcentagem_de_disco = p.disk_usage('C:\\').percent
    espaco_total = round(p.disk_usage('C:\\').total / (1024 ** 3))
    espaco_livre = round(p.disk_usage('C:\\').free / (1024 ** 3))
    espaco_utilizado = round(p.disk_usage('C:\\').used / (1024 ** 3))

    if porcentagem_de_disco >= 80 :
        print(f"Alerta o uso do seu Disco está em: [bold red]{porcentagem_de_disco}% [/bold red]")

    elif porcentagem_de_disco >= 65 :
        print(f"Alerta o uso do seu Disco está em: [bold yellow]{porcentagem_de_disco}% [/bold yellow]")

    else :
        print(f"Porcentagem de uso do Disco: [bold green] {porcentagem_de_disco}% [/bold green]")


    print(f"Espaço total do seu Disco: [bold green] {espaco_total}Gb [/bold green]")


    if espaco_livre < 20 :
        print(f"Alerta o uso do seu Disco está em: [bold red]{espaco_livre}Gb [/bold red]")

    elif espaco_livre <= 45 :
        print(f"Alerta o uso do seu Disco está em: [bold yellow]{espaco_livre}Gb [/bold yellow]")

    else :
        print(f"Espaço livre do seu Disco: [bold green] {espaco_livre}Gb [/bold green]")

    if espaco_utilizado >= 220 :
        print(f"Alerta você só tem [bold red]{espaco_total - espaco_utilizado}Gb do seu Disco dísponivel [/bold red]")

    elif espaco_utilizado >= 150 :
        print(f"Alerta você só tem: [bold yellow]{espaco_total - espaco_utilizado}Gb do seu Disco dísponivel [/bold yellow]")

    else :
        print(f"Espaço do Disco que está sendo utilizado: [bold green] {espaco_utilizado}Gb [/bold green]")


    banco('Disco', 'Uso', porcentagem_de_disco)
    banco('Disco', 'Total', espaco_total)
    banco('Disco', 'Disponível', espaco_livre)
    banco('Disco', 'Em uso', espaco_utilizado)

    print('\n')

    print("Hora da captura:")
    print(datetime.now().strftime("[blue]%H:%M:%S[/blue]"))

    print('\n')


try:
    while True:
        CPU()
        RAM()
        Disco()
        t.sleep(5   )
finally:
    cursor.close()
    cnx.close()