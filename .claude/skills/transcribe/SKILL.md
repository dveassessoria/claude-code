# Transcribe Skill

Transcreve vídeos de qualquer plataforma: YouTube, Instagram, TikTok, X/Twitter, Facebook, Vimeo e mais de 1000 outros sites.

## Quando usar

Acionar quando o usuário:
- Chamar `/transcribe <url>`
- Pedir pra transcrever um vídeo
- Compartilhar um link e pedir legenda, resumo ou texto do vídeo

## Como executar

1. Perguntar se quer timestamps (sim/não)
2. Rodar o script:

```bash
python3 ~/.claude/skills/transcribe/scripts/transcribe_url.py "<url>" [--timestamps] [--model medium]
```

Opções:
- `--timestamps` — adiciona marcações `[M:SS]` em cada segmento
- `--model <tamanho>` — modelo Whisper: `small`, `medium` (padrão), `large-v3`

## Instalação dos requisitos

Se as dependências estiverem faltando, orientar o usuário:

```bash
pip3 install yt-dlp faster-whisper
brew install ffmpeg   # macOS
```

O modelo Whisper (~1.5GB) é baixado automaticamente na primeira execução.

## Fluxo de instalação guiada

Quando o usuário chamar `/transcribe install`, verificar dependências:

```bash
python3 -c "import yt_dlp; print('yt-dlp OK')"
python3 -c "from faster_whisper import WhisperModel; print('faster-whisper OK')"
ffmpeg -version | head -1
```

Reportar o que está OK e o que precisa instalar.
