---
name: deploy-vercel
description: Esta skill deve ser usada ao publicar páginas na Vercel — deploy via Vercel CLI (vercel deploy), um projeto único com pasta por cliente, verificação da URL pública e HTTPS. Acione quando o usuário disser "publicar", "subir o site", "colocar no ar", "deploy", "vercel" ou rodar /publicar ou o teste de conexão do /setup.
---

# Deploy na Vercel

Publicar páginas em `[pastaBase]/[slug]/` dentro de um único projeto Vercel e garantir a URL pública `https://[dominio]/[pastaBase]/[slug]/` funcionando.

## Pré-requisito

Vercel CLI instalada e logada (`npm install -g vercel` + `vercel login`, feito UMA vez pelo próprio usuário, fora do chat — login é fluxo de navegador/e-mail dele, o Claude nunca faz login por ele). Sem isso, `python3 references/publicar_vercel.py` falha com uma mensagem clara indicando o que falta.

## Configuração

Tudo vem de `prospector-config.json` (bloco `vercel`): `projeto` (nome do projeto na Vercel), `dominio` (opcional — domínio próprio já anexado ao projeto no painel da Vercel; vazio = usa o `*.vercel.app` grátis que a Vercel atribui) e `pastaBase` (padrão `clientes`). Nenhum desses campos é segredo — podem ser coletados direto no chat do `/setup`, sem a cautela que senhas exigem.

## Publicar

Rode `python3 references/publicar_vercel.py [pasta_conectada]` (passando o caminho da pasta conectada do usuário). O script:

1. Confere que a CLI está logada (`vercel whoami`).
2. Vincula o projeto (`vercel link --yes --project [projeto]`) na primeira vez — depois disso o vínculo fica salvo em `_deploy_vercel/.vercel/project.json` na pasta conectada.
3. Sincroniza TODOS os clientes de `sites/[slug]/` para `_deploy_vercel/[pastaBase]/[slug]/` (um deploy da Vercel é um snapshot completo — reenviar todo mundo a cada `/publicar` é o que mantém os clientes já publicados no ar).
4. Roda `vercel deploy --prod --yes` e imprime a URL pública de cada cliente.

Não existe fallback manual nem instalação de nada no computador do usuário — a publicação acontece inteira dentro do chat, na hora.

## Verificação (obrigatória, após publicar)

1. Abra `https://[dominio]/[pastaBase]/[slug]/` e a capa `.../proposta.html` — confirme que carregam com conteúdo certo.
2. HTTPS já vem pronto por padrão (Vercel emite certificado automático, sem passo extra) — só confirme que o cadeado aparece. Se for um domínio próprio recém-anexado, a emissão pode levar alguns minutos.
3. Atualize `leads.md` + dashboard com status `publicado` e a URL.

## Teste de conexão do /setup

Rode `python3 references/publicar_vercel.py [pasta_conectada] --teste` — publica um `teste.html` simples ("Funcionou!") em `[pastaBase]/teste/`. Se falhar, a mensagem de erro já indica se é falta de login na CLI, `projeto` não configurado, ou erro do próprio deploy.
