from distutils.core import setup

setup(name="qnetwork",
      version="2.1.1",
      author="Alexey Naumov",
      author_email="rocketbuzzz@gmail.com",
      description="",
      packages=[
          "qnetwork",
          "debuggers",
          "debuggers/tcp",
          "debuggers/tcp/client",
          "debuggers/tcp/server",
          "debuggers/udp"],
      package_data={
          'debuggers/tcp/client': [
              'icons/*',
          ],
          'debuggers/tcp/server': [
              'icons/*',
          ],
      },
      scripts=[
          "debuggers/tcp/tcp-client-debugger",
          "debuggers/tcp/tcp-server-debugger"]
     )
