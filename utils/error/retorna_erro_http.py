from fastapi import HTTPException

def retorna_erro_http(msg: str, cod_status: int):
    """
    Função utilitária para gerar uma exceção HTTPException.

    :param msg: Mensagem de erro a ser retornada.
    :param cod_status: Código de status HTTP.
    """
    raise HTTPException(
        status_code=cod_status,
        detail=msg
    )