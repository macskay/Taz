import coverage
from unittest import TextTestRunner, TestLoader
from os.path import split, join, abspath
from os import chdir

if __name__ == "__main__":
    project_dir = split(split(abspath(__file__))[0])[0]
    chdir(project_dir)
    cov = coverage.coverage(branch=True)
    cov.start()
    suite = TestLoader().discover(".", pattern="test_*.py")
    TextTestRunner(verbosity=2).run(suite)
    cov.stop()
    cov.save()
    cov.html_report()


