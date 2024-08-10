import getpass
import asyncio


class Application:

    def __init__(self, raw):
        rec = raw.split(' ')
        rec = [data for data in rec if data != '']
        if rec == []:
            self.__del__()
        ip, port = rec[8].rsplit(':', 1)

        self.name: str = rec[0],
        self.pid: int = int(rec[1])
        self.user: str = rec[2]
        self.type: str = rec[4]
        self.node: str = rec[7]
        self.ip_addr: str = ip
        self.port: int = port

    def __hash__(self) -> int:
        hash = self.pid
        if self.type == 'IPv4':
            hash *= 16
        else:
            hash *= 32

        if self.node == 'TCP':
            hash *= 17
        else:
            hash *= 23
        return hash

    def __repr__(self) -> str:
        return self.__str__()

    def __str__(self) -> str:
        return f"""
        Application(
            {self.name=}
            {self.pid=}
            {self.user=}
            {self.type=}
            {self.node=}
            {self.ip_addr=}
            {self.port=}
        )"""


class Applications:

    def __init__(self, applications) -> None:
        self.applications = applications

    def append(self, value) -> None:
        self.applications.append(value)

    def __repr__(self) -> str:
        return self.__str__()

    def __str__(self) -> str:
        return f"""
        Applications(
            {self.applications=}
        )
        """


CMD = 'sudo lsof -i -P -n | grep LISTEN'


async def _lsof_get():

    def fake_ex_handler(loop, context):
        exception = context['exception']  # noqa
        message = context['message']  # noqa
    # log exception
    # get the event loop
    loop = asyncio.get_running_loop()
    loop.set_exception_handler(fake_ex_handler)
    proc = await asyncio.create_subprocess_shell(
        CMD,
        stdin=asyncio.subprocess.PIPE,
        stdout=asyncio.subprocess.PIPE,

    )

    PWD = getpass.getpass('Password: ').encode('utf-8')
    proc.stdin.write(PWD)
    proc.stdin.write_eof()
    await proc.stdin.drain()
    try:
        stdout = await proc.stdout.read()
    except Exception:
        print(stdout)

    proc._transport.close()
    apps = []
    await proc.wait()

    for record in stdout.decode('utf-8').split('\n'):
        if record != '':
            apps.append(
                Application(record)
            )

if __name__ == '__main__':
    future = asyncio.run(_lsof_get())
