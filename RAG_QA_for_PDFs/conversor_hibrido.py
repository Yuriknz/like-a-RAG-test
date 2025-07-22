"""
📄 CONVERSOR PDF → MARKDOWN (HÍBRIDO)
====================================
Tenta Docling (melhor qualidade) → Fallback para PyMuPDF (mais simples)
Detecta automaticamente GPU/CPU e configura adequadamente
"""

import os
import warnings
from pathlib import Path

# Configuração simples
PDF_DIR = "../pdfPath"
OUTPUT_FILE = "../mdPath/pdf2.md"

def detect_hardware():
    """Detecta hardware disponível e configura otimizações."""
    try:
        import torch
        
        print("🔍 DETECTANDO HARDWARE...")
        
        # Verificar CUDA
        cuda_available = torch.cuda.is_available()
        
        if cuda_available:
            gpu_count = torch.cuda.device_count()
            gpu_name = torch.cuda.get_device_name(0) if gpu_count > 0 else "Desconhecida"
            print(f"✅ GPU detectada: {gpu_name}")
            print(f"📊 Número de GPUs: {gpu_count}")
            print(f"🚀 Modo: ACELERAÇÃO POR GPU")
            return "gpu"
        else:
            print("⚠️ CUDA não disponível")
            print("💻 Modo: PROCESSAMENTO POR CPU")
            print("💡 Para usar GPU: instale CUDA + drivers NVIDIA")
            return "cpu"
            
    except ImportError:
        print("⚠️ PyTorch não detectado")
        print("💻 Modo: PROCESSAMENTO POR CPU")
        return "cpu"

def configure_for_hardware(mode):
    """Configura ambiente baseado no hardware."""
    if mode == "cpu":
        # Silenciar warnings relacionados à GPU quando usando CPU
        warnings.filterwarnings("ignore", message=".*pin_memory.*")
        warnings.filterwarnings("ignore", message=".*CUDA.*")
        warnings.filterwarnings("ignore", message=".*symlink.*")
        
        # Configurar PyTorch para CPU (se disponível)
        try:
            import torch
            torch.set_num_threads(4)  # Usar 4 threads da CPU
            print("🔧 CPU otimizada: 4 threads")
        except ImportError:
            pass
    
    elif mode == "gpu":
        print("🔧 GPU configurada para aceleração máxima")
    
    print("=" * 40)

def convert_with_docling(source_pdf, output_path):
    """Converte usando Docling (melhor qualidade)."""
    try:
        from docling.document_converter import DocumentConverter
        
        print("📄 Usando Docling (alta qualidade)...")
        converter = DocumentConverter()
        result = converter.convert(str(source_pdf))
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(result.document.export_to_markdown())
        
        return True
        
    except ImportError:
        print("⚠️ Docling não instalado - usando alternativa...")
        return False
    except Exception as e:
        print(f"⚠️ Erro com Docling: {e}")
        print("🔄 Tentando alternativa...")
        return False

def convert_with_pymupdf(source_pdf, output_path):
    """Converte usando PyMuPDF (fallback simples)."""
    try:
        import fitz  # PyMuPDF
        
        print("📄 Usando PyMuPDF (extração simples)...")
        doc = fitz.open(str(source_pdf))
        full_text = ""
        
        print(f"📖 Processando {len(doc)} páginas...")
        
        for page_num in range(len(doc)):
            page = doc[page_num]
            text = page.get_text()
            full_text += f"\n\n## Página {page_num + 1}\n\n{text}"
            
            if (page_num + 1) % 20 == 0:
                print(f"   📄 Processadas {page_num + 1} páginas...")
        
        doc.close()
        
        # Salvar como Markdown
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(f"# REGULAMENTO WORLD TRIATHLON 2024\n\n{full_text}")
        
        return True
        
    except ImportError:
        print("❌ PyMuPDF também não está instalado")
        print("💡 Execute: pip install PyMuPDF")
        return False
    except Exception as e:
        print(f"❌ Erro com PyMuPDF: {e}")
        return False

def convert_pdf():
    """Converte PDF para Markdown usando melhor método disponível."""
    
    # 1. Detectar e configurar hardware
    hardware_mode = detect_hardware()
    configure_for_hardware(hardware_mode)
    
    # 2. Encontrar PDF
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
    
    # 3. Preparar saída
    output_path = Path(OUTPUT_FILE)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    # 4. Tentar conversão (Docling primeiro, PyMuPDF como fallback)
    print("🔄 Processando...")
    
    success = convert_with_docling(source_pdf, output_path)
    
    if not success:
        success = convert_with_pymupdf(source_pdf, output_path)
    
    if success:
        print(f"✅ Markdown salvo: {output_path}")
        print(f"📊 Tamanho: {output_path.stat().st_size / 1024:.1f} KB")
        return True
    else:
        print("❌ Falha em todos os métodos de conversão")
        return False

if __name__ == "__main__":
    print("📄 CONVERSOR PDF → MARKDOWN (HÍBRIDO)")
    print("=" * 50)
    
    if convert_pdf():
        print("\n🎉 Conversão concluída!")
        print("💡 Próximo passo: python generate2_simples.py")
    else:
        print("\n❌ Falha na conversão")
        print("💡 Instale pelo menos uma opção:")
        print("   - pip install docling (melhor qualidade)")
        print("   - pip install PyMuPDF (mais simples)")
