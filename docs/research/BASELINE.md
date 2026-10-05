# Baseline e proveniência da extensão

Registro em 2026-10-05 antes de alterações da trilha de pesquisa.

- Branch `implementation`; HEAD `f908afcbe483167bd0de40cef26fff6e92d26dfd`.
- Estado inicial: `benchmark/HUMAN_REVIEW.json` removido (alteração preexistente); `docs/RESEARCH-AUDIT-2026-10-05.md` e `docs/superpowers/` não rastreados (preexistentes). Não restaurar, apagar ou editar esses itens.
- `scripts/verify_evidence.py`: exit 0, “All input, scientific source and evidence hashes verified”. Executado nesta sessão.
- IDs registrados em `reference/environment.json`: Python inicial `sha256:13b69b245a31c45a9ab9c37d319797b1c25b1a9f3145286c8e601db3d500cd97`; R de referência `sha256:be72a4cb6b900259697fd30c5253ebeabe2c8ded98b2ae82a54a28f904d22706`; R validada `sha256:ad8eb7fc6c64ca4fc5535e50034db232822c0de4b5ba82ce1e214d6735736c58`; Python científica `sha256:5d61a9a0192f6a4128a5b135ac833ee94c65b0027142d8b34857760e64560eec`; CI baseline `sha256:4a0c28c913eb937bece661f05d26389a0f3a7222857500804f57f78013f4347d`; participante `sha256:dc7aa8d4f631ca4fc5535e50034db232822c0de4b5ba82ce1e214d6735736c58`.
- Imagens E0 construídas sem atualizar as bases: Python pesquisa `sha256:fa5709341bef9077bcc81677191fa94a0c2e815f004d83701aed6f61818378e4`; R pesquisa `sha256:f63cb28be3ec39dd5fecdc5102fc566e21877314451889dcd1e94f891ce5ec06`. A imagem R conserva R 4.5.2/Bioconductor 3.22/DESeq2 1.50.2; lock de 218 pacotes em `research/r-packages.lock.csv`, comparado no build.
- SHA-256 atuais: `data/counts.csv` `69D93E59052F921CEA64B82F9B207AEBDE9D6B9532A9D12CDBA4A06AD5391736`; `data/metadata.csv` `285C9BB58AC5CCEF7345906158D3F2F4F88A0C0489E939D8FD639FA02C7BBC8D`; `data/annotation.csv` `3219D6B73D51CF6DE99BA3C9EF7D99F728C737781746EE47FB1DA368855D07DE`; `reference/comparison.json` `4658A61B32186C25E2B7F10959AE594A2FA15356AE55DC42158B8F078247F5B6`; `evidence/analysis-summary.json` `627766D7975CEAFEEFB0D31F50ABB241B533EF53E490C609F65A53E9F6D606F1`.
- Os resultados tabulares históricos e contagens de discordância estão descritos no plano e auditoria; não são uma reexecução do ajuste nesta etapa.
- A primeira consulta a `docker info` foi negada pelo sandbox; uma consulta de leitura autorizada pelo auto-review funcionou. `Rscript` não está no host. As extensões foram executadas somente nas imagens separadas; nenhum pacote foi instalado no host.

## Limites e retomada

Os IDs de referência são registros de `reference/environment.json`; os IDs E0 são imagens locais construídas nesta execução. O verificador valida hashes de evidências, não reexecuta modelos. Nunca substituir a baseline por resumos históricos.
