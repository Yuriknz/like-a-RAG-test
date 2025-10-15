/**
 * 🔌 API CONNECTOR PARA O SISTEMA PYTHON
 * =====================================
 * Este arquivo simula a conexão com o backend Python
 * Em um ambiente de produção, seria substituído por chamadas HTTP reais
 */

// Simular delay de rede
const delay = (ms) => new Promise(resolve => setTimeout(resolve, ms));

// Temas disponíveis (sincronizado com o Python)
export const TEMAS_PREDEFINIDOS = [
  "penalidades", "equipamentos", "natação", "ciclismo", "corrida", 
  "transições", "wetsuit", "drafting", "desqualificação", "cronometragem",
  "largada", "chegada", "capacete", "bicicleta", "números de competição",
  "área de transição", "alimentação", "hidratação", "oficiais técnicos",
  "protestos", "appeals", "categorias", "classificação", "distâncias oficiais",
  "tempo limite", "condições climáticas", "segurança", "dopagem", "fair play",
  "comportamento antisportivo"
];

/**
 * Gera questões no modo manual
 * @param {string} tema - Tema especificado pelo usuário
 * @returns {Promise} Resultado da geração
 */
export const gerarQuestoesManual = async (tema) => {
  console.log(`🔄 Gerando questões manuais para o tema: ${tema}`);
  
  // Simular processamento
  await delay(2000 + Math.random() * 2000);
  
  // Simular possível erro (5% de chance)
  if (Math.random() < 0.05) {
    throw new Error('Erro na conexão com o sistema Ollama');
  }
  
  // Simular resultado real do sistema Python
  const perguntasGeradas = [
    `Qual é a penalidade aplicada para ${tema} no triathlon segundo o regulamento?`,
    `Como funciona o procedimento de ${tema} durante uma competição oficial?`,
    `Quais são as regras específicas sobre ${tema} estabelecidas pela World Triathlon?`,
    `Em que situações ${tema} pode resultar em desqualificação do atleta?`,
    `Como os oficiais técnicos avaliam questões relacionadas a ${tema}?`
  ];
  
  const timestamp = new Date().toLocaleString('pt-BR');
  const nomeArquivo = `MANUAL_perguntas_respostas_${tema.replace(/\s+/g, '_')}_${Date.now()}.txt`;
  
  return {
    sucesso: true,
    modo: 'manual',
    tema: tema,
    perguntas: perguntasGeradas,
    respostas: perguntasGeradas.map(pergunta => ({
      pergunta: pergunta,
      resposta: `Segundo o regulamento da World Triathlon 2024, ${tema} é regulamentado por diretrizes específicas que visam garantir a segurança e equidade da competição. As regras estabelecem critérios claros para ${tema}, incluindo procedimentos detalhados para situações específicas durante a prova. Os atletas devem estar cientes dessas regulamentações para evitar penalizações e garantir uma competição justa.`
    })),
    arquivo: nomeArquivo,
    timestamp: timestamp,
    contextosEncontrados: Math.floor(Math.random() * 5) + 3, // 3-7 contextos
    similaridade: (Math.random() * 0.3 + 0.7).toFixed(3) // 0.700-1.000
  };
};

/**
 * Gera questões no modo automático
 * @param {number} quantidade - Número de conjuntos a gerar
 * @returns {Promise} Resultado da geração
 */
