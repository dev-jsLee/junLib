import importlib

def auto_import(module_name: str, pip_name: str, lib_name: str=None, ask:bool=True):
    """
    주어진 모듈 이름을 사용하여 해당 Python 라이브러리를 자동으로 임포트하고, 필요한 경우 pip을 통해 설치하는 함수입니다.

    이 함수는 먼저 `module_name`을 사용하여 라이브러리가 현재 환경에 이미 설치되어 있는지 확인합니다. 
    만약 라이브러리가 설치되어 있지 않은 경우, `pip_name`을 사용하여 해당 라이브러리를 설치합니다.

    매개변수:
    - module_name (str): 임포트하려는 모듈의 이름입니다.
    - pip_name (str): pip을 사용하여 설치할 때 사용될 패키지의 이름입니다.
    - lib_name (str):   사용자에게 표시될 라이브러리의 이름입니다. 
                        이 이름은 주로 로깅이나 오류 메시지에 사용됩니다.

    예외:
    - ImportError: 지정된 모듈을 임포트할 수 없을 때 발생합니다.
    - Exception: pip를 통한 설치 과정에서 오류가 발생할 경우 처리됩니다.

    출력:
    - 라이브러리가 성공적으로 설치되면 완료 메시지를 출력합니다.
    - 설치 중 오류가 발생하면 오류 메시지를 출력합니다.
    """
    lib_name = lib_name or f"{module_name}({pip_name})"
    try:
        importlib.import_module(module_name)
    except ImportError:
        print(f"{lib_name} 라이브러리가 설치되지 않았습니다.")
        if ask: input("자동 설치를 시도합니까? 시작하려면 엔터를 입력해주십시오.")
        try:
            import subprocess
            subprocess.check_call(["pip", "install", pip_name])
            print(f"{lib_name} 라이브러리 설치 완료!")
        except Exception as e:
            print(f"{lib_name} 라이브러리 설치 중 오류 발생: {str(e)}")
