---
description: Publica as páginas redesenhadas na Vercel e retorna as URLs públicas
argument-hint: "[nome do cliente ou todos]"
---

Publique páginas na Vercel seguindo a skill `deploy-vercel`.

## Passos

1. Leia `prospector-config.json`. Se o bloco `vercel` não estiver preenchido (falta `projeto`), colete-o agora direto no chat (não é dado sensível) — não prossiga sem ele.
2. Determine o que publicar: `$ARGUMENTS` (um cliente ou "todos"), ou liste as páginas com status `redesenhado` em `leads.md` e pergunte.
3. **Gere a página-capa de cada cliente**: preencha `references/capa-proposta-template.html` (skill `proposta-email`) com os dados do lead + assinatura do config e salve como `sites/[slug]/proposta.html`. É ela que vai no e-mail de proposta.
4. **Publique seguindo a skill `deploy-vercel`**: rode `python3 references/publicar_vercel.py [pasta_conectada]` — ele sincroniza todos os clientes de `sites/` e roda `vercel deploy --prod` na hora, sem fila, sem instalador, sem ação nenhuma do usuário.
5. **Verificação HTTPS**: abra cada URL com `https://` e confirme que carrega com cadeado válido (a Vercel já emite HTTPS automático, então isso normalmente já vem pronto — só confira).
6. Atualize `leads.md` e o banco do dashboard: status `publicado` + URL pública nova.

## Saída

Liste, por cliente: URL da página nova e URL da capa (`.../proposta.html`), ambas testadas em https. Sugira o próximo passo: `/proposta` para enviar os e-mails.
