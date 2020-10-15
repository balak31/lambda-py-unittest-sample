# Python unit testing and amazon web services

So you've wrote an awesome python automation tool that utilizes **boto**,
what's next?

## Libraries

We will utilize the following Python libraries, each of them has fantastic
documentation:

 * [setuptools](https://setuptools.readthedocs.io)
 * [unittest](https://docs.python.org/2/library/unittest.html)
 * [coverage](https://coverage.readthedocs.io/en/coverage-4.2)
 * [boto3](https://boto3.readthedocs.io/en/latest)
 * [moto](https://github.com/spulec/moto)


## Setup Script

Each python project should include a [setup.py](https://docs.python.org/2/distutils/setupscript.html), this file outlines the project's package dependencies, version and entry_points.

**setup** provides us with two dependency declarations:

 * install_requires
 * tests_require

 **install_requires** specifies libraries required to install and unitize the
 project, for example this project is unable to run without **boto3**:

 ```
install_requires=[
 'boto3'
]
 ```

 **tests_require** specifies libraries required to test your project,
 for example this project requires **moto** to test:

 ```
tests_require=[
  'moto'
]
 ```

The **version** is declared as a string, I suggest using a [semver](http://semver.org/) versioning pattern of **major**, **minor**, **patch**:

```
version='0.0.1'
```

**entry_points** allows us to declare **console_scripts**, these allow us to write slick command line tools. This project provides two console_scripts:

```
entry_points={
    'console_scripts': [
        's3 = sample_project.s3:main',
        'route53 = sample_project.route53:main'
    ]
}
```

## Modules

In this sample project I used **boto3** to interface with two popular
amazon web service offerings:

 * Simple Storage Service (s3)
 * Domain Name System (route53)

Each of these offerings has a python module in my projects **sample_project** directory:

  * [s3.py](sample_project/s3.py)
  * [rout53.py](sample_project/route53.py)

Each module includes a **main** function that is declared as an **entry_point** within **setup.py**:

The **s3** command will print out each bucket, and it's content:

```
$ s3
[ static ]
 => style.css
 => style.js
```

The **route** command prints out each domain, and it's records:

```
$ route53
[ example.com. ]
 => www.example.com.
 => blog.example.com.
```

## Test Cases

In the **setup.py** I've declared my **test_suite** referencing the tests directory:

```
test_suite='tests'
```

For each of my project modules, I define a test module with the suffix **_test**:

* [s3_test.py](tests/s3_test.py)
* [rout53_test.py](tests/route53_test.py)

These modules contain a test case for each function found in the code
they test, and are prefixed with **test_**.

For example, [s3.py](sample_project/s3.py) defines a function named **list_s3_buckets**, where [s3_test.py](tests/s3_test.py) defines a method named **test_list_s3_buckets**.

When writing your **unittest** you will be using the  [assertion](https://docs.python.org/2/library/unittest.html#assert-methods) methods, that is to say you will call the module function, then verify the returned results are what you expected.

*Keep in mind the smaller and more concise a module function, the easier
it is to write a test case.*


## Mocking Amazon Web Services

Rather than running your **unittest** against amazon web services directly,
we will mock these requests. This allows us to run our test without network connectivity, or credentials to the underling amazon web services.

[Moto](https://github.com/spulec/moto) is a fantastic library which [mocks](https://en.wikipedia.org/wiki/Mock_object) our **boto3** service calls.

In [s3_test.py](tests/s3_test.py) I wrote a method that performs the following
actions:

 * mock s3 bucket creation
 * mock s3 file upload

```
@mock_s3
def __moto_setup(self):
    """
    Simulate s3 file upload
    """

    s3 = get_client()
    s3.create_bucket(Bucket=self.bucket)
    s3.put_object(Bucket=self.bucket, Key=self.key, Body=self.value)
```

Then in the **test_list_s3_buckets** method, I call **list_s3_buckets** function and **assert** the expected bucket is in the return:

```
@mock_s3
def test_list_s3_buckets(self):
    """
    check that our bucket shows as expected
    """

    # setup s3 environment
    self.__moto_setup()

    buckets = [b for b in list_s3_buckets()]
    self.assertTrue(self.bucket in buckets)
```

## Test Coverage

The python [coverage](https://coverage.readthedocs.io/en/coverage-4.2) package
is a tool for measuring the code coverage of your program.

*Without changing anything in your existing tests, coverage will provide
an insightful report on how well your unittest cover your application*

Rather than running the traditional *python setup.py test*, we will run
with **coverage**:

```
$ coverage run setup.py test
running test
running egg_info
writing requirements to sample_project.egg-info/requires.txt
writing sample_project.egg-info/PKG-INFO
writing top-level names to sample_project.egg-info/top_level.txt
writing dependency_links to sample_project.egg-info/dependency_links.txt
writing entry points to sample_project.egg-info/entry_points.txt
reading manifest file 'sample_project.egg-info/SOURCES.txt'
writing manifest file 'sample_project.egg-info/SOURCES.txt'
running build_ext
test_get_client (tests.route53_test.Route53TestCase) ... ok
test_list_route53_record_sets (tests.route53_test.Route53TestCase) ... ok
test_list_route53_zones (tests.route53_test.Route53TestCase) ... ok
test_main (tests.route53_test.Route53TestCase) ... ok
test_get_client (tests.s3_test.S3TestCase) ... ok
test_list_s3_buckets (tests.s3_test.S3TestCase) ... ok
test_list_s3_objects (tests.s3_test.S3TestCase) ... ok
test_main (tests.s3_test.S3TestCase) ... ok
test_read_s3_object (tests.s3_test.S3TestCase) ... ok

----------------------------------------------------------------------
Ran 9 tests in 0.562s

OK
```

You can then view the test results using the **report** option:

```
$ coverage report -m -i --omit=venv/*
Name                         Stmts   Miss  Cover   Missing
----------------------------------------------------------
sample_project/__init__.py       0      0   100%
sample_project/route53.py       21      0   100%
sample_project/s3.py            25      0   100%
setup.py                         4      0   100%
tests/__init__.py                0      0   100%
tests/route53_test.py           37      0   100%
tests/s3_test.py                38      0   100%
----------------------------------------------------------
TOTAL                          125      0   100%
```

Or you can view the results in a detailed collection of **html** files:

```
$ coverage html --omit=venv/*
```

**index.html** gives you an entry point to each of your modules coverage.

```
$ ls -1 htmlcov/
coverage_html.js
index.html
jquery.debounce.min.js
jquery.hotkeys.js
jquery.isonscreen.js
jquery.min.js
jquery.tablesorter.min.js
keybd_closed.png
keybd_open.png
sample_project___init___py.html
sample_project_route53_py.html
sample_project_s3_py.html
setup_py.html
status.json
style.css
tests___init___py.html
tests_route53_test_py.html
tests_s3_test_py.html
```
