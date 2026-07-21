# Reinserção Amazon Associates — APÓS aprovação do AdSense

> Esta pasta (`scripts/`) está excluída do build do Jekyll — este arquivo não é publicado.
> Os blocos originais estão preservados no histórico git (commits anteriores a jul/2026).

## Regras para a reinserção (o que mudou vs. versão removida)

1. **Nunca** usar âncora de texto que descreva outra coisa (ex.: "concertos" → câmera). A âncora deve nomear o produto real.
2. **Máximo 1 bloco por post**, no final, com o disclosure já usado ("Links de parceiro Amazon…").
3. **Sem links contextuais no corpo** — foi o principal fator de risco na revisão AdSense.
4. Manter `rel="nofollow sponsored"` e o pixel apenas dentro do bloco.
5. Só inserir produto se fizer sentido real para o passeio do post.

## Mapeamento produto → tipo de post (tag: rotademetr027-20)

| Produto | ASIN | Usar em posts de |
|---|---|---|
| Garrafa térmica | B076QFL95Z | Parques e trilhas: Ibirapuera, Cantareira, Horto, Carmo, Aclimação, Juventude, Trianon |
| Protetor solar | B079ZS4Z5Z | Parques abertos e caminhadas longas: Ibirapuera, Cantareira, Carmo, Horto, roteiros de bairro |
| Repelente | B0CSDVGBXW | Trilhas e mata: Cantareira, Horto, Butantan, Carmo |
| Binóculo | B0FK31RF9G | Observação: Cantareira (aves/mirante), Horto, Igreja da Penha (vista), Farol Santander |
| Mochila | B08CNM64R1 | Roteiros de dia inteiro: guias de bairro (Liberdade, Pinheiros, Santa Cecília, Higienópolis, Santo Amaro), Feira da Madrugada |
| Livro Guia SP | 8579144736 | Posts culturais do centro: Sé, São Bento, Luz, Theatro Municipal, Mosteiro, Pátio do Colégio, museus do centro |
| Câmera 4K | B0FVL1VWRS | Apenas posts visuais onde filmar é plausível: Beco do Batman, Minhocão/Santa Cecília, mirantes. **Não** usar em museus (fotografia restrita) nem salas de concerto |

## Posts SEM produto adequado (deixar sem bloco)

- Sala São Paulo, Theatro Municipal (concerto ≠ produto de viagem; livro Guia SP no máximo)
- Museu do Crime (fotografia restrita, tom sério)
- Cemitério da Consolação (tom inadequado para venda)

## Imagens CDN (já validadas)

```
B0FVL1VWRS: https://m.media-amazon.com/images/I/61RF-YfqtAL._SL200_.jpg
B08CNM64R1: https://m.media-amazon.com/images/I/51+2HsZC80L._SL200_.jpg
B076QFL95Z: https://m.media-amazon.com/images/I/51gBQgKzK7L._SL200_.jpg
B0FK31RF9G: https://m.media-amazon.com/images/I/41DcIMtdoxL._SL200_.jpg
B079ZS4Z5Z: https://m.media-amazon.com/images/I/517yDtlJjhL._SL200_.jpg
B0CSDVGBXW: https://m.media-amazon.com/images/I/51zLwdwkdnL._SL200_.jpg
8579144736: https://m.media-amazon.com/images/I/81Yw6xzbNkL._SL200_.jpg
```
