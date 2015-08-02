# Parse Shebang

Parse shebangs so script-like files can be executed directly on Windows

On Windows, scripts are supposed to be registered with with their
interpreters and placed into PATHEXT, but that information might not
be available and the script still needs to be run. In that case, this
module is useful, because it looks up the required information to run the
script as best as possible.

## Status

| Travis CI (Ubuntu) | AppVeyor (Windows) | Coverage | PyPI | Licence |
|--------------------|--------------------|----------|------|---------|
|[![Travis](https://img.shields.io/travis/polysquare/python-parse-shebang.svg)](http://travis-ci.org/polysquare/python-parse-shebang)|[![AppVeyor](https://img.shields.io/appveyor/ci/smspillaz/python-parse-shebang.svg)](https://ci.appveyor.com/project/smspillaz/python-parse-shebang)|[![Coveralls](https://img.shields.io/coveralls/polysquare/python-parse-shebang.svg)](http://coveralls.io/polysquare/python-parse-shebang)|[![PyPIVersion](https://img.shields.io/pypi/v/parse-shebang.svg)](https://pypi.python.org/pypi/parse-shebang)[![PyPIPythons](https://img.shields.io/pypi/pyversions/parse-shebang.svg)](https://pypi.python.org/pypi/parse-shebang)|[![License](https://img.shields.io/github/license/polysquare/python-parse-shebang.svg)](http://github.com/polysquare/python-parse-shebang)|

## API Usage

    shebang = parseshebang.parse(file_to_parse)
    subprocess.check_call(shebang + ["/my_script.py"])

`file_to_parse` may be either an open file object, which supports seeking,
or a file name. A list containing the shebang components is returned.