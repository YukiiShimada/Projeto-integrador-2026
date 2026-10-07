import json
import sqlite3

def transformar_em_texto(valor):
    if valor is None:
        return None

    if isinstance(valor, dict):
        for chave in ("$date", "$oid", "$numberLong", "$numberInt", "$numberDouble"):
            if chave in valor:
                return transformar_em_texto(valor[chave])

        return json.dumps(valor, ensure_ascii=False)

    if isinstance(valor, list):
        return json.dumps(valor, ensure_ascii=False)

    return valor


with open("amostra.json", "r", encoding="utf-8") as arquivo:
    dados = json.load(arquivo)

conexao = sqlite3.connect("banco.db")
cursor = conexao.cursor()

# Recria a tabela para garantir que ela esteja correta
cursor.execute("DROP TABLE IF EXISTS atendimentos")

cursor.execute("""
CREATE TABLE atendimentos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    atendimento_id TEXT,
    data_entrada TEXT,
    data_saida TEXT,
    servico TEXT,
    especialidade TEXT,
    diagnostico TEXT,
    cidade TEXT,
    bairro TEXT,
    sexo TEXT,
    data_nascimento TEXT
)
""")

quantidade = 0

for paciente in dados:
    cidade = transformar_em_texto(paciente.get("cidade"))
    bairro = transformar_em_texto(paciente.get("bairro"))
    sexo = transformar_em_texto(paciente.get("sexo"))
    nascimento = transformar_em_texto(paciente.get("dataNascimento"))

    for registro in paciente.get("registros", []):
        if registro.get("tipo") != "ATENDIMENTO":
            continue

        informacoes = registro.get("informacoes", {})

        cursor.execute("""
        INSERT INTO atendimentos (
            atendimento_id,
            data_entrada,
            data_saida,
            servico,
            especialidade,
            diagnostico,
            cidade,
            bairro,
            sexo,
            data_nascimento
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            transformar_em_texto(informacoes.get("atendimentoId")),
            transformar_em_texto(registro.get("dataEntrada")),
            transformar_em_texto(registro.get("dataSaida")),
            transformar_em_texto(registro.get("servico")),
            transformar_em_texto(informacoes.get("especializacao")),
            transformar_em_texto(informacoes.get("diagnostico")),
            cidade,
            bairro,
            sexo,
            str(nascimento) if nascimento is not None else 
            None
        ))

        quantidade += 1

conexao.commit()

total = cursor.execute(
    "SELECT COUNT(*) FROM atendimentos"
).fetchone()[0]

conexao.close()

print("Banco criado com sucesso!")
print(f"Atendimentos inseridos: {quantidade}")
print(f"Total no banco: {total}")