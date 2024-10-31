URL = "https://portaldatransparencia.gov.br/download-de-dados/novo-bolsa-familia/"

months_dict = {
    1: "Janeiro",
    2: "Fevereiro",
    3: "Março",
    4: "Abril",
    5: "Maio",
    6: "Junho",
    7: "Julho",
    8: "Agosto",
    9: "Setembro",
    10: "Outubro",
    11: "Novembro",
    12: "Dezembro"
}
""" Identificar se existem CPF repetidos no banco de dados (lista se houver)
 """
selects_dict = {
    "total_de_registros": "SELECT COUNT(*) FROM public.beneficiarios",
    "soma_total_de_valores_pagos": "SELECT SUM(valor_parcela) FROM public.beneficiarios",
    "total_de_beneficiados_brasilia": "SELECT COUNT(*) FROM public.beneficiarios WHERE nome_municipio = 'BRASILIA'",
    "total_de_beneficiados_sao_paulo": "SELECT COUNT(*) FROM public.beneficiarios WHERE nome_municipio = 'SAO PAULO'",
    "total_de_beneficiados_salvador": "SELECT COUNT(*) FROM public.beneficiarios WHERE nome_municipio = 'SALVADOR'",
    "total_de_pagamentos_brasilia": "SELECT SUM(valor_parcela) FROM public.beneficiarios WHERE nome_municipio = 'BRASILIA'",
    "total_de_pagamentos_sao_paulo": "SELECT SUM(valor_parcela) FROM public.beneficiarios WHERE nome_municipio = 'SAO PAULO'",
    "total_de_pagamentos_salvador": "SELECT SUM(valor_parcela) FROM public.beneficiarios WHERE nome_municipio = 'SALVADOR'",
    "soma_total_por_municipio_ordem_alfabetica": "SELECT nome_municipio, SUM(valor_parcela) FROM public.beneficiarios GROUP BY nome_municipio ORDER BY nome_municipio ASC",
    "soma_total_por_municipio_ordem_maiores_valores": "SELECT nome_municipio, SUM(valor_parcela) FROM public.beneficiarios GROUP BY nome_municipio ORDER BY SUM(valor_parcela) DESC",
}