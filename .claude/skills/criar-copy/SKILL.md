# /criar-copy — Criação de Copy por Cliente e Formato

## Uso

```
/criar-copy [cliente] [formato] "[tema ou briefing do conteúdo]"
```

**Exemplos:**
- `/criar-copy aline-medina reels "identidade em Cristo para mulheres que se comparam"`
- `/criar-copy aline-medina carrossel "3 versículos sobre ansiedade"`
- `/criar-copy aline-medina sazonal "Dia das Mães"`

---

## Formatos disponíveis

| Formato | Arquivo de template |
|---------|-------------------|
| `reels` | templates/reels.md |
| `video-narrado` | templates/video-narrado.md |
| `carrossel` | templates/carrossel.md |
| `estatico` | templates/estatico.md |
| `sazonal` | templates/sazonal.md |

---

## Workflow obrigatório

### Passo 1 — Carregar o perfil do cliente

Ler **obrigatoriamente** antes de escrever qualquer palavra:

1. `clientes/[cliente]/perfil-copy.md` — tom de voz, personas, temas, restrições
2. `clientes/[cliente]/templates/[formato].md` — estrutura e checklist do formato solicitado
3. `clientes/[cliente]/referencias/[formato]/` — ler todos os roteiros/copies aprovados disponíveis para calibrar o estilo

Se algum desses arquivos não existir, avisar o usuário antes de continuar.

### Passo 2 — Confirmar o briefing

Se o usuário não forneceu tema ou briefing junto ao comando, perguntar:

> "Qual é o tema ou a mensagem central desse [formato]? Tem algum versículo específico que quer usar?"

Não avançar sem ter pelo menos o tema central.

### Passo 3 — Gerar o copy

Usar o template do formato como estrutura. Preencher com:
- Tom de voz e estilo extraídos do perfil do cliente
- Padrões observados nas referências aprovadas (estrutura de hook, uso de versículo, ritmo das frases, estilo de CTA)
- O tema/briefing fornecido pelo usuário

**Nunca inventar versículos.** Se precisar de um versículo e não tiver certeza da referência exata, indicar o tema bíblico e pedir para o usuário confirmar o versículo antes de incluir.

### Passo 4 — Entregar com checklist

Após o copy, exibir o checklist do template com os itens marcados/desmarcados conforme o que foi produzido. Itens não atendidos devem aparecer com nota explicativa.

---

## Regras absolutas (para todos os clientes)

- Nunca usar travessão (—) em nenhuma parte do copy
- Nunca inventar versículos, referências bíblicas ou citações
- Nunca citar versículo sem referência completa (livro, capítulo, versículo)
- Nunca usar estrutura "Isso não é X. Isso é Y." em nenhuma variação
- Respeitar rigorosamente as restrições listadas no perfil do cliente

---

## Quando o template do formato não existe

Se `clientes/[cliente]/templates/[formato].md` não existir, avisar:

> "O template para [formato] ainda não foi criado para [cliente]. Quer que eu crie agora com base no perfil de copy e nas referências disponíveis?"
