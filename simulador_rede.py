import networkx as nx
import ipaddress

#classe para representar os hosts

class Host:
    def __init__(self,nome,ip):
        self.nome = nome
        self.ip = ip

#classe para representar os roteadores

class Roteador:
    def __init__(self,nome,ip_interfaces):
        self.nome = nome
        self.ip_interfaces = ip_interfaces
        self.tabela_roteamento = []

    def adicionar_rota(self,destino,mascara,proximo_salto):
        self.tabela_roteamento.append({
            "destino": destino,
            "mascara":mascara,
            "proximo_salto":proximo_salto
        })

#funcao para encontrar rota

def encontrar_proximo_salto(roteador, ip_destino_final):
    melhor_rota = None
    maior_prefixo = -1
    
    ip_destino_obj = ipaddress.ip_address(ip_destino_final)

    for rota in roteador.tabela_roteamento:
        rede = ipaddress.ip_network(f"{rota['destino']}{rota['mascara']}", strict=False)
        
        if ip_destino_obj in rede:
            if rede.prefixlen > maior_prefixo:
                maior_prefixo = rede.prefixlen
                melhor_rota = rota
    if melhor_rota:
        return melhor_rota['proximo_salto']
    return None

#funcao para simular o traceroute

def xtraceroute(G, nome_origem, ip_destino, verbose=True):
   
    try:
        roteador_atual_nome = list(G.neighbors(nome_origem))[0]
    except (nx.NetworkXError, IndexError):
        if verbose: print(f"Erro: Origem '{nome_origem}' inválida ou não conectada a um roteador.")
        return False

    caminho = [roteador_atual_nome]
    ip_destino_obj = ipaddress.ip_address(ip_destino)
    
    for _ in range(20):
        roteador_obj = G.nodes[roteador_atual_nome]['device']
        
        if 'gateway_local' in roteador_obj.ip_interfaces:
            rede_local = ipaddress.ip_network(f"{roteador_obj.ip_interfaces['gateway_local']}/27", strict=False)
            if ip_destino_obj in rede_local:
                break 

        proximo_salto_ip = encontrar_proximo_salto(roteador_obj, ip_destino)
        
        if not proximo_salto_ip:
            if verbose: print(f"Erro: Rota não encontrada em '{roteador_atual_nome}'. Pacote descartado.")
            return False

        proximo_roteador_nome = None
        for vizinho in G.neighbors(roteador_atual_nome):
            dispositivo_vizinho = G.nodes[vizinho]['device']
            if isinstance(dispositivo_vizinho, Roteador):
                if proximo_salto_ip in dispositivo_vizinho.ip_interfaces.values():
                    proximo_roteador_nome = vizinho
                    break
        
        if not proximo_roteador_nome:
            if verbose: print(f"Erro: Não foi possível encontrar o dispositivo com o IP de próximo salto {proximo_salto_ip}")
            return False
        
        caminho.append(proximo_roteador_nome)
        roteador_atual_nome = proximo_roteador_nome
    else:
        if verbose: print("Erro: Limite de saltos atingido, provável loop de roteamento.")
        return False

    if verbose:
        print("Caminho completo:", " -> ".join(caminho))
    
    return True

#funcao xping

def xping(G, nome_origem, ip_destino):
    """
    Simula o ping, testando apenas a conectividade.
    """
    print(f"--- Iniciando xping de {nome_origem} para {ip_destino} ---")

    is_reachable = xtraceroute(G, nome_origem, ip_destino, verbose=False)
    
    if is_reachable:
        print(f"Resultado: Host {ip_destino} é alcançável a partir de {nome_origem}.")
    else:
        print(f"Resultado: Host {ip_destino} é inalcançável a partir de {nome_origem}.")
    
    print("--- Fim do xping ---")

 #criando os hosts

h1 = Host(nome = 'H1' , ip = '192.168.0.2')
h2 = Host(nome = 'H2' , ip = '192.168.0.3')
h3 = Host(nome = 'H3' , ip = '192.168.0.34')
h4 = Host(nome = 'H4' , ip = '192.168.0.35')
h5 = Host(nome = 'H5' , ip = '192.168.0.66')
h6 = Host(nome = 'H6' , ip = '192.168.0.67')
h7 = Host(nome = 'H7' , ip = '192.168.0.98')
h8 = Host(nome = 'H8' , ip = '192.168.0.99')



