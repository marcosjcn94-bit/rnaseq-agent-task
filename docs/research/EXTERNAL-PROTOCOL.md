# E5 — auditoria externa GSE13168

Estado: `insufficient_metadata`; nenhuma inferência executada.

## Seleção congelada

Contraste planejado: três pares GFP basal/Flu (GSM332914/332925, GSM332915/332926, GSM332916/332927), GPL96. Endpoints definidos antes da análise: LFC e IC95% para CRISPLD2, DUSP1 e KLF15; concordância global e CAMERA seriam exploratórios. Sem exigência de igualdade de magnitude e sem alegação de novidade.

| Doador no registro | Basal | Flu |
|---|---|---|
| 2 | GSM332914 | GSM332925 |
| 3 | GSM332915 | GSM332926 |
| 4 | GSM332916 | GSM332927 |

## Auditoria e decisão

SOFT e MINiML da série e seis CEL foram baixados do GEO/NCBI FTP. Hashes e extração allowlist estão em `.artifacts/research/E5/extracted/`. A auditoria confirma as seis GSM, GPL96 e os pares pelo campo `donorN` nos títulos. Os protocolos descrevem pré-tratamento de 10 nM fluticasona por 30 min e coleta após 8 h de estímulo, mas não atribuem inequivocamente o estímulo/citocina a cada registro selecionado. Os títulos “basal” e “Flu” não eliminam essa lacuna de contexto.

Decisão anterior à inferência: `insufficient_metadata`. A comparação pretendida pode misturar estímulos distintos, portanto não será ajustado um modelo para esse contraste. Os arquivos CEL foram preservados, sem processamento RMA; construir a imagem RMA não constitui resultado. O desenho também difere de AIRWAY (dexametasona 1 µM/18 h; RNA-seq), e IDs anônimos não estabelecem independência entre doadores.

O identificador numérico de doador aparece pareado dentro da série GSE13168; a relação desses doadores com a coorte AIRWAY fica `unknown`.

Fonte primária: [GEO GSE13168](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE13168); [Himes et al. (2014)](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0099625). A alternativa útil exige recuperar uma tabela por amostra que resolva estímulo e tratamento ou escolher outra coorte com metadados completos, antes de mudar o contraste.
