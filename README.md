# CineMatch — recomendador colaborativo de filmes

Aplicação web local que recomenda filmes a partir das avaliações dos perfis criados no próprio site. O catálogo usado pela interface é `data/ml-100k/world_imdb_movies_top_movies_per_year.csv`, com 33.600 filmes do IMDb.

## Funcionalidades

- criação de perfil com nome, gêneros favoritos e filmes avaliados;
- recomendações Top-10 sem filmes que o usuário já avaliou;
- filtragem colaborativa entre os perfis criados no site, com similaridade cosseno e mínimo de 2 filmes em comum;
- alternativa de início frio baseada nos gêneros escolhidos e na nota do catálogo IMDb;
- novas avaliações persistidas em SQLite e usadas na próxima recomendação;
- formulário de utilidade para teste com participantes;
- experimento reproduzível com MAE, RMSE, Precision@10, Recall@10, NDCG@10 e cobertura.

## Como executar

Pré-requisito: Python 3.10 ou superior. A única dependência externa é NumPy.

```powershell
python app.py
```

Abra `http://localhost:8000`, crie um perfil e escolha ao menos um gênero. Adicionar três ou mais filmes conhecidos com notas torna a recomendação colaborativa mais específica. No primeiro uso, a página pode levar alguns segundos para calcular a similaridade.

O arquivo de catálogo esperado é `data/ml-100k/world_imdb_movies_top_movies_per_year.csv`. A aplicação não usa os usuários ou avaliações do MovieLens; todas as avaliações usadas na recomendação são criadas pelos usuários do site e salvas localmente em `feedback.sqlite3`.

## Estrutura

| Caminho | Finalidade |
|---|---|
| `recommender.py` | carga, preparação e algoritmo de recomendação |
| `app.py` | servidor e API local; grava feedback em `feedback.sqlite3` |
| `web/` | interface HTML, CSS e JavaScript |
| `evaluate.py` | divisão treino/teste e métricas reproduzíveis |
| `results/RESULTADOS.md` | números do experimento e cinco exemplos de usuários |
| `docs/RELATORIO.md` | relatório acadêmico |
| `docs/APRESENTACAO.md` | roteiro dos slides e fala |
| `docs/ROTEIRO_VIDEO.md` | roteiro de demonstração curta |
| `docs/TESTE_COM_USUARIOS.md` | protocolo de avaliação com participantes |

## Reproduzir a avaliação

`python evaluate.py` fixa a semente em 42 e separa, para cada usuário, aproximadamente 80% das avaliações para treino e 20% para teste. A divisão impede que uma avaliação de teste seja usada para treinar ou para compor o histórico do usuário. Os arquivos gerados em `results/` registram parâmetros, hash SHA-256 de `u.data`, ambiente e resultados individuais.

Para não tratar itens desconhecidos como negativos de forma incorreta, a interpretação das métricas de ranking é conservadora: apenas filmes com nota real ≥ 4 no teste contam como relevantes; todo item recomendado que não aparece nessa lista deixa de contar como acerto, ainda que o usuário pudesse gostar dele.

## Citação dos dados

HARPER, F. M.; KONSTAN, J. A. The MovieLens Datasets: History and Context. *ACM Transactions on Interactive Intelligent Systems*, 5(4), 2015. DOI: [10.1145/2827872](https://doi.org/10.1145/2827872).
