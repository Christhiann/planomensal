# Plano Mensal — Automação de Documentos

MVP inicial para automatizar o preenchimento do Plano Mensal do Colégio.

## Objetivo
O professor preenche um formulário e o backend usa o modelo oficial `PLANO MENSAL CMT XLVII.docx` para preencher somente os campos editáveis, preservando a formatação institucional.

## Campos editáveis
- COMPONENTE
- PROFESSOR
- ANO
- TURMA
- PERÍODO
- OBJETIVOS
- HABILIDADES
- OBJETOS DO CONHECIMENTO
- METODOLOGIA/ESTRATÉGIAS DIDÁTICAS
- RECURSOS DIDÁTICOS
- AVALIAÇÕES
- REFERÊNCIAS
- ASSINATURA PROFESSOR (A)

## Estrutura
- `frontend/`: Next.js + TypeScript + Tailwind
- `backend/`: FastAPI
- `backend/templates/`: modelo oficial incluído no backend e no deploy

O formulário permite definir o nome do arquivo baixado. A extensão `.docx` é adicionada automaticamente.

## Deploy na Vercel
O projeto está configurado para publicar o Next.js e o FastAPI juntos em um único projeto Vercel usando Vercel Services (Beta). A raiz contém o `vercel.json` com o roteamento: `/api/*` para o backend e as demais rotas para o frontend.

O backend inclui o template Word em `backend/templates/` e gera os documentos em memória durante a requisição, sem depender de armazenamento persistente. Para desenvolvimento com Docker Compose, o Next.js encaminha `/api/*` ao backend usando `API_PROXY_TARGET`.

Na Vercel, importe o repositório pela raiz e publique com suporte a Vercel Services habilitado. Consulte a [documentação de Services](https://vercel.com/docs/services) e o guia de [FastAPI na Vercel](https://vercel.com/docs/frameworks/backend/fastapi).
