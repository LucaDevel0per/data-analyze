import os
import sys
from pathlib import Path

def get_size(path):
    """Retorna o tamanho de um arquivo ou pasta em bytes."""
    if os.path.isfile(path):
        return os.path.getsize(path)
    elif os.path.isdir(path):
        total_size = 0
        for dirpath, dirnames, filenames in os.walk(path):
            for f in filenames:
                fp = os.path.join(dirpath, f)
                # Pula links simbólicos quebrados
                if not os.path.exists(fp):
                    continue
                try:
                    total_size += os.path.getsize(fp)
                except OSError:
                    # Ignora arquivos que não podem ser acessados
                    pass
        return total_size
    return 0

def format_size(size_bytes):
    """Formata o tamanho em bytes para um formato legível (KB, MB, GB)."""
    if size_bytes == 0:
        return "0B"
    size_name = ("B", "KB", "MB", "GB", "TB")
    i = 0
    while size_bytes >= 1024 and i < len(size_name) - 1:
        size_bytes /= 1024
        i += 1
    return f"{size_bytes:.2f} {size_name[i]}"

def main():
    """Função principal para analisar o armazenamento."""
    # Usa o caminho fornecido como argumento, ou o diretório home do usuário como padrão
    if len(sys.argv) > 1:
        path_to_scan = sys.argv[1]
    else:
        path_to_scan = str(Path.home())

    print(f"Analisando o diretório: {path_to_scan}")
    print("Isso pode levar alguns minutos...")

    if not os.path.isdir(path_to_scan):
        print(f"Erro: O caminho '{path_to_scan}' não é um diretório válido.")
        return

    items = []
    try:
        for item_name in os.listdir(path_to_scan):
            full_path = os.path.join(path_to_scan, item_name)
            try:
                size = get_size(full_path)
                if size > 0:
                    items.append((size, full_path))
            except PermissionError:
                print(f"Permissão negada para acessar: {full_path}")
                continue
    except PermissionError:
        print(f"Não foi possível ler o diretório: {path_to_scan}. Tente executar como administrador.")
        return


    # Ordena os itens por tamanho em ordem decrescente
    items.sort(key=lambda x: x[0], reverse=True)

    print("\n--- Top 10 Itens Mais Pesados ---")
    for size, path in items[:10]:
        print(f"{format_size(size):<10} | {path}")

if __name__ == "__main__":
    main()
