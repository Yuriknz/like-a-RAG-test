"""
📄 CONVERSOR PDF → MARKDOWN (SIMPLIFICADO)
=========================================
Converte PDF do triathlon para Markdown
Detecta automaticamente GPU/CPU e configura adequadamente
"""

import os
import warnings
from pathlib import Path
from docling.document_converter import DocumentConverter

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

def convert_pdf():
    """Converte PDF para Markdown."""
    
    # 1. Detectar e configurar hardware
    hardware_mode = detect_hardware()
    configure_for_hardware(hardware_mode)
    
    # 2. Verificar se Docling está instalado
    try:
        DocumentConverter()
    except ImportError:
        print("❌ Docling não instalado")
        print("💡 Execute: pip install docling")
        return False
    
    # 3. Encontrar PDF
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
    
    # 4. Preparar saída
    output_path = Path(OUTPUT_FILE)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    try:
        # 5. Converter com configuração adequada para o hardware
        converter = DocumentConverter()
        print("🔄 Processando...")
        result = converter.convert(str(source_pdf))
        
        # 6. Salvar
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(result.document.export_to_markdown())
        
        print(f"✅ Markdown salvo: {output_path}")
        print(f"📊 Tamanho do arquivo: {output_path.stat().st_size / 1024:.1f} KB")
        return True
        
    except Exception as e:
        print(f"❌ Erro na conversão: {e}")
        if "CUDA" in str(e) or "pin_memory" in str(e):
            print("💡 Problema relacionado à GPU. Tentando novamente...")
            print("💡 Instale drivers NVIDIA + CUDA para melhor performance")
        return False

if __name__ == "__main__":
    print("📄 CONVERSOR PDF → MARKDOWN")
    print("=" * 40)
    
    if convert_pdf():
        print("\n🎉 Conversão concluída!")
        print("💡 Próximo passo: python generate2_simples.py")
    else:
        print("\n❌ Falha na conversão")
        print("💡 Verifique se:")
        print("   - PDF está na pasta pdfPath/")
        print("   - Docling está instalado: pip install docling")
        print("   - Para GPU: instale CUDA + drivers NVIDIA")
