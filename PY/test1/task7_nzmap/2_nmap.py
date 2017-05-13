# from libnmap.process import NmapProcess
#
# nm = NmapProcess("127.0.0.1", options="-sV")
# rc = nm.run()
# print(rc,nm.rc)
# if nm.rc == 0:
#     print(nm.stdout)
# else:
#     print(nm.stderr)


from libnmap.process import NmapProcess
from time import sleep


# nmap_proc = NmapProcess(targets="scanme.nmap.org", options="-sT")
# nmap_proc.run_background()
# while nmap_proc.is_running():
#     print("Nmap Scan running: ETC: {0} DONE: {1}%".format(nmap_proc.etc,
#                                                           nmap_proc.progress))
#     sleep(2)
#
# print("rc: {0} output: {1}".format(nmap_proc.rc, nmap_proc.summary))

from libnmap.process import NmapProcess
from libnmap.parser import NmapParser, NmapParserException


# start a new nmap scan on localhost with some specific options
def do_scan(targets, options):
    parsed = None
    nmproc = NmapProcess(targets, options)
    rc = nmproc.run()
    if rc != 0:
        print("nmap scan failed: {0}".format(nmproc.stderr))
    print(type(nmproc.stdout))

    try:
        parsed = NmapParser.parse(nmproc.stdout)
        print(parsed.commandline,'------------')
    except NmapParserException as e:
        print("Exception raised while parsing scan: {0}".format(e.msg))

    return parsed


# print scan results from a nmap report
def print_scan(nmap_report):
    print("Starting Nmap {0} ( http://nmap.org ) at {1}".format(
        nmap_report.version,
        nmap_report.started))

    for host in nmap_report.hosts:
        if len(host.hostnames):
            tmp_host = host.hostnames.pop()
        else:
            tmp_host = host.address

        print("Nmap scan report for {0} ({1})".format(
            tmp_host,
            host.address))
        print("Host is {0}.".format(host.status))
        print("  PORT     STATE         SERVICE")

        for serv in host.services:
            pserv = "{0:>5s}/{1:3s}  {2:12s}  {3}".format(
                    str(serv.port),
                    serv.protocol,
                    serv.state,
                    serv.service)
            if len(serv.banner):
                pserv += " ({0})".format(serv.banner)
            print(pserv)
    print(nmap_report.summary)


if __name__ == "__main__":
    report = do_scan(['127.0.0.1','127.0.0.2'], "-sV -oN D:/test.data")
    if report:
        print_scan(report)
    else:
        print("No results returned")

# from libnmap.process import NmapProcess
# from libnmap.parser import NmapParser
#
# nm = NmapProcess("127.0.0.1, scanme.nmap.org")
# nm.run()
#
# nmap_report = NmapParser.parse(nm.stdout)
#
# for scanned_hosts in nmap_report.hosts:
#     print(scanned_hosts)