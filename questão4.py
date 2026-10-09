import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import wittgenstein as lw

# 1. Carregamento do dataset de Diabetes
url = "https://raw.githubusercontent.com/jbrownlee/Datasets/master/pima-indians-diabetes.data.csv"
cols = ["Pregnancies", "Glucose", "BloodPressure", "SkinThickness", "Insulin", "BMI", "Pedigree", "Age", "Outcome"]
df = pd.read_csv(url, names=cols)

X = df.drop("Outcome", axis=1)
y = df["Outcome"]

# 2. Divisão Treino e Teste (80% / 20%)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

# 3. Treinamento do Modelo RIPPER
ripper = lw.RIPPER(random_state=42)
ripper.fit(X_train, y_train, feature_names=list(X.columns), class_feat='Outcome')

# 4. Predições
y_pred_rules = ripper.predict(X_test)

# 5. Regras Extraídas
print("=== REGRAS DIRETAS EXTRAÍDAS (RIPPER) ===")
for rule in ripper.ruleset_.rules:
    print("SE", rule, "ENTÃO Diabetes = 1")

# 6. Métricas de Desempenho
acc = accuracy_score(y_test, y_pred_rules)
prec = precision_score(y_test, y_pred_rules)
rec = recall_score(y_test, y_pred_rules)
f1 = f1_score(y_test, y_pred_rules)

print("\n=== MÉTRICAS DE DESEMPENHO - RIPPER ===")
print(f"Acurácia:  {acc*100:.2f}%")
print(f"Precisão: {prec*100:.2f}%")
print(f"Recall:   {rec*100:.2f}%")
print(f"F1-Score: {f1*100:.2f}%")
