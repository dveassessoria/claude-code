// ============================================================
// DVE Assessoria — KPIs Ariana | Importação automática via ClickUp
// Cole esse código em: Extensões > Apps Script (dentro da planilha)
// ============================================================

// ⚙️ CONFIGURAÇÃO — preencha aqui antes de rodar
const CONFIG = {
  CLICKUP_TOKEN: 'pk_270606797_VOAC2C84I4VTYNR680PUCY5OD9CS2FE8',
  TEAM_ID: '9011393934',
  ARIANA_USER_ID: '290564417',      // Ari (aricriativa.br@gmail.com)
  SHEET_NAME: 'Maio Diário',       // Nome exato da aba na planilha
  DATA_START_ROW: 3,               // Linha onde os dados começam
  // Mês de referência (0 = Janeiro, 4 = Maio, 11 = Dezembro)
  // Deixar null para usar o mês atual automaticamente
  MES_REFERENCIA: null,
};

// Mapeamento de status do ClickUp → valores do dropdown da planilha
const STATUS_MAP = {
  'backlog'               : 'Backlog',
  'to do'                 : 'Backlog',
  'open'                  : 'Backlog',
  'in progress'           : 'Andamento',
  'andamento'             : 'Andamento',
  'aprovação copy'        : 'Aprovação Copy',
  'aprovacao copy'        : 'Aprovação Copy',
  'revisão'               : 'Revisão',
  'revisao'               : 'Revisão',
  'review'                : 'Revisão',
  'correção'              : 'Correção',
  'correcao'              : 'Correção',
  'atrasado'              : 'Atrasado',
  'aprovado internamente' : 'Aprovado Internamente',
  'aprovação cliente'     : 'Aprovação Cliente',
  'aprovacao cliente'     : 'Aprovação Cliente',
  'aprovado'              : 'Aprovado',
  'complete'              : 'Aprovado',
  'done'                  : 'Aprovado',
  'closed'                : 'Aprovado',
};

// ============================================================
// FUNÇÃO PRINCIPAL — importa tarefas da Ariana
// ============================================================
function importarTarefasAriana() {
  if (!CONFIG.ARIANA_USER_ID) {
    SpreadsheetApp.getUi().alert('⚠️ Preencha o ARIANA_USER_ID no topo do script.\nRode findArianaId() primeiro para descobrir.');
    return;
  }

  const sheet = getOrCreateSheet(CONFIG.SHEET_NAME);
  const todasTasks = buscarTarefas();
  const tasks = filtrarPorMes(todasTasks);

  if (tasks.length === 0) {
    SpreadsheetApp.getUi().alert('Nenhuma tarefa encontrada para a Ariana no mês de referência.');
    return;
  }

  // Limpar dados existentes (preserva cabeçalho nas linhas 1-2)
  const lastRow = sheet.getLastRow();
  if (lastRow >= CONFIG.DATA_START_ROW) {
    sheet.getRange(CONFIG.DATA_START_ROW, 1, lastRow - CONFIG.DATA_START_ROW + 1, 12).clearContent();
  }

  // Preencher cada tarefa
  tasks.forEach((task, index) => {
    const row = CONFIG.DATA_START_ROW + index;

    const startDate = task.start_date ? new Date(parseInt(task.start_date)) : '';
    const dueDate   = task.due_date   ? new Date(parseInt(task.due_date))   : '';

    // Cliente: extrai do nome da lista (ex: "Gramado Premium - Social" → "Gramado Premium")
    const clienteRaw = task.list?.name || '';
    const cliente = clienteRaw.split(' - ')[0].trim();

    // Status: mapeia do ClickUp para o valor do dropdown
    const statusClickup = task.status?.status || '';
    const statusSheet = STATUS_MAP[statusClickup.toLowerCase().trim()] || statusClickup;

    sheet.getRange(row, 1).setValue(task.name);                                        // A - NOME TAREFA
    sheet.getRange(row, 2).setValue(cliente);                                          // B - CLIENTE
    sheet.getRange(row, 3).setFormula(`=HYPERLINK("${task.url}","Ver no ClickUp")`);  // C - TAREFA (link)
    sheet.getRange(row, 4).setValue(statusSheet);                                      // D - STATUS
    sheet.getRange(row, 5).setValue(startDate);                                        // E - INICIAL
    sheet.getRange(row, 6).setValue(dueDate);                                          // F - VENCIMENTO

    // G - ENTREGA: preencher manualmente (olhar comentário da tarefa onde a Ariana avisa entrega)

    // H - NO PRAZO: fórmula automática — calcula assim que ENTREGA for preenchida
    sheet.getRange(row, 8).setFormula(
      `=IF(G${row}="","",IF(G${row}<=F${row},"Sim","Não"))`
    );
  });

  // Formatar datas
  const totalRows = tasks.length;
  if (totalRows > 0) {
    sheet.getRange(CONFIG.DATA_START_ROW, 5, totalRows, 1).setNumberFormat('dd/MM/yyyy'); // INICIAL
    sheet.getRange(CONFIG.DATA_START_ROW, 6, totalRows, 1).setNumberFormat('dd/MM/yyyy'); // VENCIMENTO
  }

  SpreadsheetApp.getUi().alert(
    `✅ ${tasks.length} tarefas importadas!\n\n` +
    `Preenchido automaticamente:\n` +
    `• Nome, cliente e link\n` +
    `• Status\n` +
    `• Vencimento\n` +
    `• No Prazo (calcula ao preencher Entrega)\n\n` +
    `Preencher manualmente:\n` +
    `• Entrega (ver comentário da tarefa no ClickUp)\n` +
    `• Correções e Qualidade`
  );
}

