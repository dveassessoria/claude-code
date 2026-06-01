// ============================================================
// DVE Assessoria — KPIs Ariana | Importação automática via ClickUp
// Cole esse código em: Extensões > Apps Script (dentro da planilha)
// ============================================================

// ⚙️ CONFIGURAÇÃO — preencha aqui antes de rodar
const CONFIG = {
  CLICKUP_TOKEN: 'SEU_TOKEN_AQUI',  // Seu token de API do ClickUp
  TEAM_ID: 'SEU_TEAM_ID_AQUI',     // ID do workspace (está na URL: app.clickup.com/{ID}/...)
  ARIANA_USER_ID: '',               // Deixar vazio na primeira vez — rodar findArianaId() pra descobrir
  SHEET_NAME: 'Ariana',            // Nome da aba na planilha
  DATA_START_ROW: 3,               // Linha onde os dados começam (igual ao modelo do Wesley)
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
  const tasks = buscarTarefas();

  if (tasks.length === 0) {
    SpreadsheetApp.getUi().alert('Nenhuma tarefa encontrada para a Ariana.');
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

    // Extrai nome do cliente a partir do nome da lista (ex: "Gramado Premium - Social")
    const clienteRaw = task.list?.name || '';
    const cliente = clienteRaw.split(' - ')[0].trim();

    sheet.getRange(row, 1).setValue(task.name);                                                // A - DEMANDA
    sheet.getRange(row, 2).setValue(cliente);                                                  // B - CLIENTE
    sheet.getRange(row, 3).setFormula(`=HYPERLINK("${task.url}","Ver no ClickUp")`);          // C - TAREFA (link)
    // D (STATUS) — preencher manualmente
    sheet.getRange(row, 5).setValue(startDate);                                                // E - INICIAL
    sheet.getRange(row, 6).setValue(dueDate);                                                  // F - VENCIMENTO
    // G (ENTREGA), H (NO PRAZO), I (CORREÇÕES), J-L — preencher manualmente
  });

  // Formatar datas
  const totalRows = tasks.length;
  if (totalRows > 0) {
    sheet.getRange(CONFIG.DATA_START_ROW, 5, totalRows, 1).setNumberFormat('dd/MM/yyyy');
    sheet.getRange(CONFIG.DATA_START_ROW, 6, totalRows, 1).setNumberFormat('dd/MM/yyyy');
  }

  SpreadsheetApp.getUi().alert(`✅ ${tasks.length} tarefas importadas com sucesso!`);
}

// ============================================================
// BUSCAR TAREFAS NO CLICKUP (com paginação)
// ============================================================
function buscarTarefas() {
  const allTasks = [];
  let page = 0;
  let hasMore = true;

  while (hasMore) {
    const url = `https://api.clickup.com/api/v2/team/${CONFIG.TEAM_ID}/task?assignees[]=${CONFIG.ARIANA_USER_ID}&include_closed=true&subtasks=true&page=${page}`;

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

    // ClickUp retorna max 100 por página
    hasMore = tasks.length === 100;
    page++;
  }

  return allTasks;
}

// ============================================================
// HELPER — descobre o ID da Ariana (rodar uma vez)
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
// CRIAR ABA SE NÃO EXISTIR (com cabeçalhos iguais ao Wesley)
// ============================================================
function getOrCreateSheet(name) {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  let sheet = ss.getSheetByName(name);

  if (!sheet) {
    sheet = ss.insertSheet(name);
    criarCabecalhos(sheet);
    Logger.log(`Aba "${name}" criada com sucesso.`);
  }

  return sheet;
}

function criarCabecalhos(sheet) {
  // Linha 1 — título do mês (igual ao Wesley)
  sheet.getRange('A1:M1').merge().setValue('Ariana');
  sheet.getRange('A1').setBackground('#c6efce').setFontWeight('bold').setHorizontalAlignment('center');

  // Linha 2 — cabeçalhos das colunas
  const headers = [
    'DEMANDA', 'CLIENTE', 'TAREFA', 'STATUS', 'INICIAL', 'VENCIMENTO',
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
    .createMenu('📋 KPIs Ariana')
    .addItem('Importar tarefas do ClickUp', 'importarTarefasAriana')
    .addSeparator()
    .addItem('Descobrir ID da Ariana (setup inicial)', 'findArianaId')
    .addToUi();
}
