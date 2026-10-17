# Relatório — Negócio online autônomo (v0.1, 16/10/2026)

## Pesquisa (resumo)
- Demanda internacional por profissionais brasileiros +53% em 2025 (Deel; Estadão, Exame). Média de US$ 53 mil/ano para remotos no Brasil, a maior da América Latina (Bloomberg Línea, H1/2026).
- Modelos comprovados lá fora: job boards remotos (Remote OK, WeWorkRemotely, Remotive) monetizam com anúncios pagos de vagas e planos pagos; newsletters de nicho com plano pago.
- Em PT-BR: existem comunidades e conteúdo, mas pouco agregador diário, gratuito e focado em "vagas abertas a quem mora no Brasil".
- Viabilidade técnica: APIs públicas e gratuitas da Remotive e da Remote OK. Ambas exigem atribuição e link para a vaga original. A Remotive proíbe esconder vagas atrás de cadastro e repassá-las ao Google Jobs ou LinkedIn.
Fontes: estadao.com.br (procura por brasileiros +53%), exame.com, bloomberglinea.com.br, deel.com/pt/blog/relatorio-contratar-talentos-no-brasil, remotive.com/remote-jobs/api, remoteok.featurebase.app (API).

## Pontuação (1 a 5; 5 = melhor)
| Ideia | Demanda BR | Concorrência | Autonomia | Custo | Risco legal | Tempo até a 1ª receita | Total |
|---|---|---|---|---|---|---|---|
| **Vagas em Dólar** (agregador + newsletter + Pro) | 5 | 4 | 5 | 5 | 4 | 3 | **26** |
| Diretório de ferramentas de IA em PT-BR | 4 | 3 | 5 | 5 | 5 | 2 | 24 |
| Newsletter "IA para PMEs" com plano pago | 4 | 3 | 4 | 5 | 5 | 2 | 23 |
| Templates de FP&A/planejamento (Excel/Notion) | 3 | 4 | 4 | 5 | 5 | 3 | 24 |
| Micro-SaaS de currículo em inglês com IA | 4 | 2 | 4 | 3 | 4 | 3 | 20 |

**Escolhida:** Vagas em Dólar. Tem a demanda mais forte, os dados são grátis e roda 100% por cron. Não é conselho financeiro.

## O que foi construído (/workspace/online-business)
- `src/build.py`: busca vagas nas duas APIs, filtra as abertas a Worldwide/LATAM/Brasil, remove duplicadas e gera `site/index.html`, `site/jobs.json` e `site/newsletter.md`. Testado: 55 vagas reais na rodada de 16/10/2026, 23:04 (Brasília).
- `src/template.html`: página em PT-BR com chamadas para o plano Pro (R$ 19/mês), a newsletter grátis e o anúncio de vagas para empresas (US$ 99).
- `.github/workflows/build.yml`: GitHub Actions roda 2x por dia (06h e 18h, Brasília) e publica no GitHub Pages, de graça.

## Como roda sozinho
O cron do Actions busca as vagas, gera o site e publica. A edição semanal da newsletter já sai pronta em `newsletter.md`. Para enviar, falta ligar a API de um provedor (Buttondown ou Beehiiv). Por enquanto não há nenhum custo.

## Monetização
1. Anúncio de vaga por empresas: US$ 99 por 30 dias (checkout Stripe).
2. Plano Pro: R$ 19/mês, com alertas por área e salário convertido para R$ líquido PJ (checkout Stripe/Mercado Pago).
3. Patrocínio da newsletter (fintechs de câmbio e contabilidade PJ), quando passar de 2 mil inscritos.

## O que só o João pode fornecer
1. Uma conta no GitHub (ou acesso a um repositório) para hospedar o código e ativar o Pages e o Actions.
2. Domínio: vagasemdolar.com.br no Registro.br (cerca de R$ 40/ano, exige CPF/CNPJ). Opcional no começo.
3. Conta grátis no provedor de newsletter (Buttondown ou Beehiiv) e a API key dele.
4. Conta Stripe ou Mercado Pago (exige CPF/CNPJ e conta bancária) para os links de pagamento. A CNPJ da CTI ou um MEI resolve a nota fiscal.
5. Um e-mail de contato público, além de aprovar a política de privacidade (LGPD) e os termos de uso.
6. Opcional: perfis no X/LinkedIn para postar as vagas automaticamente (tokens de API).
