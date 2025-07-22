"""
🎯 GERADOR DE PERGUNTAS E RESPOSTAS DE TRIATHLON
===============================================
OBJETIVO: Usuário fornece TEMA → Sistema gera PERGUNTAS + arquivo TXT com RESPOSTAS

FLUXO SIMPLES:
1. Usuário fornece tema (ex: "penalidades")
2. Sistema busca contexto relevante no PDF
3. IA gera perguntas sobre o tema
4. IA gera respostas para as perguntas
5. Sistema salva arquivo TXT com perguntas + respostas
"""

import os
import json
import sys
from pathlib import Path
import numpy as np
import faiss
from datetime import datetime
from ollama import chat
import ollama

# Configuração simples
EMBEDDINGS_PATH = "../embeddings/embeddings.json"
QUESTIONS_OUTPUT = "../perguntas_geradas"
EMBEDDING_MODEL = "nomic-embed-text:latest"
CHAT_MODEL = "phi3.5:latest"

def calculate_cosine_similarity(vec1: np.ndarray, vec2: np.ndarray) -> float:
    """Calcula similaridade entre vetores."""
    dot_product = np.dot(vec1, vec2)
    norm_vec1 = np.linalg.norm(vec1)
    norm_vec2 = np.linalg.norm(vec2)
    
    if norm_vec1 == 0 or norm_vec2 == 0:
        return 0.0
        
    return dot_product / (norm_vec1 * norm_vec2)

def generate_embedding(text: str) -> np.ndarray:
    """Gera embedding via Ollama."""
    try:
        response = ollama.embeddings(model=EMBEDDING_MODEL, prompt=text)
        return np.array(response['embedding'], dtype='float32')
    except Exception as e:
        print(f"❌ Erro ao gerar embedding: {e}")
        return None

def load_embeddings():
    """Carrega embeddings do arquivo JSON."""
    if not os.path.exists(EMBEDDINGS_PATH):
        print(f"❌ Arquivo de embeddings não encontrado: {EMBEDDINGS_PATH}")
        print("💡 Execute primeiro: python generate2_simples.py")
        return None, None, None
    
    with open(EMBEDDINGS_PATH, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    vectors = np.array([item['embedding'] for item in data], dtype='float32')
    texts = []
    
    for item in data:
        if item['type'] == 'table_row':
            display_text = f"[TABELA] {item.get('contextual_content', item['content'])}"
        else:
            display_text = item.get('contextual_content', item['content'])
        texts.append(display_text)
    
    # Criar índice FAISS
    index = faiss.IndexFlatL2(vectors.shape[1])
    index.add(vectors)
    
    print(f"✅ Embeddings carregados: {len(data)} itens")
    return data, index, texts

def search_context(tema: str, data, index, texts, num_results=7):
    """Busca contexto relevante para o tema."""
    query_vector = generate_embedding(tema)
    if query_vector is None:
        return ""
    
    # Buscar similares
    query_vector_2d = query_vector.reshape(1, -1)
    distances, indices = index.search(query_vector_2d, num_results)
    
    # Montar contexto
    context_parts = []
    for i in range(len(indices[0])):
        idx = indices[0][i]
        similarity = calculate_cosine_similarity(query_vector, np.array(data[idx]['embedding']))
        
        if similarity > 0.3:  # Threshold mínimo
            context_parts.append(texts[idx])
    
    return "\n\n".join(context_parts)

def gerar_perguntas(tema: str, context: str):
    """Gera perguntas sobre o tema usando o contexto."""
    if not context.strip():
        print("❌ Nenhum contexto relevante encontrado no PDF")
        return None
    
    prompt = f"""Você é um especialista em triathlon. 

TAREFA: Gere 5 perguntas ESPECÍFICAS sobre "{tema}" baseado no texto do regulamento abaixo.

INSTRUÇÕES:
- Perguntas devem ser precisas e técnicas
- Use terminologia do triathlon
- Cada pergunta deve poder ser respondida com o texto fornecido
- Numere as perguntas (1., 2., 3., etc.)
- Seja específico sobre regras, penalidades, equipamentos, etc.

TEXTO DO REGULAMENTO:
{context}

Gere 5 perguntas em português sobre {tema}:"""

    try:
        print(f"🔄 Gerando perguntas sobre '{tema}'...")
        
        stream = ollama.chat(
            model=CHAT_MODEL,
            messages=[{'role': 'user', 'content': prompt}],
            stream=True,
        )

        print(f"\n📝 PERGUNTAS GERADAS SOBRE '{tema.upper()}':")
        print("=" * 80)
        
        response = ""
        for chunk in stream:
            content = chunk['message']['content']
            response += content
            print(content, end='', flush=True)
        
        print("\n" + "=" * 80)
        return response
        
    except Exception as e:
        print(f"❌ Erro ao gerar perguntas: {e}")
        return None

def gerar_respostas(perguntas: str, context: str, tema: str):
    """Gera respostas para as perguntas."""
    prompt = f"""Você é um especialista em triathlon.

TAREFA: Para cada pergunta abaixo, forneça uma resposta DETALHADA baseada APENAS no texto do regulamento fornecido.

INSTRUÇÕES:
- Use apenas informações do texto fornecido
- Seja preciso e técnico
- Formato: PERGUNTA: [pergunta]\\nRESPOSTA: [resposta detalhada]\\n\\n
- Se não houver informação suficiente, diga "Informação não encontrada no regulamento fornecido"

PERGUNTAS:
{perguntas}

TEXTO DO REGULAMENTO:
{context}

Forneça respostas detalhadas:"""

    try:
        print(f"\n🔄 Gerando respostas...")
        
        response = ollama.chat(
            model=CHAT_MODEL,
            messages=[{'role': 'user', 'content': prompt}],
            stream=False,
        )
        
        print("✅ Respostas geradas!")
        return response['message']['content']
        
    except Exception as e:
        print(f"❌ Erro ao gerar respostas: {e}")
        return None

def salvar_arquivo(tema: str, perguntas: str, respostas: str, context: str):
    """Salva arquivo TXT com perguntas e respostas."""
    # Criar diretório se não existir
    output_dir = Path(QUESTIONS_OUTPUT)
    output_dir.mkdir(exist_ok=True)
    
    # Nome do arquivo com timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"perguntas_respostas_{tema.replace(' ', '_')}_{timestamp}.txt"
    filepath = output_dir / filename
    
    # Conteúdo do arquivo
    content = f"""================================================================================
PERGUNTAS E RESPOSTAS - TRIATHLON
TEMA: {tema.upper()}
Gerado em: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}
================================================================================

📝 PERGUNTAS GERADAS:
--------------------------------------------------
{perguntas}

💡 RESPOSTAS DETALHADAS:
--------------------------------------------------
{respostas}

📄 CONTEXTO UTILIZADO (TRECHOS DO REGULAMENTO):
--------------------------------------------------
{context[:2000]}{'...' if len(context) > 2000 else ''}

================================================================================
Sistema de Geração de Perguntas de Triathlon
Baseado no Regulamento da World Triathlon 2024
================================================================================"""
    
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"\n✅ Arquivo salvo: {filepath}")
        print("📋 O arquivo contém:")
        print("   • Perguntas geradas")
        print("   • Respostas detalhadas")
        print("   • Contexto do regulamento usado")
        
        return str(filepath)
        
    except Exception as e:
        print(f"❌ Erro ao salvar arquivo: {e}")
        return None

