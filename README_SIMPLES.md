# 🏊‍♂️🚴‍♂️🏃‍♂️ GERADOR DE PERGUNTAS DE TRIATHLON

**OBJETIVO:** Usuário fornece TEMA → Sistema gera PERGUNTAS + arquivo TXT com RESPOSTAS

## 🎯 O QUE FAZ

1. **INPUT:** Usuário digita um tema (ex: "penalidades")
2. **PROCESSAMENTO:** Sistema busca conteúdo relevante no PDF de triathlon
3. **OUTPUT:** 
   - Perguntas específicas sobre o tema
   - Arquivo TXT com perguntas + respostas detalhadas

## 🚀 COMO USAR

### 1. Instalar Dependências
```bash
pip install ollama numpy faiss-cpu tiktoken docling
```

### 2. Instalar Ollama
- Baixar: https://ollama.ai/download
- Instalar modelos:
```bash
ollama pull nomic-embed-text:latest
ollama pull phi3.5:latest
```

### 3. Preparar PDF
- Colocar PDF do triathlon na pasta `pdfPath/`

### 4. Executar Sequência
```bash
# 1. Converter PDF para Markdown
python RAG_QA_for_PDFs/doclingpdf_simples.py

# 2. Gerar embeddings
python RAG_QA_for_PDFs/generate2_simples.py

# 3. Usar o gerador
python RAG_QA_for_PDFs/ollama_ask2_simples.py
```

## 📁 ESTRUTURA

```
testepapai/
├── pdfPath/                    # Colocar PDF aqui
├── mdPath/                     # Markdown gerado
├── embeddings/                 # Embeddings gerados
├── perguntas_geradas/          # Arquivos TXT de saída
└── RAG_QA_for_PDFs/
    ├── doclingpdf_simples.py   # 1️⃣ Converte PDF
    ├── generate2_simples.py    # 2️⃣ Gera embeddings
    └── ollama_ask2_simples.py  # 3️⃣ PRINCIPAL
```

## 💡 EXEMPLO DE USO

```
🔍 Digite o TEMA (ou 'sair'): penalidades

📝 PERGUNTAS GERADAS SOBRE 'PENALIDADES':
1. Qual é a penalidade aplicada a um atleta que realiza drafting ilegal?
2. Como funciona o procedimento de cumprimento na penalty box?
3. Quais infrações resultam em desqualificação imediata?
4. Qual é a consequência por não usar capacete nas transições?
5. Como são aplicadas penalidades por conduta antidesportiva?

✅ Arquivo salvo: perguntas_geradas/perguntas_respostas_penalidades_20250109_143022.txt
```

## 📄 ARQUIVO GERADO

O arquivo TXT contém:
- ✅ Perguntas numeradas
- ✅ Respostas detalhadas baseadas no regulamento
- ✅ Contexto do PDF usado
- ✅ Timestamp e identificação

## 🎯 TEMAS SUGERIDOS

- `penalidades`
- `equipamentos` 
- `natação`
- `ciclismo`
- `corrida`
- `transições`
- `wetsuit`
- `drafting`
- `desqualificação`

## ⚡ VERSÃO SIMPLIFICADA

Este é o sistema **LIMPO** focado apenas no objetivo principal:
- ❌ Removidas validações complexas
- ❌ Removidos arquivos de exemplo/documentação
- ❌ Removida configuração avançada
- ✅ Apenas 3 scripts essenciais
- ✅ Código direto e simples
- ✅ Foco total no objetivo