#criando os roteadores 

#C1 
c1 = Roteador(nome='C1', ip_interfaces={'para_a1': '192.168.0.129', 'para_a2': '192.168.0.133'})
c1.adicionar_rota('192.168.0.0', '/27', '192.168.0.130')
c1.adicionar_rota('192.168.0.32', '/27', '192.168.0.130')
c1.adicionar_rota('192.168.0.64', '/27', '192.168.0.134')
c1.adicionar_rota('192.168.0.96', '/27', '192.168.0.134')

#A1
a1 = Roteador(
    nome='A1', 
    ip_interfaces={
        'para_c1': '192.168.0.130',
        'para_e1': '192.168.0.137', 
        'para_e2': '192.168.0.141'
})
a1.adicionar_rota('192.168.0.0', '/27', '192.168.0.138')
a1.adicionar_rota('192.168.0.32', '/27', '192.168.0.142')
a1.adicionar_rota('0.0.0.0', '/0', '192.168.0.129')

#A2
a2 = Roteador(
    nome='A2',
    ip_interfaces={
        'para_c1': '192.168.0.134', 
        'para_e3': '192.168.0.145', 
        'para_e4': '192.168.0.149'
    }
)
a2.adicionar_rota('192.168.0.64', '/27', '192.168.0.146')
a2.adicionar_rota('192.168.0.96', '/27', '192.168.0.150')
a2.adicionar_rota('0.0.0.0', '/0', '192.168.0.133')

#E1-E4
e1 = Roteador(nome='E1', ip_interfaces={'gateway_local': '192.168.0.1', 'para_a1': '192.168.0.138'})
e1.adicionar_rota('0.0.0.0', '/0', '192.168.0.137')

e2 = Roteador(nome='E2', ip_interfaces={'gateway_local': '192.168.0.33', 'para_a1': '192.168.0.142'})
e2.adicionar_rota('0.0.0.0', '/0', '192.168.0.141')

e3 = Roteador(nome='E3', ip_interfaces={'gateway_local': '192.168.0.65', 'para_a2': '192.168.0.146'})
e3.adicionar_rota('0.0.0.0', '/0', '192.168.0.145')

e4 = Roteador(nome='E4', ip_interfaces={'gateway_local': '192.168.0.97', 'para_a2': '192.168.0.150'})
e4.adicionar_rota('0.0.0.0', '/0', '192.168.0.149')

#criando o grafo

todos_dispositivos = [c1, a1, a2, e1, e2, e3, e4, h1, h2, h3, h4, h5, h6, h7, h8]

G = nx.Graph()

for dispositivo in todos_dispositivos:
    G.add_node(dispositivo.nome, device=dispositivo)

G.add_edge('C1', 'A1')
G.add_edge('C1', 'A2')

G.add_edge('A1', 'E1')
G.add_edge('A1', 'E2')

G.add_edge('A2', 'E3')
G.add_edge('A2', 'E4')

G.add_edge('E1', 'H1')
G.add_edge('E1', 'H2')

G.add_edge('E2', 'H3')
G.add_edge('E2', 'H4')

G.add_edge('E3', 'H5')
G.add_edge('E3', 'H6')

G.add_edge('E4', 'H7')
G.add_edge('E4', 'H8')

#bloco principal de execucao

if __name__ == "__main__":

    #instruções
    print("Comandos disponíveis:")
    print("  xtraceroute [host_origem] [ip_destino]")
    print("  xping [host_origem] [ip_destino]")
    print("  sair")
    print("-" * 40)

    while True:
        comando_completo = input("Digite o comando > ")

        if comando_completo.lower() == 'sair':
            print("Encerrando o simulador...")
            break 

        partes = comando_completo.split()

        if len(partes) != 3:
            print("Comando inválido. Formato esperado: [comando] [origem] [destino]")
            continue 

        comando, origem, destino = partes

        if comando.lower() == 'xping':
            xping(G, origem, destino)
        elif comando.lower() == 'xtraceroute':
            xtraceroute(G, origem, destino)
        else:
            print(f"Comando '{comando}' desconhecido. Use xping ou xtraceroute.")
        
        print() 