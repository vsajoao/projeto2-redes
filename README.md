# Projeto 2: Simulação de Rede Hierárquica

Este repositório contém o código-fonte para o Projeto 2 da disciplina de Redes de Computadores, da Universidade de Brasília, ministrada pela Profa. Priscila Solís Barreto.

[cite_start]O objetivo do projeto é aprofundar os conceitos das camadas de rede e de enlace através da aplicação prática de projeto e simulação de redes[cite: 26]. Para isso, foi projetada uma rede hierárquica de data center, com um plano de endereçamento IP utilizando VLSM e tabelas de roteamento estático. Em seguida, um simulador em Python foi desenvolvido para validar o projeto, permitindo testar a conectividade e rastrear rotas entre os dispositivos da rede.

## Principais Funcionalidades

* Modelagem de uma rede hierárquica (Core, Agregação, Borda) utilizando a biblioteca `networkx`.
* Simulação de conectividade ponta-a-ponta com o comando customizado `xping`.
* Rastreamento de rota entre hosts com o comando customizado `xtraceroute`, demonstrando o caminho percorrido pelos pacotes.
* Implementação baseada em tabelas de roteamento estático predefinidas para cada um dos 7 roteadores da topologia.

## Tecnologias Utilizadas

* **Linguagem:** Python 3
* **Bibliotecas:** `networkx`, `ipaddress`
* **Ambiente:** `venv` (Ambiente Virtual Python)

## Como Executar

Para executar o simulador em um ambiente Linux:

1.  **Clone o repositório:**
    ```bash
    git clone [https://github.com/vsajoao/projeto2-redes.git](https://github.com/vsajoao/projeto2-redes.git)
    cd projeto2-redes
    ```

2.  **Crie e ative o ambiente virtual:**
    ```bash
    python3 -m venv env
    source env/bin/activate
    ```

3.  **Instale as dependências:**
    ```bash
    pip install networkx
    ```

4.  **Execute o simulador:**
    ```bash
    python3 simulador_rede.py
    ```

## Exemplos de Uso

Após iniciar o programa, você pode usar os seguintes comandos:

```text
Digite o comando > xtraceroute H1 192.168.0.99
--- Iniciando xtraceroute de H1 para 192.168.0.99 ---
Caminho completo: E1 -> A1 -> C1 -> A2 -> E4
--- Fim do xtraceroute ---

Digite o comando > xping H7 192.168.0.3
--- Iniciando xping de H7 para 192.168.0.3 ---
Resultado: Host 192.168.0.3 é alcançável a partir de H7.
--- Fim do xping ---

Digite o comando > sair
Encerrando o simulador...
