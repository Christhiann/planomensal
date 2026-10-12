# Plano Mensal — Automação de Documentos

MVP inicial para automatizar o preenchimento do Plano Mensal do Colégio.

## Objetivo
O professor preenche um formulário simples e, futuramente, o backend usará o modelo oficial `PLANO MENSAL CMT XLVII.doc/.docx` para preencher somente os campos editáveis, preservando a formatação institucional.

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
- `templates/`: local reservado para o modelo oficial

O formulário permite definir o nome do arquivo baixado. A extensão `.docx` é adicionada automaticamente.

## Próximo passo
Quando o modelo em `.docx` for enviado, o backend será conectado ao template real e será implementada a substituição dos campos e conversão para PDF.