export const gerarQuestoesAutomatico = async (quantidade) => {
  console.log(`🎲 Gerando ${quantidade} conjuntos automáticos de questões`);
  
  // Simular processamento mais longo para múltiplos temas
  await delay(3000 + (quantidade * 1000));
  
  // Simular possível erro (3% de chance)
  if (Math.random() < 0.03) {
    throw new Error('Timeout na geração automática - muitos temas selecionados');
  }
  
  // Selecionar temas aleatórios
  const temasSelecionados = [];
  const temasDisponiveis = [...TEMAS_PREDEFINIDOS];
  
  for (let i = 0; i < quantidade && temasDisponiveis.length > 0; i++) {
    const indiceAleatorio = Math.floor(Math.random() * temasDisponiveis.length);
    const temaSelecionado = temasDisponiveis.splice(indiceAleatorio, 1)[0];
    temasSelecionados.push(temaSelecionado);
  }
  
  const timestamp = new Date().toLocaleString('pt-BR');
  const conjuntosGerados = temasSelecionados.map((tema, index) => ({
    id: index + 1,
    tema: tema,
    perguntas: [
      `Qual é a penalidade aplicada para ${tema} no triathlon?`,
      `Como funciona o procedimento de ${tema} durante a competição?`,
      `Quais são as regras específicas sobre ${tema}?`,
      `Em que situações ${tema} pode resultar em desqualificação?`,
      `Como os oficiais avaliam questões relacionadas a ${tema}?`
    ],
    arquivo: `AUTO_perguntas_respostas_${tema.replace(/\s+/g, '_')}_${Date.now() + index}.txt`,
    contextosEncontrados: Math.floor(Math.random() * 4) + 2, // 2-5 contextos
    similaridade: (Math.random() * 0.25 + 0.75).toFixed(3) // 0.750-1.000
  }));
  
  return {
    sucesso: true,
    modo: 'automatico',
    quantidade: quantidade,
    temasProcessados: temasSelecionados,
    conjuntos: conjuntosGerados,
    timestamp: timestamp,
    tempoProcessamento: `${quantidade * 1.5} segundos`,
    sucessos: conjuntosGerados.length,
    falhas: 0
  };
};

/**
 * Verifica o status do sistema Python
 * @returns {Promise} Status do sistema
 */
export const verificarSistema = async () => {
  console.log('🔍 Verificando status do sistema...');
  
  await delay(1000);
  
  // Simular verificações do sistema
  const statusSimulado = {
    ollama: Math.random() > 0.1, // 90% chance de estar funcionando
    embeddings: Math.random() > 0.05, // 95% chance de existir
    pdf: Math.random() > 0.02, // 98% chance de existir
    modelos: {
      embedding: 'nomic-embed-text:latest',
      chat: 'phi3.5:latest'
    },
    estatisticas: {
      paginasProcessadas: 208,
      embeddingsGerados: Math.floor(Math.random() * 100) + 450, // 450-549
      tamanhoIndice: '2.3 MB',
      ultimaAtualizacao: new Date(Date.now() - Math.random() * 86400000).toLocaleString('pt-BR')
    }
  };
  
  return statusSimulado;
};

/**
 * Obtém lista de arquivos gerados
 * @returns {Promise} Lista de arquivos
 */
export const obterArquivosGerados = async () => {
  console.log('📁 Obtendo lista de arquivos gerados...');
  
  await delay(500);
  
  // Simular lista de arquivos existentes
  const arquivosSimulados = [
    {
      nome: 'MANUAL_perguntas_respostas_penalidades_20250107_143022.txt',
      modo: 'manual',
      tema: 'penalidades',
      data: '07/01/2025 14:30:22',
      tamanho: '15.2 KB'
    },
    {
      nome: 'AUTO_perguntas_respostas_equipamentos_20250107_145831.txt',
      modo: 'automatico',
      tema: 'equipamentos',
      data: '07/01/2025 14:58:31',
      tamanho: '18.7 KB'
    },
    {
      nome: 'MANUAL_perguntas_respostas_natacao_20250107_151204.txt',
      modo: 'manual',
      tema: 'natação',
      data: '07/01/2025 15:12:04',
      tamanho: '16.9 KB'
    }
  ];
  
  return arquivosSimulados;
};

// Exportar funções principais
const API = {
  gerarQuestoesManual,
  gerarQuestoesAutomatico,
  verificarSistema,
  obterArquivosGerados,
  TEMAS_PREDEFINIDOS
};

export default API;