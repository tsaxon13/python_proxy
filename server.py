import web
import socket
import thread

urls = (
    '/proxysetup', 'proxysetup'
)

app = web.application(urls, globals())


def forwardChildThread(source, destination):
    data = ' '
    while True:
        data = source.recv(1024)
        if data:
            destination.sendall(data)
        else:
            try:
                source.shutdown(socket.SHUT_RD)
                destination.shutdown(socket.SHUT_RW)
            except Exception:
                print("Sockets are probably already closed")
                break


def forwardParentThread(localsocket, remoteip, remoteport):
    lsocket = localsocket.accept()[0]
    remotesocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    remotesocket.connect((remoteip, int(remoteport)))
    thread.start_new_thread(forwardChildThread, (lsocket, remotesocket))
    thread.start_new_thread(forwardChildThread, (remotesocket, lsocket))


class proxysetup:

    def GET(self):
        try:
            data = web.input()
        except Exception as e:
            return "Bad request. Please send IP and Port\n\n\n" + str(e)
        else:
            if data:
                if data.ip and data.port:
                    # create local socket, remote socket and such
                    localsocket = socket.socket(
                        socket.AF_INET,
                        socket.SOCK_STREAM
                    )
                    localsocket.setsockopt(
                        socket.SOL_SOCKET,
                        socket.SO_REUSEADDR,
                        1
                    )
                    localsocket.bind(('', 0))
                    localsocket.listen(5)
                    localport = localsocket.getsockname()[1]
                    thread.start_new_thread(
                        forwardParentThread,
                        (localsocket, data.ip, data.port)
                    )
                    return (
                        "Connect to " +
                        web.ctx.host.split(":")[0] +
                        " on port " +
                        str(localport)
                    )
                else:
                    return "Bad request. Please send IP and Port"
            else:
                return "Bad request. Please send IP and Port"


if __name__ == "__main__":
    app.run()
