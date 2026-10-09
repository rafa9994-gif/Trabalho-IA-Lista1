
class BaseDeConhecimento:
    """Módulo 1: Armazenamento e Edição de Fatos e Regras"""
    def __init__(self):
        self.fatos = {}
        self.regras = []

    def adicionar_fato(self, atributo, valor):
        self.fatos[atributo] = valor

    def adicionar_regra(self, id_regra, condicoes, conclusao):
        regra = {
            'id': id_regra,
            'condicoes': condicoes,  
            'conclusao': conclusao   
        }
        self.regras.append(regra)


class ModuloExplicacao:
    """Módulo de Explicação (POR QUÊ? / COMO?)"""
    def __init__(self):
        self.trilha_inferencia = []

    def registrar_passo(self, regra_id, conclusao):
        self.trilha_inferencia.append((regra_id, conclusao))

    def explicar_como(self, objetivo, valor):
        print(f"\n[EXPLICAÇÃO - COMO?]: Como o sistema concluiu que {objetivo} = '{valor}'?")
        if not self.trilha_inferencia:
            print("  -> O valor foi informado diretamente pelo usuário como um fato inicial.")
        else:
            for passo in self.trilha_inferencia:
                print(f"  -> Disparou a Regra {passo[0]}, provando que {passo[1][0]} = '{passo[1][1]}'.")

    def explicar_por_que(self, atributo, regra_avaliada):
        print(f"\n[EXPLICAÇÃO - POR QUÊ?]: Por que o sistema está perguntando sobre '{atributo}'?")
        conds = " E ".join([f"{k}='{v}'" for k, v in regra_avaliada['condicoes'].items()])
        conc = f"{regra_avaliada['conclusao'][0]} = '{regra_avaliada['conclusao'][1]}'"
        print(f"  -> Para testar a Regra {regra_avaliada['id']} (SE {conds} ENTÃO {conc}).")


class EngenhoInferencia:
    """Módulo 2: Engenho de Inferência (Forward, Backward)"""
    def __init__(self, bc, explicacao):
        self.bc = bc
        self.explicacao = explicacao

    def forward_chaining(self):
        """Encadeamento para Frente"""
        novas_inferencias = True
        print("\n--- EXECUTANDO ENCADEMENTO PARA FRENTE (FORWARD CHAINING) ---")
        while novas_inferencias:
            novas_inferencias = False
            for regra in self.bc.regras:
                conc_attr, conc_val = regra['conclusao']
                if self.bc.fatos.get(conc_attr) == conc_val:
                    continue

                satisfeita = True
                for attr, val in regra['condicoes'].items():
                    if self.bc.fatos.get(attr) != val:
                        satisfeita = False
                        break

                if satisfeita:
                    self.bc.fatos[conc_attr] = conc_val
                    self.explicacao.registrar_passo(regra['id'], regra['conclusao'])
                    print(f"  [REGRA DISPARADA] Regra {regra['id']} ativada -> Fato Inferido: {conc_attr} = '{conc_val}'")
                    novas_inferencias = True

    def backward_chaining(self, objetivo_attr):
        """Encadeamento para Trás"""
        print(f"\n--- EXECUTANDO ENCADEMENTO PARA TRÁS (BACKWARD CHAINING) PARA: {objetivo_attr} ---")
        return self._provar_objetivo(objetivo_attr)

    def _provar_objetivo(self, atributo):
        if atributo in self.bc.fatos:
            return True

        regras_candidatas = [r for r in self.bc.regras if r['conclusao'][0] == atributo]
        
        for regra in regras_candidatas:
            regra_valida = True
            for cond_attr, cond_val in regra['condicoes'].items():
                if cond_attr not in self.bc.fatos:
                    resposta = input(f"Informe o valor para '{cond_attr}' (ou digite 'por que'): ")
                    if resposta.lower() in ['por que', 'porque', 'por que?']:
                        self.explicacao.explicar_por_que(cond_attr, regra)
                        resposta = input(f"Informe o valor para '{cond_attr}': ")
                    
                    self.bc.fatos[cond_attr] = resposta

                if self.bc.fatos[cond_attr] != cond_val:
                    regra_valida = False
                    break

            if regra_valida:
                conc_attr, conc_val = regra['conclusao']
                self.bc.fatos[conc_attr] = conc_val
                self.explicacao.registrar_passo(regra['id'], regra['conclusao'])
                return True
        return False


# Execução Demonstrativa
if __name__ == "__main__":
    bc = BaseDeConhecimento()
    exp = ModuloExplicacao()
    engine = EngenhoInferencia(bc, exp)

    # Inserção de Regras na BC
    bc.adicionar_regra("R1", {"Cabo_Conectado": "Sim", "Sinal_DSL": "Desligado"}, ("Problema", "Falha_Provedor"))
    bc.adicionar_regra("R2", {"Cabo_Conectado": "Nao"}, ("Problema", "Cabo_Desconectado"))
    bc.adicionar_regra("R3", {"Cabo_Conectado": "Sim", "Sinal_DSL": "Ligado"}, ("Problema", "Configuracao_Roteador"))

    print("=================================================")
    print("      SHELL GENÉRICO DE SISTEMA ESPECIALISTA     ")
    print("=================================================")

    objetivo = "Problema"
    sucesso = engine.backward_chaining(objetivo)

    if sucesso:
        resultado = bc.fatos.get(objetivo)
        print(f"\n>>> CONCLUSÃO FINAL: {objetivo} = '{resultado}' <<<")
        engine.explicacao.explicar_como(objetivo, resultado)
    else:
        print("\nIncapaz de deduzir conclusões com a base atual.")
