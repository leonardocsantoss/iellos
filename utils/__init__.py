# -*- coding: utf-8 -*-

def clean_cpf_cnpj(cpf_cnpj):
    if not '-' in cpf_cnpj:
        if cpf_cnpj[:3] == '000':
            cpf_cnpj = cpf_cnpj[3:]
        if len(cpf_cnpj) == 11:
            cpf_cnpj = u'%s.%s.%s-%s' % (cpf_cnpj[0:3], cpf_cnpj[3:6], cpf_cnpj[6:9], cpf_cnpj[9:11])
        else:
            cpf_cnpj = u'%s.%s.%s/%s-%s' % (cpf_cnpj[0:2], cpf_cnpj[2:5], cpf_cnpj[5:8], cpf_cnpj[8:12], cpf_cnpj[12:14])
    return cpf_cnpj