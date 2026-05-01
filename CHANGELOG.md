# CHANGELOG


## v0.21.0 (2026-05-01)

### Bug Fixes

- Support more_itertools>=11
  ([`1716acd`](https://github.com/kalekundert/parametrize_from_file/commit/1716acdab55689a63b98de45d9edf05c3b4dc887))

### Chores

- Update target python version for ruff
  ([`0bf67d6`](https://github.com/kalekundert/parametrize_from_file/commit/0bf67d67a0d9d9408c1b9b3836b8bffd489e04c2))

- Upgrade python-semantic-release
  ([`51941de`](https://github.com/kalekundert/parametrize_from_file/commit/51941deb561cb66cc3714b88178d786e035a6de8))

### Features

- Allow anything with __name__ when making namespaces
  ([`2536cb9`](https://github.com/kalekundert/parametrize_from_file/commit/2536cb966e99684b140d97fd79c8a53a4289e2a9))

- Allow preprocess functions to be generators
  ([`a334a3b`](https://github.com/kalekundert/parametrize_from_file/commit/a334a3bcf55297e887ceb6a3bcc4a111d4475ded))

- Open YAML/JSON files as binary streams
  ([`a39093c`](https://github.com/kalekundert/parametrize_from_file/commit/a39093c3f00afad6b62bb92fbfb11bffd73dd3d6))

This ensures that the way the files are parsed is independent of the user's locale. This also fixes
  #27, although for what it's worth, I was never able to reproduce that specific error.

### Testing

- Check that scoped fixtures work
  ([`5525cbf`](https://github.com/kalekundert/parametrize_from_file/commit/5525cbf670a35712c1a2d1e70e7a37823df4421b))


## v0.20.0 (2024-04-21)

### Chores

- Allow more_itertools>=8.10
  ([`1b8366c`](https://github.com/kalekundert/parametrize_from_file/commit/1b8366c5b6a8d2a93424df7bc8903ab663a8d893))

- Fix the release process
  ([`c044bdd`](https://github.com/kalekundert/parametrize_from_file/commit/c044bddd4b7ce8e535731667d6fc1afdde235d80))

- Fix typo in test error message
  ([`fe495bd`](https://github.com/kalekundert/parametrize_from_file/commit/fe495bd11b504fbd398e52357455ddf12beccd45))

- Remove unnecessary shebang lines
  ([`adccaf6`](https://github.com/kalekundert/parametrize_from_file/commit/adccaf69bc0fe567058d88bfb257d9074930597f))

### Features

- Add a schema function to rename parameters
  ([`de5a71e`](https://github.com/kalekundert/parametrize_from_file/commit/de5a71ea3850de53351315d696c7146ef212ba34))

- Save decorator arguments as function attributes
  ([`367dff2`](https://github.com/kalekundert/parametrize_from_file/commit/367dff2f54da6eb86e7d8492a289bb209094ca88))

### Testing

- Improve test coverage
  ([`b3e6791`](https://github.com/kalekundert/parametrize_from_file/commit/b3e6791ea0427e88df736fe3155e4f43feb0e3de))

- Test `add_loader()` and `remove_loader()`
  ([`681edbc`](https://github.com/kalekundert/parametrize_from_file/commit/681edbcbf63b3b4af4f053ff568498c59ab084f0))


## v0.19.0 (2023-12-12)

### Bug Fixes

- Handle class-level parametrization correctly
  ([`24f8f13`](https://github.com/kalekundert/parametrize_from_file/commit/24f8f13f0eba388006a5ce51bda5129703c2a993))

Fixes #21

### Chores

- Add linting; update semantic release
  ([`bbd5a87`](https://github.com/kalekundert/parametrize_from_file/commit/bbd5a87bae4d8d07606cf9862f2ff9f8b8d3a0b4))

- Fix PyPI link to documentation
  ([`4448eb7`](https://github.com/kalekundert/parametrize_from_file/commit/4448eb7a058a0779a39185dec4f398ade28c4220))

- Ignore deprecation warnings caused by datetime/arrow
  ([`77b4216`](https://github.com/kalekundert/parametrize_from_file/commit/77b4216e89dd8a3e19b60ed9f856940d90bc46e1))

- Switch to gitlint
  ([`f5ea748`](https://github.com/kalekundert/parametrize_from_file/commit/f5ea7484e31f940fe6b957fd9d9cdd50a590fba5))

- Update ruff command
  ([`1aac862`](https://github.com/kalekundert/parametrize_from_file/commit/1aac862da1275da6410e153f0c12229256214b77))

- Upgrade to latest readthedocs config format
  ([`74ba8ac`](https://github.com/kalekundert/parametrize_from_file/commit/74ba8acec6f3aa23dff116b79693f25d8ae4aacd))

### Features

- Improve error message
  ([`e910232`](https://github.com/kalekundert/parametrize_from_file/commit/e9102326e2e51d81615b6b7577f9252e54d01855))


## v0.18.0 (2023-09-01)

### Documentation

- Fix syntax highlighting
  ([`fbc1e14`](https://github.com/kalekundert/parametrize_from_file/commit/fbc1e14d68bcfb0e2ccd0526d7d6d47f9d31df33))

- Fix typos
  ([`7681380`](https://github.com/kalekundert/parametrize_from_file/commit/76813801e7b3544d827023b924bcaf916286069c))

- Update examples to use 'import parametrize_from_file as pff'
  ([`794806b`](https://github.com/kalekundert/parametrize_from_file/commit/794806b5fda08e47cd30c989b0799eda9cb8c1c1))

### Features

- Allow schema functions to add marks
  ([`f1f0c2b`](https://github.com/kalekundert/parametrize_from_file/commit/f1f0c2b18e6dd7140f8d393bf23cd62a7203021c))


## v0.17.1 (2023-06-22)

### Bug Fixes

- Improve error messages
  ([`3a92dbf`](https://github.com/kalekundert/parametrize_from_file/commit/3a92dbf7fca3fbecac3b425ab3574df3d9983356))

### Chores

- Replace contextlib2 with contextlib
  ([#18](https://github.com/kalekundert/parametrize_from_file/pull/18),
  [`9c68f20`](https://github.com/kalekundert/parametrize_from_file/commit/9c68f20c8e75cc00b92d5ae73e2a30c7867bbd7a))

contextlib.nullcontext was added in Python 3.7 which is the oldest supported version

### Documentation

- Fix documentation link
  ([`da99cc5`](https://github.com/kalekundert/parametrize_from_file/commit/da99cc545f55b5e0201baa9771c4f5368015250f))

- Make README example more intuitive
  ([`277ba97`](https://github.com/kalekundert/parametrize_from_file/commit/277ba9735dee3ce862edd65da709562e38badf08))

### Testing

- Account for changed module name of `nt.load()`
  ([`1fb2b7b`](https://github.com/kalekundert/parametrize_from_file/commit/1fb2b7bf42fddaf1f6578235ba179bcdc7635da6))


## v0.17.0 (2022-08-23)

### Documentation

- Fix CI badge
  ([`a47c0c1`](https://github.com/kalekundert/parametrize_from_file/commit/a47c0c11d63a80aacb235302961d8374f75ae516))

### Features

- Allow multiple cast functions for each field
  ([`c026e8b`](https://github.com/kalekundert/parametrize_from_file/commit/c026e8b9989a9c67c6c45f70a3427207e43d83c0))


## v0.16.0 (2022-06-14)

### Features

- Don't eval/exec the error() context managers
  ([`9d8b2af`](https://github.com/kalekundert/parametrize_from_file/commit/9d8b2af5834b88e42230a75a88582f1c35a934a5))


## v0.15.0 (2022-06-10)

### Features

- Provide schema functions tailored for testing
  ([`275c79d`](https://github.com/kalekundert/parametrize_from_file/commit/275c79d3cfea5951aff624b0a8300fc65d875936))

- Add the `cast` and `defaults` schema functions.

- Refactor `error` and `error_or` into standalone functions that don't depend on the `Namespace`
  class. The corresponding `Namespace` methods remain, but are now just thin wrappers.

- Interpret iterable schema arguments as pipelines.

- Get rid of the voluptuous dependency.

Fixes #16


## v0.14.0 (2022-04-18)

### Documentation

- Use sentence-case for page titles
  ([`0f30c42`](https://github.com/kalekundert/parametrize_from_file/commit/0f30c421da9b6915864070c3b2cf6970e88cadf4))

### Features

- Allow loaders to be overridden locally
  ([`466fa31`](https://github.com/kalekundert/parametrize_from_file/commit/466fa31075427da63cb2f16529dbebde6c285d18))

- Allow preprocess() to get additional contextual information
  ([`a482725`](https://github.com/kalekundert/parametrize_from_file/commit/a4827256b1157a464c7c543a528cc3a826e5494a))


## v0.13.1 (2022-04-08)

### Bug Fixes

- Improve error messages
  ([`c1eaa78`](https://github.com/kalekundert/parametrize_from_file/commit/c1eaa78d7307ef09f97c069f621ff81ed428f847))

### Chores

- Drop support for python 3.6
  ([`dca2288`](https://github.com/kalekundert/parametrize_from_file/commit/dca2288856207cbc053d39b4648eaf57ce9c3cc5))

- Upgrade `pyproject.toml` as per PEP 621
  ([`9783b75`](https://github.com/kalekundert/parametrize_from_file/commit/9783b75a4269971f45febd9e7cfb054f7a7b6cd6))

### Documentation

- Add a tutorial on temporary files
  ([`09aa784`](https://github.com/kalekundert/parametrize_from_file/commit/09aa78405334f5ea7b44be121462ac0e50f37d26))

- Fix pytest cross-references
  ([`33580bb`](https://github.com/kalekundert/parametrize_from_file/commit/33580bbb8982073f90007f4cd0f47528c7df6ea0))

- Tweak wording
  ([`f791460`](https://github.com/kalekundert/parametrize_from_file/commit/f7914601cba64e256efdc5b1c73f5bbd53933fff))

- Use python 3.7 to build the docs
  ([`6bd272c`](https://github.com/kalekundert/parametrize_from_file/commit/6bd272cf5afd2eafa014581b730db369afc65983))

### Testing

- Add pytest_tmp_files dependency
  ([`bc71d5e`](https://github.com/kalekundert/parametrize_from_file/commit/bc71d5ee20e70265c003d74329a8c8b5285bca64))


## v0.13.0 (2022-01-17)

### Features

- Allow assertions on the direct causes of exceptions
  ([`d4d2be9`](https://github.com/kalekundert/parametrize_from_file/commit/d4d2be928b25048e3a4fac4edb6b5a54c0958be5))


## v0.12.0 (2022-01-17)

### Chores

- Treat all warnings as errors in CI
  ([`97f215c`](https://github.com/kalekundert/parametrize_from_file/commit/97f215c7ca1341b282d4b5d180f2639420eacbef))

### Features

- Allow deferred eval/exec to be invoked by name
  ([`08d0bf2`](https://github.com/kalekundert/parametrize_from_file/commit/08d0bf2869989f76a188de98c56891178c80c3cf))

I think this makes the code easier to read.


## v0.11.1 (2022-01-13)

### Bug Fixes

- Migrate to more_itertools.zip_broadcast()
  ([`cdf37c3`](https://github.com/kalekundert/parametrize_from_file/commit/cdf37c377fc7c65b6852c35e277b82cec7c0b864))

This avoids a warning in python>=3.10

Fixes #13


## v0.11.0 (2022-01-12)

### Documentation

- Fix python snippet examples
  ([`5497205`](https://github.com/kalekundert/parametrize_from_file/commit/5497205cd718d4898659f4924fd81a139b1b2d4e))

- Fix typos
  ([`38cea18`](https://github.com/kalekundert/parametrize_from_file/commit/38cea1863d62ec1202dfc94ed730e099c38e7bb8))

### Features

- Add empty_ok() for voluptuous schema
  ([`6fd446d`](https://github.com/kalekundert/parametrize_from_file/commit/6fd446dd8017f38cfff02beec6c0e1d7a90e2379))


## v0.10.0 (2022-01-04)

### Features

- Get multiple variables from executed snippets
  ([`c43c57a`](https://github.com/kalekundert/parametrize_from_file/commit/c43c57af9045586f5ab81f9cd3c86bb523d6c60b))


## v0.9.1 (2021-12-23)

### Bug Fixes

- Improve debug message
  ([`08fa038`](https://github.com/kalekundert/parametrize_from_file/commit/08fa0382d20bbc73312f11232105fa5a1f325357))


## v0.9.0 (2021-12-23)

### Features

- Try to import the voluptuous submodule
  ([`4d5cca4`](https://github.com/kalekundert/parametrize_from_file/commit/4d5cca4581b82526acd1174d66256281b48d9185))


## v0.8.0 (2021-12-23)

### Features

- Allow exec() and eval() to be deferred
  ([`b8cf9d5`](https://github.com/kalekundert/parametrize_from_file/commit/b8cf9d5a10fa9389fb4f90980cce5cc48b30a5b0))

This commit also gets rid of exec_and_lookup(), which was basically just doing one specific kind of
  deferral. Fixes #8.

- Make namespaces immutable, add more error checks
  ([`8e52066`](https://github.com/kalekundert/parametrize_from_file/commit/8e52066babd80bee0ca3ff2786ddb325ad16110e))

- Make namespaces immutable, fix #10. - Provide more flexible exception assertions, fix #9. - Add
  sensible `__bool__()` implementation for error context managers, fix #12.

### Testing

- Make sure namespaces with unpickleable values can be copied
  ([`1c61ee8`](https://github.com/kalekundert/parametrize_from_file/commit/1c61ee873e8abc90b052adf309f275b58950dabd))


## v0.7.1 (2021-10-07)

### Bug Fixes

- Include voluptuous dependency
  ([`62fc60b`](https://github.com/kalekundert/parametrize_from_file/commit/62fc60ba8e1dfe0ab93a8f96b9e3b8e2dca1292d))


## v0.7.0 (2021-10-06)

### Documentation

- Tweak wording
  ([`f3be56a`](https://github.com/kalekundert/parametrize_from_file/commit/f3be56ad706b999234c6a7758f16fca3dc0a47e4))

### Features

- Support eval/exec'ing mocks
  ([`121995a`](https://github.com/kalekundert/parametrize_from_file/commit/121995a6799334ed534a26aecfa5d23331f90d61))


## v0.6.0 (2021-10-06)

### Features

- Support indirect parametrization
  ([`34308c4`](https://github.com/kalekundert/parametrize_from_file/commit/34308c4cec6af0fe8fe74c20c07f49d7b0390e8c))

Fixes #7

- Support parametrized fixtures
  ([`e9a95c4`](https://github.com/kalekundert/parametrize_from_file/commit/e9a95c4c324f9af7579cb0c6352f1292c7e7b9d7))

Fixes #6

### Testing

- Add cases that break mi.zip_broadcast()
  ([`980dd3b`](https://github.com/kalekundert/parametrize_from_file/commit/980dd3bff94d2ac6756494f2b2f78c6bdeaeea75))

See https://github.com/more-itertools/more-itertools/issues/561


## v0.5.1 (2021-08-29)

### Bug Fixes

- Correctly format error messages with braces
  ([`7caaa31`](https://github.com/kalekundert/parametrize_from_file/commit/7caaa31da50930918efd0a4389bc45c860435027))

### Chores

- Apply cookiecutter
  ([`279a595`](https://github.com/kalekundert/parametrize_from_file/commit/279a595845b1adf87ae4fd24f5cec5295fdc748f))

- Merge cookiecutter
  ([`9eef273`](https://github.com/kalekundert/parametrize_from_file/commit/9eef273505d7202573fbbc7def8c5c647387c837))


## v0.5.0 (2021-08-22)

### Bug Fixes

- Check that the schema returns a dict
  ([`85ecdf1`](https://github.com/kalekundert/parametrize_from_file/commit/85ecdf1d810ce58f88a28eeddba370a87962ba91))

### Documentation

- Add examples of my projects that use this package
  ([`f1e59f3`](https://github.com/kalekundert/parametrize_from_file/commit/f1e59f3b0e7040687b9918461a67fc6297ca6bb4))

- Install dependencies
  ([`90721fd`](https://github.com/kalekundert/parametrize_from_file/commit/90721fd11f7dacc68bb70f125aa6348bf2f5e606))

### Features

- Add the *preprocess* argument
  ([`219aa9f`](https://github.com/kalekundert/parametrize_from_file/commit/219aa9f37429b876171b48c4c01ebefa9af4fb4f))

- Add the load_parameters() function
  ([`5c8af43`](https://github.com/kalekundert/parametrize_from_file/commit/5c8af43965beca80cdd87dfcf52ed9c89e9334c1))

I don't have a specific use for this API, but it seems like a good thing to have. It also forced me
  to refactor the code a bit to better separate responsibilities.

- Allow multiple paths/keys to be specified
  ([`fe6696a`](https://github.com/kalekundert/parametrize_from_file/commit/fe6696a30edb878d677304f13ff38adc5fc15478))


## v0.4.0 (2021-08-20)

### Documentation

- Install dependencies
  ([`6ca7ae8`](https://github.com/kalekundert/parametrize_from_file/commit/6ca7ae89b27af50172ae85e833e42ea7b5919a27))

### Features

- Add the Namespace eval/exec/error helper
  ([`e0c8523`](https://github.com/kalekundert/parametrize_from_file/commit/e0c85238997bd521c361463e6794e2e7ea299a0d))


## v0.3.0 (2020-12-07)

### Chores

- Remove stale imports
  ([`707ac13`](https://github.com/kalekundert/parametrize_from_file/commit/707ac13f282f02075ca9c153f650aa620b2d195f))

### Documentation

- Slightly clarify error messages
  ([`7393ee0`](https://github.com/kalekundert/parametrize_from_file/commit/7393ee072ecdb8c9cb960be0d7abc8e9ecdcd212))

### Features

- Accept any callable as the schema
  ([`2f3d1e1`](https://github.com/kalekundert/parametrize_from_file/commit/2f3d1e15129ebc70e7d5b3a2acbda3e5d7186a4a))

Fixes #1


## v0.2.0 (2020-12-04)

### Features

- Rename the 'key' argument
  ([`25d7879`](https://github.com/kalekundert/parametrize_from_file/commit/25d7879160c46a1b3d63eb3cad37e184e2c89144))


## v0.1.1 (2020-12-04)

### Bug Fixes

- Don't apply the schema to 'id' and 'marks'
  ([`e18e931`](https://github.com/kalekundert/parametrize_from_file/commit/e18e931749cf83370a88ebadf4a587e07566b41e))

### Chores

- Add dateutil as doc dependency
  ([`a016b2e`](https://github.com/kalekundert/parametrize_from_file/commit/a016b2e153551c035c069c14c2a06576a9f50752))

- Add support for python 3.6
  ([`dc8f385`](https://github.com/kalekundert/parametrize_from_file/commit/dc8f3856896805102c89314654800234a1c827a4))

- Install the local version of this package
  ([`e539e81`](https://github.com/kalekundert/parametrize_from_file/commit/e539e818547d2fd7daac515542f7d4518e00620c))

- Remove autoclasstoc doc dependency
  ([`dc0aefc`](https://github.com/kalekundert/parametrize_from_file/commit/dc0aefc23ca48d61cc4bcfbc00d27ce9e99370ee))

- Remove this package from the requirements file
  ([`cf80457`](https://github.com/kalekundert/parametrize_from_file/commit/cf80457e0d27211101e0013cdd34396189a626fd))

- Specify which version of arrow to use when building docs
  ([`4ca3325`](https://github.com/kalekundert/parametrize_from_file/commit/4ca3325486f7658a72fa06f792d17928b16f505e))

- Try using a requirements file to satisfy ReadTheDocs
  ([`fa569c8`](https://github.com/kalekundert/parametrize_from_file/commit/fa569c8c4fb8765295815e43939c80a2d066c222))

### Documentation

- Fix punctuation
  ([`6aa39db`](https://github.com/kalekundert/parametrize_from_file/commit/6aa39db9a2b654820309a7b47ebf4d1ec8aaca6a))

- Tweak some wording
  ([`f392eb7`](https://github.com/kalekundert/parametrize_from_file/commit/f392eb7f0854706262e54b4970961a56aaabaeed))


## v0.1.0 (2020-12-03)

### Documentation

- Initial documentation
  ([`597abeb`](https://github.com/kalekundert/parametrize_from_file/commit/597abeb790823a807c60bd607e559ab2af445265))

### Features

- Give more helpful schema errors
  ([`aac84a0`](https://github.com/kalekundert/parametrize_from_file/commit/aac84a0f16ab1392fdc51e807edfdc6b042b4cc2))

### Refactoring

- The Params class is outside the scope of this module
  ([`2b5a638`](https://github.com/kalekundert/parametrize_from_file/commit/2b5a638f2383aa2be8d7aae540c1f7633108e758))


## v0.0.1 (2020-12-02)

### Bug Fixes

- Avoid using walrus operator
  ([`3775077`](https://github.com/kalekundert/parametrize_from_file/commit/37750776baaf6783edb2f279127ffdcc1dafb167))

- Use a functools.wrap() signature compatible with python<=3.8
  ([`2e2b60d`](https://github.com/kalekundert/parametrize_from_file/commit/2e2b60dce4083a3b98d77f1fe067b0a0baaad89b))

### Chores

- Fix whitespace error
  ([`cdc7fdf`](https://github.com/kalekundert/parametrize_from_file/commit/cdc7fdfb7063ea01269e4e15729a1e107181e5b9))

- Install flit when running tests
  ([`204d7db`](https://github.com/kalekundert/parametrize_from_file/commit/204d7db510969b4f4f91dd7c2c80f2228aa72b70))

- Use 'toml' instead of 'rtoml'
  ([`fa96633`](https://github.com/kalekundert/parametrize_from_file/commit/fa966333f3022966106793effaf41c646602ac02))

'rtoml' is faster and more robust, but harder to get working in CI environments because it requires
  rust to be installed. Since this package is meant to be used for testing, I don't want to add that
  hurdle.
