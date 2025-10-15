import csv
from datetime import datetime

# Início da classe sobre o imóvel.

class Imovel:
    def __init__(self, tipo):
        self.tipo = tipo
        self.valor_base = 0.0

    def calcular_aluguel(self):
        return self.valor_base

    def gerar_orcamento(self, parcelas_contrato=1):
        contrato = 2000.0
        if parcelas_contrato < 1 or parcelas_contrato > 5:
            raise ValueError('Parcelas devem ser entre 1 e 5.')
        parcela_contrato = contrato / parcelas_contrato

        orcamento = []
        mes = 1
        while mes <= 12:
            if mes <= parcelas_contrato:
                total = self.calcular_aluguel() + parcela_contrato
                parcela = parcela_contrato
            else:
                total = self.calcular_aluguel()
                parcela = 0.0
            orcamento.append({
                'Mês': mes,
                'Aluguel': round(self.calcular_aluguel(), 2),
                'Parcela Contrato': round(parcela, 2),
                'Total': round(total, 2)
            })
            mes += 1
        return orcamento

    def salvar_csv(self, orcamento, nome_arquivo='orcamento.csv'):
        with open(nome_arquivo, mode='w', newline='', encoding='utf-8') as file:
            campos = ['Mês', 'Aluguel', 'Parcela Contrato', 'Total']
            escritor = csv.DictWriter(file, fieldnames=campos)
            escritor.writeheader()
            escritor.writerows(orcamento)
        print('Orçamento salvo em', nome_arquivo)

# Classe dos valores bases.

class Apartamento(Imovel):
    def __init__(self, quartos=1, garagem=False, sem_criancas=False):
        Imovel.__init__(self, 'Apartamento')
        self.valor_base = 700.0
        if quartos == 2:
            self.valor_base += 200.0
        if garagem:
            self.valor_base += 300.0
        self.sem_criancas = sem_criancas

    def calcular_aluguel(self):
        valor = self.valor_base
        if self.sem_criancas:
            valor = valor * 0.95  # 5% de desconto, tive que pesquisar na net.
        return valor

class Casa(Imovel):
    def __init__(self, quartos=1, garagem=False):
        Imovel.__init__(self, 'Casa')
        self.valor_base = 900.0
        if quartos == 2:
            self.valor_base += 250.0
        if garagem:
            self.valor_base += 300.0

class Estudio(Imovel):
    def __init__(self, vagas_estacionamento=0):
        Imovel.__init__(self, 'Estúdio')
        self.valor_base = 1200.0
        if vagas_estacionamento > 0:
            if vagas_estacionamento <= 2:
                self.valor_base += 250.0
            else:
                self.valor_base += 250.0 + (vagas_estacionamento - 2) * 60.0

# Parte que interage com o usuário usando o print.

def obter_tipo_imovel():
    print('Bem-vindo à Imobiliária R.M!')
    print('Escolha o tipo de imóvel:')
    print('1 - Apartamento')
    print('2 - Casa')
    print('3 - Estúdio')
    while True:
        op = input('Digite o número da opção: ').strip()
        if op == '1' or op == '2' or op == '3':
            return int(op)
        print('Opção inválida. Tente novamente.')

# Parte principal do programa.

if __name__ == '__main__':
    tipo = obter_tipo_imovel()

    if tipo == 1:
        quartos = int(input('Número de quartos (1 ou 2)? '))
        garagem = input('Deseja vaga de garagem? (s/n): ').lower() == 's'
        sem_criancas = input('Não possui crianças? (s/n): ').lower() == 's'
        imovel = Apartamento(quartos=quartos, garagem=garagem, sem_criancas=sem_criancas)

    elif tipo == 2:
        quartos = int(input('Número de quartos (1 ou 2)? '))
        garagem = input('Deseja vaga de garagem? (s/n): ').lower() == 's'
        imovel = Casa(quartos=quartos, garagem=garagem)

    else:
        vagas = int(input('Quantas vagas de estacionamento deseja? '))
        imovel = Estudio(vagas_estacionamento=vagas)

    aluguel = imovel.calcular_aluguel()
    print('')
    print('Aluguel mensal: R$', round(aluguel, 2))
    print('Valor do contrato: R$ 2.000,00 (parcelável em até 5x)')

    while True:
        try:
            parcelas = int(input('Em quantas vezes deseja parcelar o contrato (1 a 5)? '))
            if parcelas >= 1 and parcelas <= 5:
                break
            else:
                print('Escolha entre 1 e 5 parcelas.')
        except:
            print('Digite um número válido.')

    orcamento = imovel.gerar_orcamento(parcelas_contrato=parcelas)
    print('')
    print('ORÇAMENTO PARA 12 MESES:')
    print('Mês  Aluguel    Contrato   Total')
    for linha in orcamento:
        print(linha['Mês'], ' R$', '{:.2f}'.format(linha['Aluguel']), ' R$', '{:.2f}'.format(linha['Parcela Contrato']), ' R$', '{:.2f}'.format(linha['Total']))

    salvar = input('\nDeseja salvar o orçamento em CSV? (s/n): ').lower() == 's'
    if salvar:
        nome = 'orcamento_' + imovel.tipo.lower().replace(' ', '_') + '_' + datetime.now().strftime('%Y%m%d_%H%M') + '.csv'
        imovel.salvar_csv(orcamento, nome_arquivo=nome)
