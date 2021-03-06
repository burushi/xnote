# encoding=utf-8
import sys
import os
import time
sys.path.insert(1, "lib")
import unittest
import xutils
import xconfig
from xutils import textutil

@xutils.cache(prefix='fib')
def fib(n):
    if n == 1 or n == 2:
        return 1
    return fib(n-1) + fib(n-2)

class TestMain(unittest.TestCase):
    def test_quote_unicode(self):
        result = xutils.quote_unicode("http://测试")
        self.assertEqual("http://%E6%B5%8B%E8%AF%95", result)
        result = xutils.quote_unicode("http://test/测试")
        self.assertEqual("http://test/%E6%B5%8B%E8%AF%95", result)
        r1 = xutils.quote_unicode("测试")
        r2 = xutils.quote_unicode(r1)
        self.assertEqual(r1, r2) # 重复encode是安全的

    def test_quote_unicode_2(self):
        result = xutils.quote_unicode("http://test?name=测试")
        self.assertEqual("http://test?name=%E6%B5%8B%E8%AF%95", result)
        result = xutils.quote_unicode("http://test?name=测试&age=10")
        self.assertEqual("http://test?name=%E6%B5%8B%E8%AF%95&age=10", result)

    def test_get_opt(self):
        # 不好用
        import getopt
        opts, args = getopt.getopt(["--data","/data", "--log", "/log/log.log"], "x", ["data=", "log="])
        print()
        print(opts)
        print(args)
        self.assertEqual(opts[0], ("--data", "/data"))

    def test_argparse(self):
        import argparse

        parser = argparse.ArgumentParser()
        parser.add_argument("-a", action="store", default=False)
        parser.add_argument("--data", default="./data")
        parser.add_argument("--test", default=True)
        result = parser.parse_args(["-a", "1", "--data", "/data"])
        print()
        print(result)
        self.assertEqual(True, hasattr(result, "data"))
        self.assertEqual(False, hasattr(result, "not_exists"))
        self.assertEqual("1", result.a)
        self.assertEqual("/data", result.data)
        self.assertEqual(True, result.test)

    def test_get_relative_path(self):
        path   = "./test/test.html"
        parent = "./"
        relative_path = xutils.get_relative_path(path, parent)
        self.assertEqual("test/test.html", relative_path)

        path   = "./test.html"
        parent = "./"
        relative_path = xutils.get_relative_path(path, parent)
        self.assertEqual("test.html", relative_path)

        path = "./test/test.html"
        parent = "./test"
        relative_path = xutils.get_relative_path(path, parent)
        self.assertEqual("test.html", relative_path)

    def test_splitpath(self):
        if not xutils.is_windows():
            path = "/root/test"
            pathlist = xutils.splitpath(path)
            self.assertEqual(2, len(pathlist))

    def test_decode_name(self):
        self.assertEqual("a.txt", xutils.decode_name("a.txt"))
        self.assertEqual("a.txt", xutils.decode_name("YS50eHQ=.x0"))
        self.assertEqual("a.txt", xutils.decode_name("YS50eHQ=.xenc"))

    def test_encode_name(self):
        self.assertEqual("YS50eHQ=.x0", xutils.encode_name("a.txt"))
        self.assertEqual("YS50eHQ=.x0", xutils.encode_name("YS50eHQ=.x0"))

    def test_edit_distance(self):
        self.assertEqual(1, xutils.edit_distance("abcd","abc"))
        self.assertEqual(2, xutils.edit_distance("abcd", "ab"))
        self.assertEqual(3, xutils.edit_distance("abc", "def"))
        self.assertEqual(3, xutils.edit_distance("kkabcd", "abc"))

    def test_bs4(self):
        html = "<p>hello<p><p>world</p>"
        if xutils.bs4 is not None:
            soup = xutils.bs4.BeautifulSoup(html, "html.parser")
            text = soup.get_text(separator=" ")
            self.assertEqual("hello world", text)


    def test_search_path(self):
        print(os.getcwd())
        result = xutils.search_path("./", "*test*")
        self.assertTrue(len(result) > 0)

    def test_cache(self):
        fib(35)
        self.assertTrue(xutils.expire_cache("fib(1,)"))

    def test_storage(self):
        obj = xutils.Storage(name="name")
        self.assertEqual(obj.name, "name")
        self.assertEqual(obj.value, None)

    def test_storage_default(self):
        obj = xutils.Storage(1, name="name")
        self.assertEqual(obj.value, 1)

    def test_save_file(self):
        tmpfile = os.path.join(xconfig.DATA_DIR, "tmp.txt")
        xutils.savetofile(tmpfile, "test")
        content = xutils.readfile(tmpfile)
        self.assertEqual("test", content)
        xutils.remove(tmpfile, True)

    def test_match_time(self):
        tm = time.strptime("2015-01-01", "%Y-%m-%d")
        self.assertFalse(xutils.match_time(year = 2016, tm = tm))
        self.assertTrue(xutils.match_time(month = 1, tm = tm))


    def test_history(self):
        h = xutils.History("test", 3)
        h.put(1)
        h.put(2)
        h.put(3)
        h.put(4)
        self.assertEqual(len(h), 3)

    def test_exec_code(self):
        code = "print(123)"
        xutils.exec_python_code(name='test', code = code, record_stdout = False, raise_err = True)

    def test_mark_text(self):
        text = "hello world"
        html = xutils.mark_text(text)
        self.assertEqual("hello&nbsp;world", html)

        text = "a link https://link"
        html = xutils.mark_text(text)
        self.assertEqual('a&nbsp;link&nbsp;<a href="https://link">https://link</a>', html)

    def test_count_alpha(self):
        text = "abc def 123"
        self.assertEqual(6, textutil.count_alpha(text))

    def test_count_digit(self):
        text = "abc def 123"
        self.assertEqual(3, textutil.count_digit(text))

    def test_textutil(self):
        import doctest
        doctest.testmod(m=textutil, verbose=True)

    def test_netutil(self):
        import doctest
        doctest.testmod(m=xutils.netutil, verbose=True)

    def test_dateutil(self):
        import doctest
        doctest.testmod(m=xutils.dateutil, verbose=True)

    def test_fsutil(self):
        import doctest
        doctest.testmod(m=xutils.fsutil, verbose=True)

    def test_print_table(self):
        xutils.print_table([dict(name="a", age=10), dict(name="b", age=12)])

    def test_http_get(self):
        out = xutils.http_get("http://baidu.com")

    def test_http_download(self):
        fname = "baidu_tmp.html"
        xutils.http_download("http://baidu.com", fname)
        os.remove(fname)

    def test_splithost(self):
        host, path = xutils.splithost("http://example.com/hello")
        self.assertEqual("example.com", host)
        self.assertEqual("/hello", path)


        
