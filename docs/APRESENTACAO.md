# Apresentação — CineMatch (10 minutos)

Preencha os nomes da equipe na capa. Esta estrutura cabe em 10 minutos; ajuste proporcionalmente se a disciplina tiver outro tempo.

## Slide 1 — Problema e objetivo (0:45)

**No slide:** “Como escolher um filme em um catálogo grande?”; objetivo: recomendar itens ainda desconhecidos a partir de avaliações semelhantes.

**Fala:** “Escolhemos o domínio de filmes porque a decisão é frequente e o catálogo é amplo. O CineMatch recebe avaliações, consulta o histórico e gera uma lista personalizada. Também trata a pessoa que ainda não avaliou nada.”

## Slide 2 — Dados (1:00)

**No slide:** MovieLens 100K; 100.000 avaliações de 1–5; 943 usuários; 1.682 filmes; setembro de 1997 a abril de 1998.

**Fala:** “A interação é uma nota explícita. Removemos registros inválidos e usamos título e gêneros apenas para exibir a interface; o modelo aprende exclusivamente da relação usuário–filme.”

## Slide 3 — Método (1:15)

**No slide:** matriz esparsa → média por usuário → similaridade cosseno → 40 vizinhos → score → retirar itens conhecidos. Fluxo alternativo: sem histórico → média bayesiana.

**Fala:** “Centralizar as notas evita que uma pessoa que sempre dá cinco pareça idêntica a outra que sempre dá três. Exigimos ao menos dois filmes em comum e reduzimos similaridades com pouco suporte.”

## Slide 4 — Demonstração: perfil com histórico (1:40)

**Ação:** executar `python app.py`; abrir `localhost:8000`; criar um perfil, escolher gêneros e avaliar três filmes; apontar histórico e Top-10; mostrar que um título já avaliado não aparece na lista.

**Fala:** “A coluna da esquerda apresenta o histórico. À direita, a interface informa o score e se veio de vizinhos. O filtro de candidatos remove os filmes do histórico antes de ordenar.”

## Slide 5 — Demonstração: nova avaliação (1:00)

**Ação:** buscar um filme, dar nota e salvar; clicar Atualizar; mostrar a lista recalculada.

**Fala:** “A avaliação fica persistida localmente e passa a compor o perfil. Isto também permite realizar o estudo com participantes.”

## Slide 6 — Demonstração: início frio (0:50)

**Ação:** criar outro perfil, escolher gêneros e não adicionar filmes; mostrar a média da comunidade; adicionar ao menos três filmes e atualizar.

**Fala:** “Sem duas avaliações não é possível achar vizinhos de forma confiável, portanto apresentamos títulos com melhor média bayesiana. Depois de obter evidências, a filtragem colaborativa é ativada.”

## Slide 7 — Avaliação offline (1:35)

**No slide:** tabela abaixo e nota “80/20 por usuário, semente 42; teste nunca usado no treino”.

| Modelo | MAE | RMSE | Precision@10 | NDCG@10 | Cobertura |
|---|---:|---:|---:|---:|---:|
| User-kNN | 0,7567 | 0,9753 | 0,0193 | 0,0223 | 49,45% |
| Média bayesiana | 0,8310 | 1,0344 | 0,0836 | 0,0980 | 2,31% |

**Fala:** “O modelo colaborativo melhora as previsões de nota, mas a referência de popularidade é mais forte em Top-10. O principal ganho da colaboração é oferecer muito mais itens do catálogo. Mostramos cinco exemplos detalhados no relatório, sem esconder usuários com resultado fraco.”

## Slide 8 — Teste com usuários, limites e conclusão (1:55)

**No slide:** formulário 1–5 + comentário; limitações: base antiga, esparsidade, início frio e viés de popularidade; próximos passos: híbrido e diversidade.

**Fala:** “A avaliação humana mede utilidade percebida e intenção de assistir. Não substituímos pessoas por números inventados: o formulário está integrado e a planilha de coleta está no repositório. O sistema está funcional, reproduzível e mostra claramente onde o ranking pode evoluir.”

## Reserva para perguntas (1:00)

Deixe a aplicação aberta em um perfil recém-criado e o arquivo `results/RESULTADOS.md` disponível para responder sobre exemplos e métricas.
