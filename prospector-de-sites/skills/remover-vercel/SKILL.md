---
name: remover-vercel
description: Esta skill deve ser usada para apagar um projeto inteiro da Vercel — ação destrutiva e irreversível que tira TODOS os clientes publicados nele do ar de uma vez, não só um. Acione quando o usuário disser "apagar o projeto", "remover da vercel", "desfazer a publicação de teste", "cancelar o projeto vercel" ou "deletar o site de teste".
---

# Remover projeto da Vercel

## Isso não é pra tirar UM cliente do ar

A arquitetura do Prospector usa **um único projeto Vercel pra agência inteira** (cada cliente é uma subpasta `[pastaBase]/[slug]/` dentro do mesmo projeto — ver skill `deploy-vercel`). Apagar o projeto tira TODOS os clientes já publicados do ar de uma vez.

- **Pra tirar um cliente específico do ar**: apague a pasta `sites/[slug]/` local e rode `/publicar` de novo. Como cada deploy reenvia tudo que existe em `sites/`, o cliente removido simplesmente some do próximo deploy — o projeto Vercel e os demais clientes continuam no ar. NÃO use esta skill pra isso.
- **Pra apagar o projeto inteiro**: só faça isso de propósito — desfazer um teste, recomeçar do zero com outro nome, ou encerrar a operação. É irreversível: perde o histórico de deployments e a URL para de responder na hora (404).

## Confirmação obrigatória (bloqueante)

Nunca rode a remoção sem confirmação explícita do usuário no chat, mostrando claramente:
- Qual projeto vai ser apagado (`vercel.projeto` do config).
- Que TODOS os clientes publicados nele saem do ar imediatamente.

Se o usuário só quer remover um cliente, pare e explique a seção acima em vez de apagar o projeto.

## Comando

```
vercel remove [projeto] --yes
```

Roda direto pelo nome do projeto (sem `--cwd` — não depende da pasta de staging local). Confirme que sumiu:

```
vercel project ls
```

`[projeto]` não deve mais aparecer na lista, e as URLs publicadas devem responder `404`.

## Depois de apagar

- **Se for republicar com o mesmo nome de projeto depois**: apague também `_deploy_vercel/.vercel/` (dentro da pasta conectada) antes do próximo `/publicar`. Sem isso, o script tenta reusar o vínculo antigo (`project.json`) apontando pra um projeto que não existe mais, e o deploy falha.
- **Se for mudar o nome do projeto**: atualize `vercel.projeto` no `prospector-config.json` (dashboard → Configurações → Conexão Vercel).
- Avise o usuário: clientes que estavam com status `publicado` no dashboard agora têm link quebrado — republique antes de mandar qualquer proposta com esse link.
