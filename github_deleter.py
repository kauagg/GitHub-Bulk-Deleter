import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import requests
import threading
import os

class GitHubRepoDeleterGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("GitHub Repository Deleter")
        self.root.geometry("900x700")
        self.root.resizable(True, True)
        
        # Variáveis
        self.token = tk.StringVar()
        self.repos = []
        self.filter_text = tk.StringVar()
        self.selected_repos = set()
        
        self.setup_ui()
    
    def setup_ui(self):
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configurar grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(3, weight=1)
        
        # Título
        title_label = ttk.Label(main_frame, text="Gerenciador de Repositórios GitHub", 
                               font=('Arial', 16, 'bold'))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # Seção do Token
        token_frame = ttk.LabelFrame(main_frame, text="Configuração do Token", padding="10")
        token_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        token_frame.columnconfigure(1, weight=1)
        
        ttk.Label(token_frame, text="Token GitHub:").grid(row=0, column=0, sticky=tk.W, padx=(0, 10))
        token_entry = ttk.Entry(token_frame, textvariable=self.token, show="*", width=50)
        token_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(0, 10))
        
        ttk.Button(token_frame, text="Carregar Repositórios", 
                  command=self.load_repos_thread).grid(row=0, column=2)
        
        # Seção de Filtro e Seleção
        filter_frame = ttk.Frame(main_frame)
        filter_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        filter_frame.columnconfigure(1, weight=1)
        
        ttk.Label(filter_frame, text="Filtrar:").grid(row=0, column=0, sticky=tk.W, padx=(0, 10))
        filter_entry = ttk.Entry(filter_frame, textvariable=self.filter_text, width=40)
        filter_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(0, 10))
        filter_entry.bind('<KeyRelease>', self.filter_repos)
        
        ttk.Button(filter_frame, text="Limpar", 
                  command=self.clear_filter).grid(row=0, column=2, padx=(0, 10))
        
        ttk.Button(filter_frame, text="Selecionar Todos", 
                  command=self.select_all).grid(row=0, column=3, padx=(0, 10))
        
        ttk.Button(filter_frame, text="Desselecionar Todos", 
                  command=self.deselect_all).grid(row=0, column=4)
        
        # Lista de repositórios
        list_frame = ttk.LabelFrame(main_frame, text="Repositórios (Clique para selecionar múltiplos)", padding="10")
        list_frame.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        list_frame.columnconfigure(0, weight=1)
        list_frame.rowconfigure(0, weight=1)
        
        # Treeview para lista de repositórios com checkboxes
        columns = ('selected', 'name', 'url', 'created', 'private')
        self.repo_tree = ttk.Treeview(list_frame, columns=columns, show='headings', height=18)
        
        # Definir cabeçalhos
        self.repo_tree.heading('selected', text='✓')
        self.repo_tree.heading('name', text='Nome')
        self.repo_tree.heading('url', text='URL')
        self.repo_tree.heading('created', text='Criado em')
        self.repo_tree.heading('private', text='Privado')
        
        # Definir largura das colunas
        self.repo_tree.column('selected', width=30, anchor='center')
        self.repo_tree.column('name', width=180)
        self.repo_tree.column('url', width=350)
        self.repo_tree.column('created', width=90)
        self.repo_tree.column('private', width=60)
        
        # Scrollbar para a treeview
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.repo_tree.yview)
        self.repo_tree.configure(yscrollcommand=scrollbar.set)
        
        self.repo_tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # Bind clicks para seleção
        self.repo_tree.bind('<Button-1>', self.on_tree_click)
        
        # Frame de botões
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=4, column=0, columnspan=3, pady=10)
        
        self.delete_btn = ttk.Button(button_frame, text="Excluir Selecionados (0)", 
                                   command=self.delete_selected, style='Danger.TButton')
        self.delete_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Button(button_frame, text="Atualizar Lista", 
                  command=self.load_repos_thread).pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Button(button_frame, text="Sair", 
                  command=self.root.quit).pack(side=tk.LEFT)
        
        # Status bar
        self.status_var = tk.StringVar(value="Pronto para começar...")
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, relief=tk.SUNKEN)
        status_bar.grid(row=5, column=0, columnspan=3, sticky=(tk.W, tk.E))
        
        # Contador de selecionados
        self.selected_count_var = tk.StringVar(value="Nenhum repositório selecionado")
        count_label = ttk.Label(main_frame, textvariable=self.selected_count_var)
        count_label.grid(row=6, column=0, columnspan=3, sticky=tk.W)
        
        # Configurar estilo para botão de perigo
        style = ttk.Style()
        style.configure('Danger.TButton', foreground='red')
    
    def set_status(self, message):
        self.status_var.set(message)
        self.root.update_idletasks()
    
    def update_selected_count(self):
        count = len(self.selected_repos)
        self.delete_btn.config(text=f"Excluir Selecionados ({count})")
        if count == 0:
            self.selected_count_var.set("Nenhum repositório selecionado")
        else:
            self.selected_count_var.set(f"{count} repositório(s) selecionado(s) para exclusão")
    
    def load_repos_thread(self):
        if not self.token.get():
            messagebox.showwarning("Token Necessário", "Por favor, insira seu token do GitHub.")
            return
        
        threading.Thread(target=self.load_repos, daemon=True).start()
    
    def load_repos(self):
        self.set_status("Carregando repositórios...")
        self.selected_repos.clear()
        
        try:
            headers = {
                "Authorization": f"token {self.token.get()}",
                "Accept": "application/vnd.github.v3+json"
            }
            
            repos = []
            page = 1
            
            while True:
                response = requests.get(
                    f"https://api.github.com/user/repos?page={page}&per_page=100&sort=created", 
                    headers=headers
                )
                
                if response.status_code != 200:
                    self.root.after(0, lambda: messagebox.showerror(
                        "Erro", 
                        f"Falha ao carregar repositórios: {response.status_code}\n{response.json().get('message', 'Erro desconhecido')}"
                    ))
                    self.set_status("Erro ao carregar repositórios")
                    return
                
                page_repos = response.json()
                if not page_repos:
                    break
                    
                repos.extend(page_repos)
                page += 1
            
            self.repos = repos
            self.root.after(0, self.populate_repo_list)
            self.set_status(f"Carregados {len(repos)} repositórios")
            
        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror("Erro", f"Erro ao carregar repositórios: {str(e)}"))
            self.set_status("Erro ao carregar repositórios")
    
    def populate_repo_list(self, repos=None):
        if repos is None:
            repos = self.repos
        
        # Limpar lista atual
        for item in self.repo_tree.get_children():
            self.repo_tree.delete(item)
        
        # Adicionar repositórios à lista
        for i, repo in enumerate(repos):
            is_selected = repo['name'] in self.selected_repos
            self.repo_tree.insert('', tk.END, iid=str(i), values=(
                '✓' if is_selected else '',
                repo['name'],
                repo['html_url'],
                repo['created_at'][:10],
                'Sim' if repo['private'] else 'Não'
            ))
        
        self.update_selected_count()
    
    def on_tree_click(self, event):
        item = self.repo_tree.identify_row(event.y)
        column = self.repo_tree.identify_column(event.x)
        
        if item and column == '#1':  # Coluna de seleção
            repo_index = int(item)
            if repo_index < len(self.repos):
                repo_name = self.repos[repo_index]['name']
                
                if repo_name in self.selected_repos:
                    self.selected_repos.remove(repo_name)
                else:
                    self.selected_repos.add(repo_name)
                
                # Atualizar visualização
                is_selected = repo_name in self.selected_repos
                self.repo_tree.set(item, 'selected', '✓' if is_selected else '')
                self.update_selected_count()
    
    def select_all(self):
        self.selected_repos.clear()
        for repo in self.repos:
            self.selected_repos.add(repo['name'])
        self.populate_repo_list()
    
    def deselect_all(self):
        self.selected_repos.clear()
        self.populate_repo_list()
    
    def filter_repos(self, event=None):
        filter_text = self.filter_text.get().lower()
        
        if not filter_text:
            self.populate_repo_list(self.repos)
            return
        
        filtered_repos = [repo for repo in self.repos if filter_text in repo['name'].lower()]
        self.populate_repo_list(filtered_repos)
    
    def clear_filter(self):
        self.filter_text.set("")
        self.populate_repo_list(self.repos)
    
    def delete_selected(self):
        if not self.selected_repos:
            messagebox.showwarning("Nada Selecionado", "Por favor, selecione pelo menos um repositório para excluir.")
            return
        
        selected_repos_info = []
        for repo_name in self.selected_repos:
            repo = next((r for r in self.repos if r['name'] == repo_name), None)
            if repo:
                selected_repos_info.append(repo)
        
        # Confirmação
        repo_list = "\n".join([f"• {repo['name']} ({repo['html_url']})" for repo in selected_repos_info])
        
        confirm = messagebox.askyesno(
            "Confirmar Exclusão Múltipla", 
            f"Tem certeza que deseja EXCLUIR PERMANENTEMENTE {len(selected_repos_info)} repositório(s)?\n\n"
            f"Repositórios selecionados:\n{repo_list}\n\n"
            f"⚠️  ESTA AÇÃO NÃO PODE SER DESFEITA!",
            icon='warning'
        )
        
        if confirm:
            threading.Thread(target=self.delete_multiple_repos, args=(selected_repos_info,), daemon=True).start()
    
    def delete_multiple_repos(self, repos_to_delete):
        total = len(repos_to_delete)
        success_count = 0
        failed_repos = []
        
        for i, repo in enumerate(repos_to_delete, 1):
            self.set_status(f"Excluindo {i}/{total}: {repo['name']}...")
            
            try:
                headers = {
                    "Authorization": f"token {self.token.get()}",
                    "Accept": "application/vnd.github.v3+json"
                }
                
                response = requests.delete(
                    f"https://api.github.com/repos/{repo['owner']['login']}/{repo['name']}",
                    headers=headers
                )
                
                if response.status_code == 204:
                    success_count += 1
                    # Remover da lista de selecionados
                    if repo['name'] in self.selected_repos:
                        self.selected_repos.remove(repo['name'])
                else:
                    failed_repos.append(f"{repo['name']} (erro {response.status_code})")
                    
            except Exception as e:
                failed_repos.append(f"{repo['name']} (erro: {str(e)})")
        
        # Mostrar resultado
        self.root.after(0, lambda: self.show_deletion_result(success_count, total, failed_repos))
        
        # Recarregar lista se algum foi excluído com sucesso
        if success_count > 0:
            self.root.after(0, self.load_repos_thread)
    
    def show_deletion_result(self, success_count, total_count, failed_repos):
        message = f"Exclusão concluída!\n\nSucesso: {success_count}/{total_count}"
        
        if failed_repos:
            failed_list = "\n".join(failed_repos)
            message += f"\n\nFalharam:\n{failed_list}"
        
        if failed_repos:
            messagebox.showwarning("Resultado da Exclusão", message)
        else:
            messagebox.showinfo("Sucesso", message)
        
        self.set_status(f"Exclusão concluída: {success_count}/{total_count} repositórios")

def main():
    root = tk.Tk()
    app = GitHubRepoDeleterGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()