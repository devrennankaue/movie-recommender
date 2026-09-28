# CineMatch: recomendação personalizada de filmes por filtragem colaborativa

**Disciplina:** preencher.  
**Equipe:** preencher.  
**Data:** 27 de setembro de 2026.

## Resumo

O CineMatch é uma aplicação local para recomendar filmes a partir de avaliações explícitas. O sistema usa filtragem colaborativa baseada em usuários para estimar a nota de filmes ainda desconhecidos e uma média bayesiana para o caso de início frio. Em uma divisão reproduzível por usuário do MovieLens 100K, o modelo colaborativo obteve MAE de 0,7567 e RMSE de 0,9753, menores que a referência de média bayesiana. A interface permite consultar histórico, recomendar, registrar avaliações e coletar a percepção de participantes.

## 1. Objetivo e problema

Catálogos extensos tornam a escolha de filmes cansativa. O objetivo foi criar um recomendador que, dado o histórico de notas de uma pessoa, encontre filmes não vistos com maior chance de agradá-la. O sistema deve também continuar útil para uma pessoa sem histórico e possibilitar avaliação por usuários de teste.

## 2. Fundamentação

Na filtragem colaborativa, preferências de pessoas com comportamentos parecidos ajudam a prever preferências ausentes. Para cada usuário-alvo `u`, calculamos a similaridade cosseno entre o vetor de notas centralizado pela média desse usuário e o vetor de cada candidato a vizinho. A predição de um filme `i` é a média do alvo acrescida da média ponderada dos desvios de nota dos vizinhos:

`r̂(u,i) = μu + Σv sim(u,v)(r(v,i) − μv) / Σv |sim(u,v)|`.

Foram usados os 40 vizinhos mais similares, pelo menos dois filmes em comum e regularização `c/(c+10)`, em que `c` é o número de coavaliações. Essas escolhas reduzem a influência de coincidências com pouco suporte. Quando o perfil tem menos de duas avaliações ou não possui vizinhos utilizáveis, a aplicação ordena filmes por média bayesiana, que suaviza a média de cada filme em direção à média global usando peso prévio 20.

## 3. Dados e preparação

Foi usado MovieLens 100K, do GroupLens Research: 100.000 notas de 1 a 5 dadas por 943 usuários a 1.682 filmes entre setembro de 1997 e abril de 1998. Cada usuário tem ao menos 20 avaliações. O arquivo `u.data` contém usuário, item, nota e instante; `u.item` acrescenta título e gêneros.

A preparação remove linhas inválidas, mantém somente notas de 1 a 5 e, se houvesse uma dupla usuário–filme repetida, preservaria a interação mais recente. No arquivo empregado não houve perda: 100.000 interações limpas. A matriz usuário × filme é esparsa e valores ausentes não são convertidos em zero como se fossem uma nota. Os dados são baixados pela fonte oficial e não entram no repositório.

## 4. Método experimental

A semente 42 seleciona cerca de 20% das avaliações de cada usuário para teste, com pelo menos uma avaliação de teste. Restaram 80.367 interações de treino e 19.633 de teste. Nenhuma avaliação de teste aparece no perfil entregue ao modelo. A referência é a média bayesiana de popularidade, que ignora personalização.

MAE é a média do erro absoluto de notas previstas; RMSE penaliza erros grandes. Para a lista Top-10, um filme do teste é relevante quando a nota real é pelo menos 4. Precision@10 mede a fração de acertos na lista, Recall@10 mede a fração de filmes relevantes encontrados, e NDCG@10 dá mais peso ao acerto nas primeiras posições. Cobertura é a fração do catálogo de treino que apareceu em ao menos uma lista Top-10. As métricas de ranking são médias macro dos 927 usuários que tinham item relevante no teste.

## 5. Resultados

| Modelo | MAE ↓ | RMSE ↓ | Precision@10 ↑ | Recall@10 ↑ | NDCG@10 ↑ | Cobertura@10 ↑ |
|---|---:|---:|---:|---:|---:|---:|
| Filtragem colaborativa user-kNN | 0,7567 | 0,9753 | 0,0193 | 0,0136 | 0,0223 | 0,4945 |
| Média bayesiana | 0,8310 | 1,0344 | 0,0836 | 0,0631 | 0,0980 | 0,0231 |

O método colaborativo reduz MAE em 8,9% e RMSE em 5,7% frente à referência, portanto estima notas com mais precisão. A referência supera o modelo nas métricas de Top-10, pois títulos muito populares são uma referência forte no MovieLens e a base é esparsa. Em contrapartida, o modelo colaborativo recomenda aproximadamente 49,5% do catálogo, contra 2,3%, sinal de maior diversidade entre usuários. Não é adequado afirmar, apenas com esses números, que a qualidade percebida será maior: o teste com pessoas complementa a análise.

Cinco exemplos completos — histórico de treino, Top-10, acertos e métricas — estão em [`results/RESULTADOS.md`](../results/RESULTADOS.md). O usuário 1 alcançou Precision@10 de 0,20 e NDCG@10 de 0,359; os usuários 2–5 evidenciam que o desempenho varia de acordo com o tamanho e a compatibilidade do perfil. O arquivo `results/evaluation.json` preserva os números brutos, parâmetros, hash do dataset e ambiente de execução.

## 6. Avaliação com usuários de teste

A interface registra uma nota de utilidade de 1 a 5 e comentário. O protocolo de coleta está em [`docs/TESTE_COM_USUARIOS.md`](TESTE_COM_USUARIOS.md). Este repositório não fabrica respostas humanas: a subseção de resultados qualitativos deve ser preenchida apenas depois da aplicação do protocolo a pelo menos cinco participantes. Para cada participante, registrar ID fictício, número de filmes avaliados, nota de utilidade, se escolheria algum item recomendado e comentário. Relatar média e desvio-padrão da utilidade e a proporção de participantes que escolheriam ao menos um filme.

## 7. Limitações

Os dados são antigos, contêm só notas explícitas e não representam o público atual. Similaridade baseada em coavaliações sofre com esparsidade e início frio. A nota prevista não é garantia de interesse real e a avaliação offline assume que itens não observados no teste são irrelevantes, o que subestima listas boas. O algoritmo também não considera contexto, disponibilidade de streaming, idioma, diversidade intencional ou possíveis vieses de popularidade.

## 8. Conclusão

O CineMatch cumpre o fluxo de um recomendador: prepara interações, personaliza por filtragem colaborativa, exclui itens conhecidos, atende início frio, permite nova avaliação e coleta feedback. O experimento mostra ganho nas previsões de nota e ganho claro de cobertura, mas evidencia que o ranking precisa de melhorias. Uma evolução razoável seria combinar o score colaborativo com popularidade regularizada e reordenar a lista para diversidade, validando-a novamente com participantes.

## Referências

HARPER, F. M.; KONSTAN, J. A. The MovieLens Datasets: History and Context. *ACM Transactions on Interactive Intelligent Systems*, 5(4), 2015. DOI: 10.1145/2827872.

GROUPLENS RESEARCH. *MovieLens 100K Dataset*. Disponível em: <https://grouplens.org/datasets/movielens/100k/>. Acesso em: 27 set. 2026.
