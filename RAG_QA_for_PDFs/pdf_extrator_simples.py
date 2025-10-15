"""
📄 CONVERSOR PDF -> TEXTO SIMPLES
===============================
Extrai texto do PDF de forma simples sem dependências complexas
"""

import fitz  # PyMuPDF
from pathlib import Path

# Configuração simples  
PDF_DIR = "../pdfPath"
OUTPUT_FILE = "../mdPath/pdf2.md"

def convert_pdf():
    """Converte PDF para texto usando PyMuPDF."""
    
    # Verificar se PyMuPDF está instalado
    try:
        import fitz
    except ImportError:
        print("❌ PyMuPDF não instalado")
        print("💡 Execute: pip install PyMuPDF")
        return False
    
    # Encontrar PDF
    pdf_dir = Path(PDF_DIR)
    if not pdf_dir.exists():
        print(f"❌ Diretório não encontrado: {pdf_dir}")
        return False
    
    pdf_files = list(pdf_dir.glob("*.pdf"))
    if not pdf_files:
        print(f"❌ Nenhum PDF encontrado em: {pdf_dir}")
        return False
    
    source_pdf = pdf_files[0]
    print(f"📄 Convertendo: {source_pdf.name}")
    
    # Preparar saída
    output_path = Path(OUTPUT_FILE)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    try:
        # Abrir PDF
        doc = fitz.open(str(source_pdf))
        text_content = ""
        
        print(f"🔄 Processando {len(doc)} páginas...")
        
        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            text = page.get_text()
            text_content += f"\n\n## Página {page_num + 1}\n\n{text}"
            
            if (page_num + 1) % 10 == 0:
                print(f"   Processadas: {page_num + 1}/{len(doc)} páginas")
        
        doc.close()
        
        # Salvar
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(text_content)
        
        print(f"✅ Texto extraído e salvo: {output_path}")
        print(f"📊 Total de caracteres: {len(text_content)}")
        return True
        
    except Exception as e:
        print(f"❌ Erro na conversão: {e}")
        return False

if __name__ == "__main__":
    print("📄 CONVERSOR PDF → TEXTO")
    print("=" * 40)
    
    if convert_pdf():
        print("\n🎉 Conversão concluída!")
        print("💡 Próximo passo: python generate2_simples.py")
    else:
        print("\n❌ Falha na conversão")
        print("💡 Instale PyMuPDF: pip install PyMuPDF")
