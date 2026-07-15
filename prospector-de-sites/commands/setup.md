---
description: Configura o plugin — assinatura, preferências e conexão com a Vercel (roda uma vez)
---

Configure o ambiente do Prospector de Sites. Siga esta ordem:

## 1. Pasta de trabalho

Verifique se há uma pasta do usuário conectada. Se não houver, peça para conectar uma pasta (ex.: "Clientes") usando a ferramenta de solicitação de pasta — tudo (config, leads e sites criados) será salvo nela para persistir entre sessões.

## 2. Verificar config existente

Procure `prospector-config.json` na pasta conectada. Se existir, mostre um resumo e pergunte o que o usuário quer atualizar. Se não existir, colete os dados abaixo.

## 3. Dados do usuário (perguntar via AskUserQuestion / formulário)

Colete:

- **Assinatura da proposta**: nome completo, como quer se apresentar (ex.: "Designer de páginas de alta conversão") e WhatsApp/telefone de contato.
- **Nichos padrão de prospecção**: sugira nutricionistas, psicólogos, advogados e psiquiatras como ponto de partida, mas deixe o usuário editar livremente.
- **Cidade/região padrão**.
- **Leads qualificados por busca**: padrão 10.
- **Modo de envio da proposta**: padrão "criar rascunho no Gmail para revisão" (recomendado). Alternativa: enviar direto.

## 4. Conexão com a Vercel

Confira se a Vercel CLI está pronta: rode `vercel whoami`.

- **Se falhar** (CLI ausente ou não logada): explique que é preciso instalar a Vercel CLI (`npm install -g vercel`) e rodar `vercel login` — UMA vez, feito pelo próprio usuário fora do chat (é um fluxo de e-mail/navegador dele; o Claude nunca faz esse login). Depois de logar, ele volta e roda `/setup` de novo. Salve o config parcial e encerre.
- **Se já estiver logada**: como não há senha nem token envolvido, colete direto no chat (sem a cautela de dado sensível):
  1. **Nome do projeto** (`projeto`): sugira um slug a partir do nome do usuário/agência (ex.: "estudio-paginas"), mas deixe editar. É o nome do projeto na Vercel e também vira o domínio grátis `[projeto].vercel.app`.
  2. **Domínio próprio** (opcional): se o usuário já tiver um domínio anexado ao projeto no painel da Vercel, pergunte qual é. Se não tiver, deixe em branco — usa o `*.vercel.app` grátis, que já é um domínio limpo e apresentável.
  3. **Pasta base** (`pastaBase`): padrão `clientes`.

## 5. Salvar e testar

Salve tudo em `prospector-config.json` na pasta conectada, neste formato:

```json
{
  "assinatura": { "nome": "", "apresentacao": "", "whatsapp": "" },
  "prospeccao": { "nichos": ["nutricionistas", "psicologos", "advogados", "psiquiatras"], "cidade": "", "leadsPorBusca": 10 },
  "envio": { "modo": "rascunho" },
  "vercel": { "projeto": "", "dominio": "", "pastaBase": "clientes" }
}
```

Se o `projeto` foi informado, teste a conexão seguindo a skill `deploy-vercel` (modo `--teste`): publica uma página `teste.html` simples e informa a URL pública ao usuário. Se o teste falhar, diagnostique (CLI não logada, nome de projeto inválido, erro do deploy) antes de concluir.

## 6. Dashboard inicial

Siga a seção "Setup" da skill `dashboard-leads`: copie `dashboard-server.py` e `iniciar-dashboard.bat` para a raiz da pasta conectada, crie o banco `prospector.db` (schema da skill) e gere o `dashboard.html` do template. Explique ao usuário: duplo clique em `iniciar-dashboard.bat` abre o painel completo em http://localhost:8765 com edição/exclusão salvando no banco (requer Python no Windows; sem ele, o dashboard.html abre no modo leitura).

## 7B. Entregar o manual

Copie da pasta do plugin para a pasta conectada (sobrescrevendo versões antigas): `manual.html` (manual do usuário) e o iniciador do dashboard certo pro sistema do usuário (`iniciar-dashboard.bat` ou `.command`). A publicação não precisa de nenhum script local (a Vercel CLI já cuida disso). Apresente o `manual.html` ao usuário com a frase: "Esse é o seu manual — guarda ele que responde 90% das dúvidas."

## 7. Encerrar

Confirme o que foi salvo e explique o ciclo (guiando SEMPRE o próximo passo ao fim de cada comando): `/prospectar` → `/redesenhar` → `/publicar` → `/proposta`, com `/editor` opcional para ajustes manuais e o `dashboard.html` como painel de controle de tudo.
