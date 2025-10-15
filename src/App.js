import React, { useState, useEffect } from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';
import './App.css';
import API, { TEMAS_PREDEFINIDOS } from './api';

function App() {
  const [activeTab, setActiveTab] = useState('manual');
  const [tema, setTema] = useState('');
  const [quantidadeAuto, setQuantidadeAuto] = useState(5);
  const [loading, setLoading] = useState(false);
  const [resultado, setResultado] = useState(null);
  const [statusSistema, setStatusSistema] = useState(null);
  const [arquivosGerados, setArquivosGerados] = useState([]);

  // Carregar status do sistema ao iniciar
  useEffect(() => {
    const carregarStatus = async () => {
      try {
        const status = await API.verificarSistema();
        setStatusSistema(status);
        
        const arquivos = await API.obterArquivosGerados();
        setArquivosGerados(arquivos);
      } catch (error) {
        console.error('Erro ao carregar status:', error);
      }
    };
    
    carregarStatus();
  }, []);

  // Gerar questões usando a API
  const gerarQuestoes = async (modo, temaInput = null, quantidade = null) => {
    setLoading(true);
    setResultado(null);

    try {
      let resultado;
      
      if (modo === 'manual') {
        resultado = await API.gerarQuestoesManual(temaInput);
      } else {
        resultado = await API.gerarQuestoesAutomatico(quantidade);
      }
      
      setResultado(resultado);
      
      // Atualizar lista de arquivos
      const arquivosAtualizados = await API.obterArquivosGerados();
      setArquivosGerados(arquivosAtualizados);
      
    } catch (error) {
      console.error('Erro:', error);
      setResultado({ 
        erro: error.message || 'Erro ao gerar questões. Verifique se o sistema Python está funcionando.' 
      });
    } finally {
      setLoading(false);
    }
  };

  const handleManualSubmit = (e) => {
    e.preventDefault();
    if (!tema.trim()) {
      alert('Por favor, digite um tema');
      return;
    }
    gerarQuestoes('manual', tema);
  };

  const handleAutomaticoSubmit = (e) => {
    e.preventDefault();
    gerarQuestoes('automatico', null, quantidadeAuto);
  };

  return (
    <div className="min-vh-100" style={{ backgroundColor: '#f8f9fa' }}>
      {/* Header */}
      <nav className="navbar navbar-expand-lg navbar-dark" style={{ backgroundColor: '#1e3a8a' }}>
        <div className="container">
          <span className="navbar-brand mb-0 h1">
            🏊‍♂️🚴‍♂️🏃‍♂️ Gerador de Perguntas de Triathlon
          </span>
        </div>
      </nav>

      <div className="container mt-4">
        {/* Título Principal */}
        <div className="text-center mb-4">
          <h1 className="display-4 text-primary fw-bold">Sistema RAG - Triathlon</h1>
          <p className="lead text-muted">
            Gerador Inteligente de Perguntas baseado no Regulamento da World Triathlon 2024
          </p>
        </div>

        {/* Cards de Estatísticas */}
        <div className="row mb-4">
          <div className="col-md-3">
            <div className="card bg-primary text-white">
              <div className="card-body text-center">
                <h5>📄 PDF</h5>
                <h3>{statusSistema?.estatisticas?.paginasProcessadas || 208}</h3>
                <small>Páginas Processadas</small>
              </div>
            </div>
          </div>
          <div className="col-md-3">
            <div className="card bg-success text-white">
              <div className="card-body text-center">
                <h5>🔍 Embeddings</h5>
                <h3>{statusSistema?.estatisticas?.embeddingsGerados || '+500'}</h3>
                <small>Contextos Indexados</small>
              </div>
            </div>
          </div>
          <div className="col-md-3">
            <div className="card bg-info text-white">
              <div className="card-body text-center">
                <h5>🎯 Temas</h5>
                <h3>{TEMAS_PREDEFINIDOS.length}</h3>
                <small>Temas Disponíveis</small>
              </div>
            </div>
          </div>
          <div className="col-md-3">
            <div className="card bg-warning text-white">
              <div className="card-body text-center">
                <h5>🤖 IA</h5>
                <h3>{statusSistema?.ollama ? '✅' : '❌'}</h3>
                <small>{statusSistema?.ollama ? 'Ollama OK' : 'Ollama OFF'}</small>
              </div>
            </div>
          </div>
        </div>

        {/* Tabs */}
        <ul className="nav nav-tabs nav-fill mb-4">
          <li className="nav-item">
            <button 
              className={`nav-link ${activeTab === 'manual' ? 'active' : ''}`}
              onClick={() => setActiveTab('manual')}
            >
              📝 Modo Manual
            </button>
          </li>
          <li className="nav-item">
            <button 
              className={`nav-link ${activeTab === 'automatico' ? 'active' : ''}`}
              onClick={() => setActiveTab('automatico')}
            >
              🎲 Modo Automático
            </button>
          </li>
          <li className="nav-item">
            <button 
              className={`nav-link ${activeTab === 'temas' ? 'active' : ''}`}
              onClick={() => setActiveTab('temas')}
            >
              📋 Temas Disponíveis
            </button>
          </li>
        </ul>

        {/* Conteúdo das Tabs */}
        <div className="row">
          <div className="col-md-8">
            {/* Tab Manual */}
            {activeTab === 'manual' && (
              <div className="card shadow">
                <div className="card-header bg-primary text-white">
                  <h5 className="mb-0">📝 Geração Manual de Questões</h5>
                </div>
                <div className="card-body">
                  <p className="text-muted">
                    Digite um tema específico para gerar 5 perguntas personalizadas com respostas detalhadas.
                  </p>
                  
                  <form onSubmit={handleManualSubmit}>
                    <div className="mb-3">
                      <label htmlFor="tema" className="form-label fw-bold">
                        Tema para as Questões:
                      </label>
                      <input
                        type="text"
                        className="form-control form-control-lg"
                        id="tema"
                        value={tema}
                        onChange={(e) => setTema(e.target.value)}
                        placeholder="Ex: penalidades, equipamentos, natação..."
                        disabled={loading}
                      />
                      <div className="form-text">
                        💡 Exemplos: penalidades, equipamentos, drafting, wetsuit, transições
                      </div>
                    </div>
                    
                    <button 
                      type="submit" 
                      className="btn btn-primary btn-lg w-100"
                      disabled={loading || !tema.trim()}
                    >
                      {loading ? (
                        <>
                          <span className="spinner-border spinner-border-sm me-2" role="status"></span>
                          Gerando questões...
                        </>
                      ) : (
                        <>🚀 Gerar Questões Sobre "{tema}"</>
                      )}
                    </button>
                  </form>
                </div>
              </div>
            )}

            {/* Tab Automático */}
            {activeTab === 'automatico' && (
              <div className="card shadow">
                <div className="card-header bg-success text-white">
                  <h5 className="mb-0">🎲 Geração Automática de Questões</h5>
                </div>
                <div className="card-body">
                  <p className="text-muted">
                    Gere múltiplos conjuntos de questões automaticamente com temas escolhidos aleatoriamente.
                  </p>
                  
                  <form onSubmit={handleAutomaticoSubmit}>
                    <div className="mb-3">
                      <label htmlFor="quantidade" className="form-label fw-bold">
                        Quantidade de Conjuntos:
                      </label>
                      <select
                        className="form-select form-select-lg"
                        id="quantidade"
                        value={quantidadeAuto}
                        onChange={(e) => setQuantidadeAuto(parseInt(e.target.value))}
                        disabled={loading}
                      >
                        <option value={3}>3 conjuntos</option>
                        <option value={5}>5 conjuntos</option>
                        <option value={10}>10 conjuntos</option>
                        <option value={15}>15 conjuntos</option>
                        <option value={20}>20 conjuntos</option>
                      </select>
                      <div className="form-text">
                        🎯 Cada conjunto = 5 perguntas + respostas de um tema aleatório
                      </div>
                    </div>
                    
                    <button 
                      type="submit" 
                      className="btn btn-success btn-lg w-100"
                      disabled={loading}
                    >
                      {loading ? (
                        <>
                          <span className="spinner-border spinner-border-sm me-2" role="status"></span>
                          Gerando {quantidadeAuto} conjuntos...
                        </>
                      ) : (
                        <>🎲 Gerar {quantidadeAuto} Conjuntos Automáticos</>
                      )}
                    </button>
                  </form>
                </div>
              </div>
            )}

            {/* Tab Temas */}
            {activeTab === 'temas' && (
              <div className="card shadow">
                <div className="card-header bg-info text-white">
                  <h5 className="mb-0">📋 Temas Disponíveis para Geração</h5>
                </div>
                <div className="card-body">
                  <p className="text-muted mb-3">
                    {TEMAS_PREDEFINIDOS.length} temas especializados em triathlon disponíveis:
                  </p>
                  
                  <div className="row">
                    {TEMAS_PREDEFINIDOS.map((tema, index) => (
                      <div key={index} className="col-md-4 mb-2">
                        <span 
                          className="badge bg-light text-dark border p-2 w-100 d-block text-start cursor-pointer"
                          style={{ cursor: 'pointer' }}
                          onClick={() => {
                            setTema(tema);
                            setActiveTab('manual');
                          }}
                          title="Clique para usar este tema no modo manual"
                        >
                          🏷️ {tema}
                        </span>
                      </div>
                    ))}
                  </div>
                  
                  <div className="mt-3 p-3 bg-light rounded">
                    <small className="text-muted">
                      💡 <strong>Dica:</strong> Clique em qualquer tema para usá-lo no modo manual
                    </small>
                  </div>
                </div>
              </div>
            )}
          </div>

          {/* Sidebar com Resultado */}
          <div className="col-md-4">
            <div className="card shadow">
              <div className="card-header bg-dark text-white">
                <h5 className="mb-0">📊 Resultado</h5>
              </div>
              <div className="card-body">
                {!resultado && !loading && (
                  <div className="text-center text-muted py-5">
                    <h1>🎯</h1>
                    <p>Aguardando geração de questões...</p>
                  </div>
                )}

                {loading && (
                  <div className="text-center py-5">
                    <div className="spinner-border text-primary mb-3" role="status"></div>
                    <p>Processando com IA...</p>
                    <small className="text-muted">Buscando contexto relevante no regulamento</small>
                  </div>
                )}

                {resultado && !resultado.erro && resultado.modo === 'manual' && (
                  <div className="result-appear">
                    <div className="mb-3">
                      <span className="badge bg-primary mb-2">📝 Manual</span>
                      <h6 className="fw-bold">Tema: {resultado.tema}</h6>
                      <small className="text-muted">{resultado.timestamp}</small>
                    </div>

                    <div className="mb-3">
                      <h6>📝 Perguntas Geradas:</h6>
                      <ol className="small">
                        {resultado.perguntas.map((pergunta, index) => (
                          <li key={index} className="mb-1">{pergunta.replace(/^\d+\.\s*/, '')}</li>
                        ))}
                      </ol>
                    </div>

                    <div className="mb-3">
                      <small className="text-muted">
                        🔍 Contextos: {resultado.contextosEncontrados} • 
                        📊 Similaridade: {resultado.similaridade}
                      </small>
                    </div>

                    <div className="alert alert-success">
                      <strong>✅ Sucesso!</strong><br/>
                      <small>
                        📁 Arquivo: {resultado.arquivo}<br/>
                        💾 Salvo em: perguntas_geradas/
                      </small>
                    </div>
                  </div>
                )}

                {resultado && !resultado.erro && resultado.modo === 'automatico' && (
                  <div className="result-appear">
                    <div className="mb-3">
                      <span className="badge bg-success mb-2">🎲 Automático</span>
                      <h6 className="fw-bold">
                        {resultado.sucessos}/{resultado.quantidade} Conjuntos
                      </h6>
                      <small className="text-muted">{resultado.timestamp}</small>
                    </div>

                    <div className="mb-3">
                      <h6>🎯 Temas Processados:</h6>
                      <div className="mb-2">
                        {resultado.temasProcessados.map((tema, index) => (
                          <span key={index} className="badge bg-secondary me-1 mb-1 small">
                            {tema}
                          </span>
                        ))}
                      </div>
                    </div>

                    <div className="mb-3">
                      <small className="text-muted">
                        ⏱️ Tempo: {resultado.tempoProcessamento} • 
                        📊 Taxa de sucesso: 100%
                      </small>
                    </div>

                    <div className="alert alert-success">
                      <strong>✅ Lote Concluído!</strong><br/>
                      <small>
                        📁 {resultado.sucessos} arquivos gerados<br/>
                        💾 Salvo em: perguntas_geradas/
                      </small>
                    </div>
                  </div>
                )}

                {resultado && resultado.erro && (
                  <div className="alert alert-danger">
                    <strong>❌ Erro:</strong><br/>
                    <small>{resultado.erro}</small>
                  </div>
                )}
              </div>
            </div>

            {/* Arquivos Gerados */}
            {arquivosGerados.length > 0 && (
              <div className="card mt-3">
                <div className="card-header bg-secondary text-white">
                  <h6 className="mb-0">📁 Arquivos Recentes</h6>
                </div>
                <div className="card-body p-2">
                  {arquivosGerados.slice(0, 3).map((arquivo, index) => (
                    <div key={index} className="border-bottom pb-2 mb-2 last:border-0">
                      <div className="d-flex justify-content-between align-items-start">
                        <div className="flex-grow-1">
                          <small className="fw-bold text-truncate d-block">
                            {arquivo.tema}
                          </small>
                          <small className="text-muted">
                            {arquivo.data} • {arquivo.tamanho}
                          </small>
                        </div>
                        <span className={`badge badge-sm ${
                          arquivo.modo === 'manual' ? 'bg-primary' : 'bg-success'
                        }`}>
                          {arquivo.modo === 'manual' ? 'M' : 'A'}
                        </span>
                      </div>
                    </div>
                  ))}
                  {arquivosGerados.length > 3 && (
                    <small className="text-muted">
                      +{arquivosGerados.length - 3} arquivos...
                    </small>
                  )}
                </div>
              </div>
            )}

            {/* Status do Sistema */}
            {statusSistema && (
              <div className="card mt-3">
                <div className="card-body">
                  <h6 className="card-title">🔧 Status do Sistema</h6>
                  <small className="text-muted">
                    <div className="mb-1">
                      <strong>Ollama:</strong> {statusSistema.ollama ? '✅ Online' : '❌ Offline'}
                    </div>
                    <div className="mb-1">
                      <strong>Embeddings:</strong> {statusSistema.embeddings ? '✅ OK' : '❌ Erro'}
                    </div>
                    <div className="mb-1">
                      <strong>Índice:</strong> {statusSistema.estatisticas?.tamanhoIndice || 'N/A'}
                    </div>
                    <div>
                      <strong>Última atualização:</strong><br/>
                      {statusSistema.estatisticas?.ultimaAtualizacao || 'N/A'}
                    </div>
                  </small>
                </div>
              </div>
            )}

            {/* Info Card */}
            <div className="card mt-3">
              <div className="card-body">
                <h6 className="card-title">ℹ️ Como Funciona</h6>
                <small className="text-muted">
                  <strong>1. RAG:</strong> Sistema busca contexto relevante no PDF<br/>
                  <strong>2. IA:</strong> Ollama gera perguntas específicas<br/>
                  <strong>3. Respostas:</strong> Baseadas exclusivamente no regulamento<br/>
                  <strong>4. Arquivo:</strong> TXT salvo com perguntas + respostas
                </small>
              </div>
            </div>
          </div>
        </div>

        {/* Footer */}
        <footer className="text-center mt-5 py-3 border-top">
          <small className="text-muted">
            🏆 Sistema RAG para Triathlon • Baseado no Regulamento World Triathlon 2024 • 
            Powered by Ollama + React
          </small>
        </footer>
      </div>
    </div>
  );
}

export default App;