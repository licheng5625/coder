import http.client
import urllib.parse
import socket
from urlunshort.urlunshort import resolve
from urllib.parse import urlparse

def unshorten_url(url):
    #if is_shortened(url):
         try:
            parsed = urllib.parse.urlparse(url)
            h = http.client.HTTPConnection(parsed.netloc,timeout=2)
            resource = parsed.path
            if parsed.query != "":
                resource += "?" + parsed.query
            h.request('HEAD', resource )
            response = h.getresponse()
            print('check '+url)

            if int(response.status/100) == 3 and response.getheader('Location') is not None:
                newurl=response.getheader('Location')
                if newurl !=url:
                    return unshorten_url(newurl)         # changed to process chains of short urls
                else:
                    return urlparse(url).netloc
            else:
                return urlparse(url).netloc

         except Exception:
              return urlparse(url).netloc
         except ConnectionRefusedError:
             return urlparse(url).netloc
         except socket.gaierror:
             return urlparse(url).netloc
    # urlret=resolve(url)
    # if urlret ==None:
    #     return urlparse(url).netloc
    # else:
    #     ret=resolve(urlret)
    #     if ret == None:
    #         return urlparse(urlret).netloc
    #     else:
    #         return urlparse(ret).netloc

    # else:
    #     return url


#print(unshorten_url('https://youtu.be/xaDBkpZkipI'))