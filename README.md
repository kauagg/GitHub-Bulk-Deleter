# GitHub Repository Bulk Deleter 🗑️

![Python](https://img.shields.io/badge/Python-3.6%2B-blue)
![GitHub](https://img.shields.io/badge/GitHub-API-orange)
![License](https://img.shields.io/badge/License-MIT-green)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux%20%7C%20MacOS-lightgrey)

A powerful desktop application for bulk management and deletion of GitHub repositories through an intuitive graphical interface.

## ✨ Features

- 🖼️ **User-Friendly GUI** - Easy to use Tkinter interface
- 🔍 **Real-time Filtering** - Quickly find repositories
- ☑️ **Multiple Selection** - Select multiple repositories for batch operations
- 🗑️ **Bulk Deletion** - Delete multiple repositories at once
- 🛡️ **Safety Measures** - Multiple confirmation dialogs
- 📊 **Visual Feedback** - Progress tracking and status updates
- 🔐 **Security** - Hidden token input and secure operations
- ⚡ **Async Operations** - Non-blocking interface during operations

## 🚀 Quick Start

### Prerequisites
- Python 3.6 or higher
- GitHub account
- GitHub personal access token

### Installation
1. **Download the application files**
2. **Install dependencies:**
   ```bash
   pip install requests


🛠️ Instalação
Pré-requisitos
Python 3.6 ou superior

Conta no GitHub

Token de acesso pessoal do GitHub

Instalação das Dependências
bash
pip install requests
Configuração do Token GitHub
Acesse GitHub Settings > Tokens

Clique em "Generate new token"

Marque a opção "repo" (acesso completo aos repositórios)

Copie o token gerado

🎮 Como Usar
Execute a aplicação:

bash
python github_repo_deleter.py
Insira seu token GitHub no campo indicado

Clique em "Carregar Repositórios" para buscar seus repositórios

Selecione os repositórios clicando na coluna ✓

Use "Selecionar Todos" para marcar todos

Use "Desselecionar Todos" para limpar a seleção

Filtre repositórios digitando no campo de filtro

Clique em "Excluir Selecionados (X)" onde X é o número de repositórios selecionados

Confirme a exclusão na janela de confirmação

Acompanhe o progresso na barra de status

🏗️ Estrutura do Projeto
text
github-repo-bulk-deleter/
├── github_repo_deleter.py    # Arquivo principal
├── README.md                 # Este arquivo
├── requirements.txt          # Dependências
└── images/                   # Screenshots
    ├── main-screen.png
    └── deletion-confirm.png
📦 Arquivo requirements.txt
txt
requests>=2.25.1
🎯 Funcionalidades Detalhadas
🔄 Carregamento de Repositórios
Busca automática de todos os repositórios do usuário

Suporte a paginação (até 100 repositórios por página)

Ordenação por data de criação

🔍 Sistema de Filtro
Filtro em tempo real por nome do repositório

Não diferencia maiúsculas/minúsculas

Limpeza rápida do filtro

✅ Seleção Múltipla
Seleção individual clicando na coluna de checkmarks

Seleção em lote com "Selecionar Todos"

Contador em tempo real de itens selecionados

Persistência da seleção durante filtragem

🗑️ Exclusão em Lote
Exclusão múltipla em uma única operação

Confirmação detalhada mostrando todos os repositórios

Feedback de progresso durante a exclusão

Relatório final com sucessos e falhas

🛡️ Medidas de Segurança
Token oculto durante digitação

Múltiplas camadas de confirmação

Validação de permissões do token

Tratamento de erros robusto

⚠️ Avisos Importantes

BACKUP SEMPRE: Faça backup dos seus repositórios antes de excluir

IRREVERSÍVEL: A exclusão é permanente e não pode ser desfeita

PERMISSÕES: O token precisa ter escopo repo para exclusão

TESTE: Teste primeiro em repositórios de teste

🐛 Solução de Problemas
Erro de Autenticação

Verifique se o token está correto

Confirme se o token tem permissão repo

Verifique se o token não expirou

Repositórios Não Aparecem
Confirme que o usuário tem repositórios

Verifique a conexão com a internet

Confirme as permissões do token

Erro na Exclusão
Verifique se você é owner do repositório

Confirme que o repositório existe

Verifique limites de rate limit do GitHub

🤝 Contribuindo
Fork o projeto

Crie uma branch para sua feature (git checkout -b feature/AmazingFeature)

Commit suas mudanças (git commit -m 'Add some AmazingFeature')

Push para a branch (git push origin feature/AmazingFeature)

Abra um Pull Request

📄 Licença
Distribuído sob licença MIT. Veja LICENSE para mais informações.

👨‍💻 Autor
Desenvolvedor FullStack Kauã - kauagg

🙏 Agradecimentos
GitHub REST API

Tkinter

Requests Library

⚠️ AVISO: Use com responsabilidade. A exclusão de repositórios é permanente!**

📝 Exemplo de Uso Rápido
bash
# Clone o repositório
git clone https://github.com/seu-usuario/github-repo-bulk-deleter.git

# Entre no diretório
cd github-repo-bulk-deleter

# Instale as dependências
pip install -r requirements.txt

# Execute a aplicação
python github_repo_deleter.py
⭐ Se este projeto foi útil, deixe uma estrela no repositório!
