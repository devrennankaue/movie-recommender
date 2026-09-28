# Resultados experimentais

Gerado por `python evaluate.py`. Dados de teste nunca entram no modelo.

Treino: 80367; teste: 19633; semente: 42.

| Modelo | MAE ↓ | RMSE ↓ | Precision@10 ↑ | Recall@10 ↑ | NDCG@10 ↑ | Cobertura ↑ |
|---|---:|---:|---:|---:|---:|---:|
| user_knn | 0.7567 | 0.9753 | 0.0193 | 0.0136 | 0.0223 | 0.4945 |
| media_bayesiana | 0.8310 | 1.0344 | 0.0836 | 0.0631 | 0.0980 | 0.0231 |

Ranking: média macro apenas dos usuários com ao menos um item relevante no teste. Relevante = nota ≥ 4; candidatos = todos os filmes observados no treino e desconhecidos do usuário. Itens não avaliados no teste contam como não acertos, embora possam ser relevantes na prática.

## Usuário 1

Histórico de treino: 218; teste: 54; relevantes: 27.

Amostra do histórico: Star Trek: First Contact (1996) (4/5); Smilla's Sense of Snow (1997) (2/5); Doom Generation, The (1995) (2/5); Field of Dreams (1989) (3/5); Glengarry Glen Ross (1992) (4/5).

Métricas: precision@10 = 0.2000, recall@10 = 0.0741, ndcg@10 = 0.3590.

| Filme recomendado | Estimativa | Acerto no teste |
|---|---:|---|
| Maya Lin: A Strong Clear Vision (1994) | 5.00 | Sim |
| Wrong Trousers, The (1993) | 5.00 | Sim |
| Fear of a Black Hat (1993) | 5.00 | Não |
| Touch of Evil (1958) | 5.00 | Não |
| High Noon (1952) | 5.00 | Não |
| Braindead (1992) | 5.00 | Não |
| Anna Karenina (1997) | 5.00 | Não |
| Die xue shuang xiong (Killer, The) (1989) | 5.00 | Não |
| Gaslight (1944) | 5.00 | Não |
| 8 1/2 (1963) | 5.00 | Não |

## Usuário 2

Histórico de treino: 50; teste: 12; relevantes: 8.

Amostra do histórico: Mrs. Brown (Her Majesty, Mrs. Brown) (1997) (4/5); Air Force One (1997) (4/5); Bed of Roses (1996) (3/5); English Patient, The (1996) (4/5); Men in Black (1997) (4/5).

Métricas: precision@10 = 0.0000, recall@10 = 0.0000, ndcg@10 = 0.0000.

| Filme recomendado | Estimativa | Acerto no teste |
|---|---:|---|
| Patton (1970) | 5.00 | Não |
| Misérables, Les (1995) | 5.00 | Não |
| Rebecca (1940) | 5.00 | Não |
| Victor/Victoria (1982) | 5.00 | Não |
| Thin Blue Line, The (1988) | 5.00 | Não |
| Love Jones (1997) | 5.00 | Não |
| Soul Food (1997) | 5.00 | Não |
| Eve's Bayou (1997) | 5.00 | Não |
| Beautiful Thing (1996) | 5.00 | Não |
| Boy's Life 2 (1997) | 5.00 | Não |

## Usuário 3

Histórico de treino: 44; teste: 10; relevantes: 4.

Amostra do histórico: L.A. Confidential (1997) (2/5); Wedding Singer, The (1998) (3/5); Schindler's List (1993) (4/5); In the Name of the Father (1993) (2/5); Paradise Lost: The Child Murders at Robin Hood Hills (1996) (5/5).

Métricas: precision@10 = 0.0000, recall@10 = 0.0000, ndcg@10 = 0.0000.

| Filme recomendado | Estimativa | Acerto no teste |
|---|---:|---|
| Microcosmos: Le peuple de l'herbe (1996) | 4.49 | Não |
| Dazed and Confused (1993) | 4.49 | Não |
| Chungking Express (1994) | 4.47 | Não |
| Hard Eight (1996) | 4.47 | Não |
| Big Lebowski, The (1998) | 4.37 | Não |
| Crow, The (1994) | 4.37 | Não |
| Year of the Horse (1997) | 4.36 | Não |
| Hugo Pool (1997) | 4.36 | Não |
| Casino (1995) | 4.35 | Não |
| Duoluo tianshi (1995) | 4.32 | Não |

## Usuário 4

Histórico de treino: 20; teste: 4; relevantes: 1.

Amostra do histórico: Mimic (1997) (3/5); Assignment, The (1997) (5/5); One Flew Over the Cuckoo's Nest (1975) (4/5); In & Out (1997) (5/5); Scream (1996) (4/5).

Métricas: precision@10 = 0.0000, recall@10 = 0.0000, ndcg@10 = 0.0000.

| Filme recomendado | Estimativa | Acerto no teste |
|---|---:|---|
| Twelve Monkeys (1995) | 5.00 | Não |
| Babe (1995) | 5.00 | Não |
| Dead Man Walking (1995) | 5.00 | Não |
| Richard III (1995) | 5.00 | Não |
| Usual Suspects, The (1995) | 5.00 | Não |
| Mighty Aphrodite (1995) | 5.00 | Não |
| Postino, Il (1994) | 5.00 | Não |
| Braveheart (1995) | 5.00 | Não |
| Taxi Driver (1976) | 5.00 | Não |
| Brothers McMullen, The (1995) | 5.00 | Não |

## Usuário 5

Histórico de treino: 140; teste: 35; relevantes: 11.

Amostra do histórico: Adventures of Priscilla, Queen of the Desert, The (1994) (5/5); Blues Brothers, The (1980) (5/5); Beverly Hills Cop III (1994) (2/5); Body Snatcher, The (1945) (3/5); Santa Clause, The (1994) (1/5).

Métricas: precision@10 = 0.0000, recall@10 = 0.0000, ndcg@10 = 0.0000.

| Filme recomendado | Estimativa | Acerto no teste |
|---|---:|---|
| Steel (1997) | 4.75 | Não |
| Go Fish (1994) | 4.75 | Não |
| Great Day in Harlem, A (1994) | 4.75 | Não |
| Two or Three Things I Know About Her (1966) | 4.75 | Não |
| Ice Storm, The (1997) | 4.75 | Não |
| Hearts and Minds (1996) | 4.75 | Não |
| Career Girls (1997) | 4.75 | Não |
| Life Less Ordinary, A (1997) | 4.75 | Não |
| Dangerous Beauty (1998) | 4.75 | Não |
| Anne Frank Remembered (1995) | 4.73 | Não |

## Usuário sem histórico

Recebe a média bayesiana por filme. Não há personalização até existirem evidências suficientes.

Schindler's List (1993), Casablanca (1942), Shawshank Redemption, The (1994), Star Wars (1977), Wrong Trousers, The (1993).
