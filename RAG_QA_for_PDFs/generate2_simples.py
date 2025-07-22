"""
🔍 GERADOR DE EMBEDDINGS (SIMPLIFICADO)
======================================
Gera embeddings do Markdown para busca
"""

import json
import re
from pathlib import Path
import tiktoken
import ollama

# Configuração
MARKDOWN_FILE = "../mdPath/pdf2.md"
OUTPUT_FILE = "../embeddings/embeddings.json"
EMBEDDING_MODEL = "nomic-embed-text:latest"
CHUNK_SIZE = 512
OVERLAP = 128

def test_ollama():
    """Testa conexão com Ollama."""
    try:
        ollama.embeddings(model=EMBEDDING_MODEL, prompt="teste")
        print("✅ Ollama conectado")
        return True
    except Exception as e:
        print(f"❌ Erro Ollama: {e}")
        print(f"💡 Execute: ollama pull {EMBEDDING_MODEL}")
        return False

def chunk_text(text):
    """Divide texto em chunks."""
    tokenizer = tiktoken.get_encoding("cl100k_base")
    
    # Dividir por seções (##)
    sections = re.split(r'\n## ', text)
    chunks = []
    
    for i, section in enumerate(sections):
        if not section.strip():
            continue
            
        # Título da seção
        lines = section.split('\n')
        title = lines[0].replace('## ', '').strip()
        content = '\n'.join(lines[1:]).strip()
        
        if not content:
            continue
        
        # Dividir seção em parágrafos
        paragraphs = [p.strip() for p in content.split('\n\n') if p.strip()]
        
        for j, paragraph in enumerate(paragraphs):
            # Verificar se é tabela
            is_table = '|' in paragraph and paragraph.count('|') > 2
            
            # Contexto completo
            if is_table:
                contextual_content = f"Seção: {title}. Tabela: {paragraph}"
                chunk_type = "table_row"
            else:
                contextual_content = f"Seção: {title}. {paragraph}"
                chunk_type = "text_chunk"
            
            chunks.append({
                'id': f"chunk_{i}_{j}",
                'content': paragraph,
                'contextual_content': contextual_content,
                'type': chunk_type,
                'section_title': title,
                'embedding': None  # Será preenchido depois
            })
    
    print(f"✅ Texto dividido em {len(chunks)} chunks")
    return chunks

def generate_embeddings(chunks):
    """Gera embeddings para os chunks."""
    print("🔄 Gerando embeddings...")
    
    for i, chunk in enumerate(chunks):
        try:
            response = ollama.embeddings(
                model=EMBEDDING_MODEL,
                prompt=chunk['contextual_content']
            )
            chunk['embedding'] = response['embedding']
            
            if (i + 1) % 50 == 0:
                print(f"   Processados: {i + 1}/{len(chunks)}")
                
        except Exception as e:
            print(f"❌ Erro no chunk {i}: {e}")
            return None
    
    print("✅ Embeddings gerados")
    return chunks

def main():
    """Função principal."""
    print("🔍 GERADOR DE EMBEDDINGS")
    print("=" * 40)
    
    # Verificar arquivo
    markdown_path = Path(MARKDOWN_FILE)
    if not markdown_path.exists():
        print(f"❌ Arquivo não encontrado: {markdown_path}")
        print("💡 Execute primeiro: python doclingpdf_simples.py")
        return
    
    # Testar Ollama
    if not test_ollama():
        return
    
    # Carregar e processar texto
    print(f"📖 Carregando: {markdown_path}")
    with open(markdown_path, 'r', encoding='utf-8') as f:
        text = f.read()
    
    print(f"📊 Tamanho: {len(text)} caracteres")
    
    # Dividir em chunks
    chunks = chunk_text(text)
    
    # Gerar embeddings
    chunks_with_embeddings = generate_embeddings(chunks)
    if not chunks_with_embeddings:
        return
    
    # Salvar
    output_path = Path(OUTPUT_FILE)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(chunks_with_embeddings, f, ensure_ascii=False, indent=2)
    
    print(f"✅ Embeddings salvos: {output_path}")
    print(f"📊 Total de embeddings: {len(chunks_with_embeddings)}")
    print("\n🎉 Pronto!")
    print("💡 Próximo passo: python ollama_ask2_simples.py")

if __name__ == "__main__":
    main()
