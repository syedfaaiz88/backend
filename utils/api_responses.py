from rest_framework.response import Response

def custom_response(status=True, message='', error_code='', errors=None , result=None, has_result=True, status_code=200):
    return Response({
        'status': status,
        'message': message,
        'errorCode': error_code,
        'errors': errors,
        'result': result,
        'hasResult': has_result
    }, status=status_code)