// ============================================================
// FILTRAR TAREFAS PELO MÊS DE REFERÊNCIA
// Usa a data de vencimento (due_date) como referência
// ============================================================
function filtrarPorMes(tasks) {
  const hoje = new Date();
  const mes = CONFIG.MES_REFERENCIA !== null ? CONFIG.MES_REFERENCIA : hoje.getMonth();
  const ano = hoje.getFullYear();

  return tasks.filter(task => {
    if (!task.due_date) return false;
    const due = new Date(parseInt(task.due_date));
    return due.getMonth() === mes && due.getFullYear() === ano;
  });
}

// ============================================================
// BUSCAR TAREFAS NO CLICKUP (com paginação)
// ============================================================
function buscarTarefas() {
  const allTasks = [];
  let page = 0;
  let hasMore = true;

  while (hasMore) {
    const url = [
      `https://api.clickup.com/api/v2/team/${CONFIG.TEAM_ID}/task`,
      `?assignees[]=${CONFIG.ARIANA_USER_ID}`,
      `&include_closed=true`,
      `&subtasks=true`,
      `&page=${page}`
    ].join('');

    const response = UrlFetchApp.fetch(url, {
      headers: { 'Authorization': CONFIG.CLICKUP_TOKEN },
      muteHttpExceptions: true
    });

    if (response.getResponseCode() !== 200) {
      SpreadsheetApp.getUi().alert(`Erro na API do ClickUp:\n${response.getContentText()}`);
      return [];
    }

    const data = JSON.parse(response.getContentText());
    const tasks = data.tasks || [];

    allTasks.push(...tasks);

    hasMore = tasks.length === 100;
    page++;
  }

  return allTasks;
}

// ============================================================
// HELPER — descobre o ID da Ariana (rodar uma vez no setup)
// Resultado aparece em: Ver > Registros de execução
// ============================================================
function findArianaId() {
  const url = `https://api.clickup.com/api/v2/team/${CONFIG.TEAM_ID}/member`;

  const response = UrlFetchApp.fetch(url, {
    headers: { 'Authorization': CONFIG.CLICKUP_TOKEN },
    muteHttpExceptions: true
  });

  if (response.getResponseCode() !== 200) {
    Logger.log('Erro: ' + response.getContentText());
    return;
  }

  const data = JSON.parse(response.getContentText());
  const membros = data.members.map(m => ({
    id: m.user.id,
    nome: m.user.username,
    email: m.user.email
  }));

  Logger.log('=== MEMBROS DO WORKSPACE ===');
  membros.forEach(m => Logger.log(`ID: ${m.id} | Nome: ${m.nome} | Email: ${m.email}`));
  Logger.log('Copie o ID da Ariana e cole em CONFIG.ARIANA_USER_ID');
}

// ============================================================
// HELPER — testa o mapeamento de status (rodar se achar status errado)
// Resultado aparece em: Ver > Registros de execução
// ============================================================
function verStatusDasTasksAriana() {
  const tasks = buscarTarefas();
  const statusUnicos = [...new Set(tasks.map(t => t.status?.status || 'sem status'))];

  Logger.log('=== STATUS ENCONTRADOS NO CLICKUP ===');
  statusUnicos.forEach(s => {
    const mapeado = STATUS_MAP[s.toLowerCase().trim()] || '⚠️ SEM MAPEAMENTO — adicionar no STATUS_MAP';
    Logger.log(`"${s}" → "${mapeado}"`);
  });
}

// ============================================================
// CRIAR ABA SE NÃO EXISTIR
// ============================================================
function getOrCreateSheet(name) {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  let sheet = ss.getSheetByName(name);

  if (!sheet) {
    sheet = ss.insertSheet(name);
    criarCabecalhos(sheet);
  }

  return sheet;
}

function criarCabecalhos(sheet) {
  const mesAtual = Utilities.formatDate(new Date(), Session.getScriptTimeZone(), 'MMMM yyyy');

  sheet.getRange('A1:M1').merge().setValue(mesAtual);
  sheet.getRange('A1')
    .setBackground('#c6efce')
    .setFontWeight('bold')
    .setFontSize(14)
    .setHorizontalAlignment('center');

  const headers = [
    'NOME TAREFA', 'CLIENTE', 'TAREFA', 'STATUS', 'INICIAL', 'VENCIMENTO',
    'ENTREGA', 'NO PRAZO', 'CORREÇÕES', 'NO PRAZO', 'QUALIDADE', 'TEMPO (dias)'
  ];

  const headerRange = sheet.getRange(2, 1, 1, headers.length);
  headerRange.setValues([headers]);
  headerRange.setBackground('#000000').setFontColor('#ffffff').setFontWeight('bold');
}

// ============================================================
// MENU PERSONALIZADO — aparece na barra do Google Sheets
// ============================================================
function onOpen() {
  SpreadsheetApp.getUi()
    .createMenu('KPIs Ariana')
    .addItem('Importar tarefas do ClickUp', 'importarTarefasAriana')
    .addSeparator()
    .addItem('Ver status existentes no ClickUp', 'verStatusDasTasksAriana')
    .addItem('Descobrir ID da Ariana (setup inicial)', 'findArianaId')
    .addToUi();
}
