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
    "Total de registros": "SELECT COUNT(*) AS \"Total_de_registros\" FROM public.beneficiarios",
    "Soma total de valores pagos": "SELECT SUM(valor_parcela) AS \"Soma_total_de_valores_pagos\" FROM public.beneficiarios",
    "Total de beneficiados em Brasília": "SELECT COUNT(*) AS \"Total_de_beneficiados_em_Brasilia\" FROM public.beneficiarios WHERE nome_municipio = 'BRASILIA'",
    "Total de beneficiados em São Paulo": "SELECT COUNT(*) AS \"Total_de_beneficiados_em_Sao_Paulo\" FROM public.beneficiarios WHERE nome_municipio = 'SAO PAULO'",
    "Total de beneficiados em Salvador": "SELECT COUNT(*) AS \"Total_de_beneficiados_em_Salvador\" FROM public.beneficiarios WHERE nome_municipio = 'SALVADOR'",
    "Total de pagamentos em Brasília": "SELECT SUM(valor_parcela) AS \"Total_de_pagamentos_em_Brasilia\" FROM public.beneficiarios WHERE nome_municipio = 'BRASILIA'",
    "Total de pagamentos em São Paulo": "SELECT SUM(valor_parcela) AS \"Total_de_pagamentos_em_Sao_Paulo\" FROM public.beneficiarios WHERE nome_municipio = 'SAO PAULO'",
    "Total de pagamentos em Salvador": "SELECT SUM(valor_parcela) AS \"Total_de_pagamentos_em_Salvador\" FROM public.beneficiarios WHERE nome_municipio = 'SALVADOR'",
    "Soma total por município em ordem alfabética": "SELECT nome_municipio, SUM(valor_parcela) FROM public.beneficiarios GROUP BY nome_municipio ORDER BY nome_municipio ASC",
    "Soma total por município em ordem de maiores valores": "SELECT nome_municipio, SUM(valor_parcela) FROM public.beneficiarios GROUP BY nome_municipio ORDER BY SUM(valor_parcela) DESC",
    "CPF duplicados": "SELECT cpf_favorecido, COUNT(cpf_favorecido) FROM public.beneficiarios GROUP BY cpf_favorecido HAVING COUNT(cpf_favorecido) > 1"
}