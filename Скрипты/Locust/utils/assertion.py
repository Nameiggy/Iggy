from config.config import logger
def check_http_response(response,param_to_check) -> bool:
    result = None
    try:
        assert param_to_check in response.text
    except AssertionError as err:
        response.failure(f"Assertion arror: text pattern {param_to_check} was not found in response body! )")
        logger.warning(f"Assertion arror: text pattern {param_to_check} was not found in response body!")
        result = False
        pass
    else:
        result = True
    finally:
        return result