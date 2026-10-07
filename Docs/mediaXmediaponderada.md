A diferença entre a **Média Simples** e a **Média Ponderada (Taxa Ponderada)** é a unidade que você está medindo: se você está olhando para as **Instituições** ou para os **Alunos**.

---

### A Demonstração Matemática

Se cada Instituto Federal $i$ tem uma taxa de conclusão $T_i = \frac{\text{Concluintes}_i}{\text{Ingressantes}_i}$ e nós ponderamos cada IF pelo seu número de alunos ingressantes ($w_i = \text{Ingressantes}_i$):

$$\text{Média Ponderada} = \frac{\sum (w_i \cdot T_i)}{\sum w_i} = \frac{\sum \left(\text{Ingressantes}_i \cdot \frac{\text{Concluintes}_i}{\text{Ingressantes}_i}\right)}{\sum \text{Ingressantes}_i} = \frac{\sum \text{Concluintes}_i}{\sum \text{Ingressantes}_i} = \textbf{Taxa Global}$$

Ou seja: **a soma de todos os concluintes dividida pela soma de todos os ingressantes é exatamente a média ponderada das taxas de cada IF.**

---

### Um Exemplo Prático e Intuitivo:

Imagine uma região com apenas **dois Institutos Federais**:

* **IF Pequeno (ex: interior):** Teve **10** ingressantes e **9** concluintes $\rightarrow$ **Taxa = 90%**
* **IF Gigante (ex: capital):** Teve **1.000** ingressantes e **500** concluintes $\rightarrow$ **Taxa = 50%**

#### 1. Média Simples (foco na Instituição):
$$\frac{90\% + 50\%}{2} = \mathbf{70\%}$$
> Trata os dois IFs com o mesmo peso. Ela responde à pergunta: *"Em média, como se comportam as instituições?"*  
> *(Porém, dá uma falsa impressão de que a maioria dos alunos se formou).*

#### 2. Média Ponderada / Taxa Ponderada (foco no Aluno):
$$\text{Total Concluintes} = 9 + 500 = 509$$
$$\text{Total Ingressantes} = 10 + 1.000 = 1.010$$
$$\text{Taxa Ponderada} = \frac{509}{1.010} \times 100 = \mathbf{50,4\%}$$
> Leva em consideração onde os alunos realmente estão. Ela responde à pergunta: *"De cada 100 alunos que entraram nessa rede, quantos se formaram?"*

---

### Como isso se aplica aos resultados da Região no TCC?

Veja a tabela que geramos na função para a **Região Sul**:

* **Média Simples dos IFs do Sul:** **59,98%** (a média aritmética dos 6 IFs da região Sul, tratando cada reitoria com peso igual).
* **Taxa Ponderada da Região Sul:** **78,52%** (a realidade dos milhões de alunos do Sul).

**Por que essa diferença de quase 20 pontos percentuais?**  
Porque os maiores Institutos Federais do Sul (os que concentram a esmagadora maioria das vagas e matrículas) tiveram taxas de sucesso muito altas, "puxando" o resultado global da região para cima!

Apresentar **ambas** na monografia mostra maturidade estatística:
* A **Média e o Desvio Padrão** revelam a *dispersão entre as escolas*;
* A **Taxa Ponderada** revela o *retrato real da população discente*.