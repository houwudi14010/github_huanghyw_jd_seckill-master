

import urllib
a="https://epaper.scdaily.cn/shtml/scrb/20210419/253239.shtml"
b='<a target="_blank" href="/scrb/20210419/3da789c7367faa81097a30bc57adc0c1.jpg"><img class="auto-width" src="/scrb/20210419/m_3da789c7367faa81097a30bc57adc0c1.jpg" border="0"></a>'
c = urllib.parse.urljoin(a,b)
print(c)
