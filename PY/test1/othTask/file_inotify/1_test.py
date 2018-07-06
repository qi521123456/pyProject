def duiji(n):
    a = 1
    b = 1
    c = 2

    for i in range(n-3):
        d = a+c
        a = b
        b = c
        c = d
        print(c)
def monitor(path):
    import inotify.adapters
    i = inotify.adapters.Inotify()
    i.add_watch(path)
    try:
        for event in i.event_gen():
            if event is not None:
                (header, type_names, watch_path, filename) = event
                print("WD=(%d) MASK=(%d) COOKIE=(%d) LEN=(%d) MASK->NAMES=%s "
                             "WATCH-PATH=[%s] FILENAME=[%s]"%(
                             header.wd, header.mask, header.cookie, header.len, type_names,
                             watch_path.decode('utf-8'), filename.decode('utf-8')))
    finally:
        i.remove_watch(path)


if __name__ == '__main__':
    monitor('D:/')
    # duiji(20)