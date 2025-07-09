import sys
import subprocess


def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

required = [
    "click",
    "pyaudio"
]

def check():
    for pkg in required:
        try:
            __import__(pkg)
            print(f"{pkg} 已安装")
        except ImportError:
            print(f"正在安装 {pkg} ...")
            install(pkg)

if __name__ == "__main__":
    check()
