import pandas as pd
from sklearn.tree import DecisionTreeClassifier, export_text
from sklearn.preprocessing import OrdinalEncoder

# 1. Montagem da Base de Dados Expandida (30 instâncias)
data = [
    ["Ruim", "Alta", "Nenhuma", "$0 a $15k", "Instavel", "Jovem", "Alto"],
    ["Desconhecida", "Alta", "Nenhuma", "$15 a $35k", "Instavel", "Jovem", "Alto"],
    ["Desconhecida", "Baixa", "Nenhuma", "$15 a $35k", "Instavel", "Adulto", "Moderado"],
    ["Desconhecida", "Baixa", "Nenhuma", "$0 a $15k", "Instavel", "Jovem", "Alto"],
    ["Desconhecida", "Baixa", "Nenhuma", "Acima de $35k", "Estavel", "Adulto", "Baixo"],
    ["Desconhecida", "Baixa", "Adequada", "Acima de $35k", "Estavel", "Adulto", "Baixo"],
    ["Ruim", "Baixa", "Nenhuma", "$0 a $15k", "Instavel", "Jovem", "Alto"],
    ["Ruim", "Baixa", "Adequada", "Acima de $35k", "Estavel", "Adulto", "Moderado"],
    ["Boa", "Baixa", "Nenhuma", "Acima de $35k", "Estavel", "Adulto", "Baixo"],
    ["Boa", "Alta", "Adequada", "Acima de $35k", "Estavel", "Adulto", "Baixo"],
    ["Boa", "Alta", "Nenhuma", "$0 a $15k", "Instavel", "Jovem", "Alto"],
    ["Boa", "Alta", "Nenhuma", "$15 a $35k", "Estavel", "Adulto", "Moderado"],
    ["Boa", "Alta", "Nenhuma", "Acima de $35k", "Estavel", "Adulto", "Baixo"],
    ["Ruim", "Alta", "Nenhuma", "$15 a $35k", "Instavel", "Jovem", "Alto"],
    ["Boa", "Baixa", "Adequada", "$15 a $35k", "Estavel", "Adulto", "Baixo"],
    ["Boa", "Baixa", "Nenhuma", "$15 a $35k", "Estavel", "Adulto", "Baixo"],
    ["Desconhecida", "Alta", "Adequada", "Acima de $35k", "Estavel", "Adulto", "Baixo"],
    ["Desconhecida", "Alta", "Nenhuma", "Acima de $35k", "Instavel", "Jovem", "Moderado"],
    ["Ruim", "Alta", "Adequada", "$15 a $35k", "Instavel", "Adulto", "Moderado"],
    ["Ruim", "Baixa", "Nenhuma", "$15 a $35k", "Instavel", "Jovem", "Alto"],
    ["Boa", "Alta", "Adequada", "$15 a $35k", "Estavel", "Jovem", "Moderado"],
    ["Boa", "Baixa", "Nenhuma", "$0 a $15k", "Estavel", "Adulto", "Moderado"],
    ["Desconhecida", "Baixa", "Adequada", "$0 a $15k", "Instavel", "Jovem", "Moderado"],
    ["Ruim", "Alta", "Adequada", "Acima de $35k", "Estavel", "Adulto", "Baixo"],
    ["Ruim", "Baixa", "Nenhuma", "Acima de $35k", "Instavel", "Adulto", "Moderado"],
    ["Boa", "Baixa", "Adequada", "Acima de $35k", "Estavel", "Jovem", "Baixo"],
    ["Desconhecida", "Alta", "Nenhuma", "$0 a $15k", "Instavel", "Jovem", "Alto"],
    ["Ruim", "Alta", "Nenhuma", "$0 a $15k", "Instavel", "Adulto", "Alto"],
    ["Boa", "Alta", "Nenhuma", "Acima de $35k", "Instavel", "Jovem", "Moderado"],
    ["Desconhecida", "Baixa", "Adequada", "$15 a $35k", "Estavel", "Adulto", "Baixo"]
]

columns = ["Historia", "Divida", "Garantia", "Renda", "Estabilidade", "Idade", "Risco"]
df = pd.DataFrame(data, columns=columns)

# 2. Separação de Atributos e Classe
X = df.drop("Risco", axis=1)
y = df["Risco"]

# 3. Codificação dos dados categóricos
encoder = OrdinalEncoder()
X_encoded = encoder.fit_transform(X)

# 4. Treinamento da Árvore de Decisão CART (Impureza de Gini)
model = DecisionTreeClassifier(criterion="gini", max_depth=4, random_state=42)
model.fit(X_encoded, y)

# 5. Exportação do Texto de Regras
rules = export_text(model, feature_names=list(X.columns))
print("=== REGRAS EXTRAÍDAS PELA ÁRVORE DE DECISÃO (CART) ===")
print(rules)
