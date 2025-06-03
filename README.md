# 🏦 Sistema Bancário em Python com POO

Este projeto é um sistema bancário simples desenvolvido em Python, com foco no uso de **Programação Orientada a Objetos (POO)**. Ele simula as principais operações de um banco, como criação de contas, saques, depósitos e extrato de transações.

## ✅ Funcionalidades

- Cadastro de clientes (com CPF, nome, data de nascimento e endereço)
- Criação de contas bancárias vinculadas a clientes
- Depósito e saque com validações
- Histórico de transações por conta
- Limite de saques por conta corrente
- Exibição de extrato com saldo e movimentações
- Interface via terminal (CLI)

## 🧱 Estrutura do Projeto

- `Cliente`, `PessoaFisica` — Representam os usuários do sistema
- `Conta`, `ContaCorrente` — Modelam contas bancárias com operações
- `Transacao`, `Saque`, `Deposito` — Representam ações realizadas na conta
- `Historico` — Registra todas as movimentações
- Funções auxiliares para criar e listar clientes e contas

