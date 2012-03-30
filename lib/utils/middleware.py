# -*- coding:utf-8 -*-

class NoCache(object):
    """
        Middleware responsável por dizer ao browser para não salvar as páginas no cache.
        Ela adiciona atributos ao cabeçalho de resposta da requisição.
    """ 
           
    def process_response(self, request, response):
        
        response['Pragma'] = 'no-cache'
        response['Cache-Control'] = "no-store, no-cache, must-revalidate, post-check=0, pre-check=0"
                 
        return response