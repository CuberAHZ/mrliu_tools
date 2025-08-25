try:
    import socket, pyaudio, queue, threading
except:
    import tools.pkg_installer as pkg_installer
    pkg_installer.required = ["pyaudio"]
    pkg_installer.check()


__version__ = "1.1.0"


def audio_send(receiver_ip, port, rate, channels, chunk, FORMAT = pyaudio.paInt16):
    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT, channels=channels, rate=rate, input=True, frames_per_buffer=chunk*2)

    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    try:
        print("开始发送音频数据...")
        while True:
            data = stream.read(chunk)  # 从麦克风读取数据
            udp_socket.sendto(data, (receiver_ip, port))  # 发送音频数据到接收端
    except KeyboardInterrupt:
        print("停止发送音频数据...")
    finally:
        stream.stop_stream()
        stream.close()
        p.terminate()
        udp_socket.close()


def audio_recv(port, rate, channels, chunk, MAXSIZE=25, FORMAT=pyaudio.paInt16):
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT, channels=channels, rate=rate, output=True, frames_per_buffer=chunk*2)

    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_socket.bind(("0.0.0.0", port))

    audio_q = queue.Queue(maxsize=MAXSIZE)

    def udp_receiver():
        while True:
            data, _ = udp_socket.recvfrom(16384)
            try:
                audio_q.put(data, timeout=0.1)
            except queue.Full:
                pass  # 丢弃过多的数据，防止阻塞

    threading.Thread(target=udp_receiver, daemon=True).start()

    try:
        print("开始接收音频数据...")
        while True:
            try:
                data = audio_q.get(timeout=0.2)
            except queue.Empty:
                data = b'\x00' * (chunk * channels * 2)
            stream.write(data)
    except KeyboardInterrupt:
        print("停止接收音频数据...")
    finally:
        stream.stop_stream()
        stream.close()
        p.terminate()
        udp_socket.close()
