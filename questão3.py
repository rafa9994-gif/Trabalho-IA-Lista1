import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

# 1. Carregamento da base de dados pública
url = "https://raw.githubusercontent.com/jbrownlee/Datasets/master/pima-indians-diabetes.data.csv"
cols = ["Pregnancies", "Glucose", "BloodPressure", "SkinThickness", "Insulin", "BMI", "Pedigree", "Age", "Outcome"]
df = pd.read_csv(url, names=cols)

# 2. Divisão X e y
X = df.drop("Outcome", axis=1)
y = df["Outcome"]

# 3. Separação Treino (80%) e Teste (20%)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

# 4. Treinamento do Modelo
dt_model = DecisionTreeClassifier(max_depth=4, random_state=42)
dt_model.fit(X_train, y_train)

# 5. Predições e Métricas
y_pred = dt_model.predict(X_test)

print("=== MÉTRICAS DE DESEMPENHO - ÁRVORE DE DECISÃO ===")
print(f"Acurácia:  {accuracy_score(y_test, y_pred)*100:.2f}%")
print(f"Precisão: {precision_score(y_test, y_pred)*100:.2f}%")
print(f"Recall:   {recall_score(y_test, y_pred)*100:.2f}%")
print(f"F1-Score: {f1_score(y_test, y_pred)*100:.2f}%")