def main():
    """Função principal."""
    print("\n🏊‍♂️🚴‍♂️🏃‍♂️ GERADOR DE PERGUNTAS DE TRIATHLON 🏃‍♂️🚴‍♂️🏊‍♂️")
    print("Digite um TEMA para gerar perguntas + arquivo TXT com respostas")
    print("Digite 'sair' para encerrar\n")
    
    print("💡 Exemplos de temas:")
    print("   • penalidades     • equipamentos    • natação")
    print("   • ciclismo        • corrida         • transições")
    print("   • wetsuit         • drafting        • desqualificação")
    
    # Carregar embeddings
    print(f"\n🔄 Carregando embeddings...")
    data, index, texts = load_embeddings()
    if not data:
        return
    
    while True:
        tema = input(f"\n🔍 Digite o TEMA (ou 'sair'): ").strip()
        
        if tema.lower() == 'sair':
            print("👋 Encerrando. Até mais!")
            break
        
        if not tema:
            print("❌ Digite um tema válido")
            continue
        
        # 1. Buscar contexto
        print(f"🔍 Buscando contexto sobre '{tema}'...")
        context = search_context(tema, data, index, texts)
        
        if not context:
            print(f"❌ Nenhum conteúdo encontrado sobre '{tema}'")
            continue
        
        print(f"✅ Contexto encontrado ({len(context)} caracteres)")
        
        # 2. Gerar perguntas
        perguntas = gerar_perguntas(tema, context)
        if not perguntas:
            continue
        
        # 3. Gerar respostas
        respostas = gerar_respostas(perguntas, context, tema)
        if not respostas:
            continue
        
        # 4. Salvar arquivo
        arquivo = salvar_arquivo(tema, perguntas, respostas, context)
        
        if arquivo:
            print(f"\n🎉 SUCESSO! Arquivo completo gerado: {arquivo}")

if __name__ == "__main__":
    main()
