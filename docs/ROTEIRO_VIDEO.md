# Roteiro para vídeo curto de demonstração (2min30s)

Grave a tela em 1920×1080, com microfone ligado. Antes de gravar, execute `python app.py` e abra `http://localhost:8000`.

| Tempo | Imagem na tela | Narração sugerida |
|---:|---|---|
| 0:00–0:12 | Página inicial do CineMatch | “Este é o CineMatch, um recomendador de filmes por filtragem colaborativa.” |
| 0:12–0:38 | Criar perfil: nome, gêneros e três filmes | “A pessoa cria seu próprio perfil, informa gêneros favoritos e avalia filmes conhecidos. Itens já avaliados são removidos antes da recomendação.” |
| 0:38–0:58 | Destacar score, gêneros e vizinhos | “Cada cartão exibe a previsão, os gêneros e o suporte de vizinhos. Isto torna a decisão mais transparente.” |
| 0:58–1:20 | Buscar filme, escolher nota 5 e salvar | “Uma nova avaliação é salva localmente e atualiza o perfil. O usuário pode, assim, ajustar suas próximas recomendações.” |
| 1:20–1:43 | Novo perfil apenas com gêneros | “Para uma pessoa sem filmes avaliados, o sistema usa seus gêneros e a média bayesiana da comunidade.” |
| 1:43–2:03 | Adicionar três filmes e atualizar | “Após evidência suficiente, a filtragem colaborativa passa a contribuir para a lista.” |
| 2:03–2:20 | Formulário de feedback | “Ao final, a pessoa avalia a utilidade das recomendações de um a cinco e pode deixar um comentário para a avaliação do sistema.” |
| 2:20–2:30 | `results/RESULTADOS.md` | “A avaliação reproduzível separa treino e teste por usuário e registra MAE, RMSE e métricas de Top-10. O código, resultados e relatório estão no repositório.” |

## Checklist antes de enviar

- [ ] Conferir que a URL e os textos estão legíveis.
- [ ] Mostrar criação de perfil, recomendações e início frio.
- [ ] Não expor dados pessoais ou notificações do computador.
- [ ] Exportar em MP4, até 3 minutos, e publicar o link no README ou na submissão da disciplina.
