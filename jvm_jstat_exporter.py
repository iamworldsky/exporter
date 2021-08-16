from prometheus_client import start_http_server, Summary, Gauge, Counter
import commands,time,os,sys


c = Gauge('jvm_fullgc', 'Java fullgc times', ['application'])
d = Gauge('jvm_youngc', 'Java yonngc times', ['application'])
e = Gauge('jvm_fullgc_time', 'Java fullgc time', ['application'])
f = Gauge('jvm_youngc_time', 'Java yonngc time', ['application'])
g = Gauge('jvm_eden_ratio', 'Java Eden use ratio', ['application'])
h = Gauge('jvm_old_ratio', 'Java Old use ratio', ['application'])
j = Gauge('jvm_metadata_ratio', 'Java metadata use ratio', ['application'])


if __name__ == '__main__':
    # Start up the server to expose the metrics.
    start_http_server(18201)
    print("server is starting, listening on 18201!")

    application = {}
    for i in range(1, len(sys.argv)):
        app = sys.argv[i]
    	stataus, pid = commands.getstatusoutput("jps -v | grep %s | awk '{print $1}' " % sys.argv[i] )
    	application[app]=pid
    while True:
        time.sleep(2)
        for k,v in application.items():
		status, jstat = commands.getstatusoutput("jstat -gcutil %d | sed -n 2p | awk '{print $3,$4,$5,$7,$8,$9,$10}'" % int(v) )
        	if status == 0:
	            eden, old, metadata, youngc, youngctime, fullgc, fullgctime = jstat.split()
                    c.labels(application=k).set(fullgc)
                    d.labels(application=k).set(youngc)
                    e.labels(application=k).set(fullgctime)
                    f.labels(application=k).set(youngctime)
                    g.labels(application=k).set(eden)
                    h.labels(application=k).set(old)
                    j.labels(application=k).set(metadata)
