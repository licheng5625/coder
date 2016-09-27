
import urllib
import urllib2
import ssl

print ssl.OPENSSL_VERSION

ctx = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)

data = urllib.urlencode({ 'task': 'mac-status', 'mac': '78-DD-08-E5-78-7F' })

url= urllib2.urlopen('https://www.mac-status.de/index.php',context=ctx).read()
