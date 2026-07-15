#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Prospector — publica os sites dos clientes na Vercel via CLI (vercel deploy).
Uso: python3 publicar_vercel.py <pasta_conectada> [--teste]
Lê o bloco "vercel" de prospector-config.json, sincroniza sites/[slug]/ para
uma pasta de staging (_deploy_vercel/[pastaBase]/[slug]/) e roda `vercel deploy --prod`.
Exige a Vercel CLI já instalada e logada (`vercel login`, feito uma vez fora do chat)."""
import json, os, shutil, subprocess, sys

def ler_config(pasta):
    caminho = os.path.join(pasta, 'prospector-config.json')
    try: return json.load(open(caminho, encoding='utf-8'))
    except Exception: return {}

def checar_cli():
    try:
        r = subprocess.run(['vercel', 'whoami'], capture_output=True, text=True, timeout=30)
    except FileNotFoundError:
        print('ERRO: Vercel CLI não encontrada. Instale com `npm install -g vercel` e rode `vercel login` (uma vez, fora do chat).')
        return False
    if r.returncode != 0:
        print('ERRO: Vercel CLI não está logada. Rode `vercel login` (uma vez, fora do chat) e tente de novo.')
        return False
    return True

def sincronizar_sites(pasta, staging, pasta_base):
    origem = os.path.join(pasta, 'sites')
    if not os.path.isdir(origem):
        return []
    slugs = []
    for slug in sorted(os.listdir(origem)):
        origem_slug = os.path.join(origem, slug)
        if not os.path.isdir(origem_slug):
            continue
        destino_slug = os.path.join(staging, pasta_base, slug)
        shutil.copytree(origem_slug, destino_slug, dirs_exist_ok=True)
        slugs.append(slug)
    return slugs

def montar_teste(staging, pasta_base):
    destino = os.path.join(staging, pasta_base, 'teste')
    os.makedirs(destino, exist_ok=True)
    with open(os.path.join(destino, 'index.html'), 'w', encoding='utf-8') as f:
        f.write('<!doctype html><meta charset="utf-8"><title>Teste</title><h1>Funcionou!</h1>')

def linkar_projeto(staging, projeto):
    if os.path.exists(os.path.join(staging, '.vercel', 'project.json')):
        return True
    r = subprocess.run(['vercel', 'link', '--yes', '--project', projeto, '--cwd', staging],
                        capture_output=True, text=True, timeout=60)
    if r.returncode != 0:
        print('ERRO ao vincular o projeto na Vercel:\n' + r.stderr.strip())
        return False
    return True

def publicar(staging):
    r = subprocess.run(['vercel', 'deploy', '--prod', '--yes', '--cwd', staging],
                        capture_output=True, text=True, timeout=300)
    if r.returncode != 0:
        print('ERRO ao publicar na Vercel:\n' + r.stderr.strip())
        return None
    linhas = [l.strip() for l in r.stdout.splitlines() if l.strip().startswith('http')]
    return linhas[-1] if linhas else r.stdout.strip()

def main():
    args = sys.argv[1:]
    teste = '--teste' in args
    posicionais = [a for a in args if a != '--teste']
    if not posicionais:
        print('Uso: python3 publicar_vercel.py <pasta_conectada> [--teste]')
        sys.exit(1)
    pasta = os.path.abspath(posicionais[0])

    if not checar_cli():
        sys.exit(1)

    cfg = ler_config(pasta).get('vercel', {})
    projeto = cfg.get('projeto') or ''
    dominio = cfg.get('dominio') or ''
    pasta_base = cfg.get('pastaBase') or 'clientes'
    if not projeto:
        print('ERRO: falta "projeto" no bloco vercel do prospector-config.json (rode /setup).')
        sys.exit(1)

    staging = os.path.join(pasta, '_deploy_vercel')
    os.makedirs(staging, exist_ok=True)

    if not linkar_projeto(staging, projeto):
        sys.exit(1)

    slugs = sincronizar_sites(pasta, staging, pasta_base)
    if teste:
        montar_teste(staging, pasta_base)

    url_deploy = publicar(staging)
    if not url_deploy:
        sys.exit(1)

    host = dominio or url_deploy.split('//', 1)[-1].rstrip('/')
    if teste:
        print('OK: https://%s/%s/teste/' % (host, pasta_base))
    if slugs:
        print('Publicado(s):')
        for slug in slugs:
            print('  https://%s/%s/%s/' % (host, pasta_base, slug))
    elif not teste:
        print('Nenhum site em sites/ para publicar.')

if __name__ == '__main__':
    main()
