# Sistema Bancário em POO

## Sobre o Projeto
Este projeto é uma simulação de um sistema bancário implementado utilizando os princípios da Programação Orientada a Objetos (POO). Ele permite a criação de usuários e contas bancárias, além de realizar operações básicas como depósitos, saques e exibição de extratos.

## Funcionalidades
- **Criação de Usuários**: Permite adicionar novos usuários ao sistema bancário.
- **Criação de Contas**: Permite abrir novas contas bancárias para usuários existentes.
- **Depósitos**: Permite realizar depósitos em contas existentes.
- **Saques**: Permite realizar saques de contas, respeitando o saldo e limites estabelecidos.
- **Extratos**: Exibe o histórico de transações e o saldo atual da conta.
- **Limite de Transações Diárias**: Limita o número de transações diárias para cada conta a 10.
- **Persistência de Dados**: Armazena informações das contas em um arquivo de texto para manter os dados entre execuções.
- **Mensagens Informativas**: Exibe mensagens informativas quando não há contas cadastradas ou ao tentar criar uma conta existente.

## Como Usar
Para utilizar o sistema, siga os passos abaixo:
1. Clone o repositório para sua máquina local.
2. Execute o arquivo principal do sistema.
3. Siga as instruções no menu interativo para realizar operações bancárias.

## Menu de Operações
- **d** - Realizar depósito
- **s** - Realizar saque
- **e** - Exibir extrato
- **nu** - Novo usuário
- **nc** - Nova conta para usuário existente
- **lc** - Listar contas
- **q** - Sair

## Tecnologias Utilizadas
- Python
- POO

## Contribuições
Contribuições são sempre bem-vindas! Para contribuir, por favor:
1. Faça um fork do projeto.
2. Crie uma nova branch para suas modificações (`git checkout -b feature/novaFeature`).
3. Faça commit das suas alterações (`git commit -m 'Adicionando uma nova feature'`).
4. Faça push para a branch (`git push origin feature/novaFeature`).
5. Abra um Pull Request.

Link do Projeto: https://github.com/thiagoaquinodasilva/desafio-dio-banco-python

## Atualizações Recentes
### Versão 2.0
- **Limite de Transações Diárias**: Implementado um limite de 10 transações diárias por conta. Mensagem informativa é exibida ao tentar exceder este limite.
- **Persistência de Dados**: Adicionado um arquivo de texto (`contas.txt`) para armazenar informações das contas. As contas são carregadas automaticamente ao iniciar o sistema e novas contas são registradas no arquivo.
- **Mensagens Informativas**: Adicionada uma mensagem informativa quando não há contas cadastradas ao listar contas.

## Imagem UML do Projeto
![UML - Trilha Python - desafio banco](https://github.com/thiagoaquinodasilva/desafio-dio-banco-python/assets/92541911/4ced8fab-ea4e-4936-ac23-8a4cbe798240)

---

Desenvolvido com ❤️ por Thiago Aquino.
