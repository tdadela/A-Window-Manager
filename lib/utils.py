import subprocess


def run_application(command):
    subprocess.Popen(command)


def run_bash_command(cmd):
    process = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE)
    output, _ = process.communicate()
    return output.decode("utf-8").strip()


def check_program_existence(prog):
    return bool(run_bash_command(f"which {prog}"))


def get_program_location(prog):
    result = run_bash_command(f"which {prog}")
    if not result:
        print(
            f"There is no {prog} on your computer. Please install it for wm to work properly.")
        return ""

    return result
