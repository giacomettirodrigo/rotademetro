#!/usr/bin/env python3
"""
IndexNow submission script for rotademetro.com.br
Submits all site URLs to Bing via IndexNow API.

Usage:
    python3 indexnow-submit.py

Requirements:
    pip install requests

Before running:
    1. Create a key verification file at your site root:
       Create a file named "3dd321d0b98c03176990edd0c677541d.txt"
       containing only the key: 3dd321d0b98c03176990edd0c677541d
    2. Deploy the site so the key file is accessible at:
       https://www.rotademetro.com.br/3dd321d0b98c03176990edd0c677541d.txt
    3. Run this script.
"""

import requests
import json
import time

# ── Config ──────────────────────────────────────────────────────────────────
API_KEY   = "3dd321d0b98c03176990edd0c677541d"
HOST      = "www.rotademetro.com.br"
BASE_URL  = f"https://{HOST}"
ENDPOINT  = "https://api.indexnow.org/indexnow"
# ────────────────────────────────────────────────────────────────────────────

URLS = [
    # Static pages
    f"{BASE_URL}/",
    f"{BASE_URL}/todos-os-posts.html",
    f"{BASE_URL}/p/sobre.html",
    f"{BASE_URL}/p/contato.html",
    f"{BASE_URL}/p/busca-por-estacao.html",
    f"{BASE_URL}/p/politica-de-privacidade.html",

    # Posts — 2012 originals
    f"{BASE_URL}/2012/02/metro-se-caixa-cultural.html",
    f"{BASE_URL}/2012/02/casa-da-imagem-e-beco-do-pinto-metro-se.html",
    f"{BASE_URL}/2012/02/pateo-do-colegio-metro-se.html",
    f"{BASE_URL}/2012/02/metro-consolacao-caixa-cultural-avenida.html",
    f"{BASE_URL}/2012/03/metro-liberdade-feira-da-liberdade.html",
    f"{BASE_URL}/2012/03/happy-hour-no-metro-ana-rosa-bar-veloso.html",
    f"{BASE_URL}/2012/03/metro-sao-bento-india-centro-cultural.html",
    f"{BASE_URL}/2012/03/metro-trianon-masp-parque-trianon.html",

    # Posts — 2026 May
    f"{BASE_URL}/2026/05/masp-avenida-paulista-metro-trianon.html",
    f"{BASE_URL}/2026/05/visitar-theatro-municipal-sp-metro-anhangabau.html",
    f"{BASE_URL}/2026/05/pinacoteca-de-sp-de-metro-como-chegar.html",
    f"{BASE_URL}/2026/05/museu-da-lingua-portuguesa-como-visitar.html",
    f"{BASE_URL}/2026/05/mosteiro-sao-bento-sp-metro-como-chegar.html",
    f"{BASE_URL}/2026/05/mercado-municipal-sp-metro-sao-bento.html",
    f"{BASE_URL}/2026/05/bairro-liberdade-metro-guia-japao-sao-paulo.html",
    f"{BASE_URL}/2026/05/parque-ibirapuera-metro-brigadeiro.html",
    f"{BASE_URL}/2026/05/feira-artes-praca-republica-metro-republica.html",
    f"{BASE_URL}/2026/05/japan-house-sp-metro-paraiso.html",
    f"{BASE_URL}/2026/05/beco-do-batman-metro-vila-madalena.html",
    f"{BASE_URL}/2026/05/ccsp-o-que-fazer-no-centro-cultural.html",

    # Posts — 2026 June
    f"{BASE_URL}/2026/06/metro-moema-linha-5-lilas-ibirapuera-pavilhao-japones.html",
    f"{BASE_URL}/2026/06/museu-ipiranga-parque-independencia-metro-linha-5.html",
    f"{BASE_URL}/2026/06/cemiterio-consolacao-metro-sao-paulo.html",
    f"{BASE_URL}/2026/06/instituto-tomie-ohtake-metro-faria-lima.html",
    f"{BASE_URL}/2026/06/zoologico-sp-metro-jabaquara-orca-zoo-como-chegar.html",
    f"{BASE_URL}/2026/06/memorial-america-latina-metro-barra-funda-como-chegar.html",
    f"{BASE_URL}/2026/06/museu-da-imigracao-metro-bras.html",
    f"{BASE_URL}/2026/06/parque-da-juventude-metro-carandiru.html",
    f"{BASE_URL}/2026/06/instituto-butantan-metro-butanta.html",
    f"{BASE_URL}/2026/06/mercado-de-pinheiros-metro-faria-lima.html",
    f"{BASE_URL}/2026/06/higienopolis-metro-higienopolis-mackenzie.html",
    f"{BASE_URL}/2026/06/santa-cecilia-metro-guia-bairro.html",

    # Posts — 2026 July
    f"{BASE_URL}/2026/07/farol-santander-metro-sao-bento.html",
    f"{BASE_URL}/2026/07/arena-corinthians-metro-itaquera.html",
    f"{BASE_URL}/2026/07/santo-amaro-metro-linha-5-lilas.html",
    f"{BASE_URL}/2026/07/parque-estadual-cantareira-metro-tucuruvi.html",
    f"{BASE_URL}/2026/07/bras-feira-da-madrugada-metro.html",
    f"{BASE_URL}/2026/07/museu-do-crime-metro-santa-cecilia.html",
    f"{BASE_URL}/2026/07/museu-do-futebol-metro-higienopolis-mackenzie.html",
    f"{BASE_URL}/2026/07/museu-arte-sacra-metro-tiradentes.html",
    f"{BASE_URL}/2026/07/sala-sao-paulo-metro-luz.html",
]

