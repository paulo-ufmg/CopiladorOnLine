from subprocess import Popen, PIPE

class PythonShell:
    def execute(self, code):
        try:
            process = Popen(['python3', '-c', code], stdout=PIPE, stderr=PIPE)
            output, error = process.communicate()
            if process.returncode == 0:
                return output.decode(), None
            else:
                return None, error.decode()
        except Exception as e:
            return None, str(e)
