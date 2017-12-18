import lxml.html as html
from urllib.request import urlopen
from urllib.error import URLError


def parse(url):
    try:
        resp = urlopen(url)
        page = html.parse(resp)
        tags = ("h1", "h2", "h3", "h4", "h5", "h6", "p", "span")
        string = ""
        for tag in tags:
            try:
                string = page.xpath("//%s/text()" % tag)[0]
                string = string.replace(
                    "\n", "").replace("\r", "").replace("\t", "").strip()
                if string:
                    break
            except IndexError:
                continue
        return insert_TM_sign(string)
    except URLError:
        return


def insert_TM_sign(string):
    tm_sign = "&trade;"
    str_list = string.replace(".", " .").replace(",", " ,").split()
    temp_list = []
    for string in str_list:
        if len(string) == 6:
            temp_list.append(string + tm_sign)
        else:
            temp_list.append(string)
    string = " ".join(temp_list).replace(" .", ".").replace(" ,", ",")
    return string