# Deduplicate
URLS = list(dict.fromkeys(URLS))


def submit_batch(urls: list[str]) -> dict:
    """Submit a batch of URLs to IndexNow."""
    payload = {
        "host": HOST,
        "key": API_KEY,
        "keyLocation": f"{BASE_URL}/{API_KEY}.txt",
        "urlList": urls,
    }
    response = requests.post(
        ENDPOINT,
        headers={"Content-Type": "application/json; charset=utf-8"},
        data=json.dumps(payload),
        timeout=30,
    )
    return {"status": response.status_code, "text": response.text}


def main():
    print(f"IndexNow submission — {len(URLS)} URLs → {HOST}\n")

    # IndexNow accepts up to 10,000 URLs per request but 10 is a safe batch
    BATCH_SIZE = 10
    batches = [URLS[i:i+BATCH_SIZE] for i in range(0, len(URLS), BATCH_SIZE)]

    success = 0
    errors  = 0

    for i, batch in enumerate(batches, 1):
        print(f"Batch {i}/{len(batches)} ({len(batch)} URLs)...")
        result = submit_batch(batch)
        status = result["status"]

        if status in (200, 202):
            print(f"  ✓ HTTP {status} — accepted")
            success += len(batch)
        elif status == 422:
            print(f"  ⚠ HTTP 422 — one or more URLs invalid (check format)")
            errors += len(batch)
        elif status == 429:
            print(f"  ⚠ HTTP 429 — rate limited. Waiting 60s...")
            time.sleep(60)
            # Retry once
            result = submit_batch(batch)
            if result["status"] in (200, 202):
                print(f"  ✓ Retry succeeded")
                success += len(batch)
            else:
                print(f"  ✗ Retry failed: {result['status']}")
                errors += len(batch)
        else:
            print(f"  ✗ HTTP {status}: {result['text'][:200]}")
            errors += len(batch)

        if i < len(batches):
            time.sleep(2)  # polite pause between batches

    print(f"\nDone. {success} submitted, {errors} errors.")
    if errors:
        print("Check that the key file is live at:")
        print(f"  {BASE_URL}/{API_KEY}.txt")


if __name__ == "__main__":
    main()
