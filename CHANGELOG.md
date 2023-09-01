# CHANGELOG



## v0.18.0 (2023-09-01)

### Documentation

* docs: update examples to use &#39;import parametrize_from_file as pff&#39; ([`794806b`](https://github.com/kalekundert/parametrize_from_file/commit/794806b5fda08e47cd30c989b0799eda9cb8c1c1))

* docs: fix typos ([`7681380`](https://github.com/kalekundert/parametrize_from_file/commit/76813801e7b3544d827023b924bcaf916286069c))

* docs: fix syntax highlighting ([`fbc1e14`](https://github.com/kalekundert/parametrize_from_file/commit/fbc1e14d68bcfb0e2ccd0526d7d6d47f9d31df33))

* docs: make README example more intuitive ([`277ba97`](https://github.com/kalekundert/parametrize_from_file/commit/277ba9735dee3ce862edd65da709562e38badf08))

### Feature

* feat: allow schema functions to add marks ([`f1f0c2b`](https://github.com/kalekundert/parametrize_from_file/commit/f1f0c2b18e6dd7140f8d393bf23cd62a7203021c))

### Fix

* fix: improve error messages ([`3a92dbf`](https://github.com/kalekundert/parametrize_from_file/commit/3a92dbf7fca3fbecac3b425ab3574df3d9983356))

### Unknown

* Merge branch &#39;master&#39; of github.com:kalekundert/parametrize_from_file ([`c701520`](https://github.com/kalekundert/parametrize_from_file/commit/c7015201da2db23f2dab73a9d7899d6e4856fdd2))


## v0.17.1 (2023-06-22)

### Chore

* chore: replace contextlib2 with contextlib (#18)

contextlib.nullcontext was added in Python 3.7 which is the oldest supported version ([`9c68f20`](https://github.com/kalekundert/parametrize_from_file/commit/9c68f20c8e75cc00b92d5ae73e2a30c7867bbd7a))

### Documentation

* docs: fix documentation link ([`da99cc5`](https://github.com/kalekundert/parametrize_from_file/commit/da99cc545f55b5e0201baa9771c4f5368015250f))

* docs: fix CI badge ([`a47c0c1`](https://github.com/kalekundert/parametrize_from_file/commit/a47c0c11d63a80aacb235302961d8374f75ae516))

### Test

* test: account for changed module name of `nt.load()` ([`1fb2b7b`](https://github.com/kalekundert/parametrize_from_file/commit/1fb2b7bf42fddaf1f6578235ba179bcdc7635da6))

### Unknown

* Merge branch &#39;master&#39; of github.com:kalekundert/parametrize_from_file ([`309056d`](https://github.com/kalekundert/parametrize_from_file/commit/309056ddc74db9822bf699519fe6b8261395c8b0))


## v0.17.0 (2022-08-23)

### Feature

* feat: allow multiple cast functions for each field ([`c026e8b`](https://github.com/kalekundert/parametrize_from_file/commit/c026e8b9989a9c67c6c45f70a3427207e43d83c0))


## v0.16.0 (2022-06-14)

### Feature

* feat: don&#39;t eval/exec the error() context managers ([`9d8b2af`](https://github.com/kalekundert/parametrize_from_file/commit/9d8b2af5834b88e42230a75a88582f1c35a934a5))


## v0.15.0 (2022-06-10)

### Feature

* feat: provide schema functions tailored for testing

- Add the `cast` and `defaults` schema functions.

- Refactor `error` and `error_or` into standalone functions that don&#39;t
  depend on the `Namespace` class.  The corresponding `Namespace`
  methods remain, but are now just thin wrappers.

- Interpret iterable schema arguments as pipelines.

- Get rid of the voluptuous dependency.

Fixes #16 ([`275c79d`](https://github.com/kalekundert/parametrize_from_file/commit/275c79d3cfea5951aff624b0a8300fc65d875936))


## v0.14.0 (2022-04-18)

### Documentation

* docs: use sentence-case for page titles ([`0f30c42`](https://github.com/kalekundert/parametrize_from_file/commit/0f30c421da9b6915864070c3b2cf6970e88cadf4))

* docs: use python 3.7 to build the docs ([`6bd272c`](https://github.com/kalekundert/parametrize_from_file/commit/6bd272cf5afd2eafa014581b730db369afc65983))

### Feature

* feat: allow loaders to be overridden locally ([`466fa31`](https://github.com/kalekundert/parametrize_from_file/commit/466fa31075427da63cb2f16529dbebde6c285d18))

* feat: allow preprocess() to get additional contextual information ([`a482725`](https://github.com/kalekundert/parametrize_from_file/commit/a4827256b1157a464c7c543a528cc3a826e5494a))

### Unknown

* Merge branch &#39;master&#39; of github.com:kalekundert/parametrize_from_file ([`5cda235`](https://github.com/kalekundert/parametrize_from_file/commit/5cda2352669d8dca11bdedfb30fb92f89ef107d3))


## v0.13.1 (2022-04-08)

### Chore

* chore: drop support for python 3.6 ([`dca2288`](https://github.com/kalekundert/parametrize_from_file/commit/dca2288856207cbc053d39b4648eaf57ce9c3cc5))

* chore: upgrade `pyproject.toml` as per PEP 621 ([`9783b75`](https://github.com/kalekundert/parametrize_from_file/commit/9783b75a4269971f45febd9e7cfb054f7a7b6cd6))

### Documentation

* docs: add a tutorial on temporary files ([`09aa784`](https://github.com/kalekundert/parametrize_from_file/commit/09aa78405334f5ea7b44be121462ac0e50f37d26))

* docs: fix pytest cross-references ([`33580bb`](https://github.com/kalekundert/parametrize_from_file/commit/33580bbb8982073f90007f4cd0f47528c7df6ea0))

* docs: tweak wording ([`f791460`](https://github.com/kalekundert/parametrize_from_file/commit/f7914601cba64e256efdc5b1c73f5bbd53933fff))

### Fix

* fix: improve error messages ([`c1eaa78`](https://github.com/kalekundert/parametrize_from_file/commit/c1eaa78d7307ef09f97c069f621ff81ed428f847))

### Test

* test: add pytest_tmp_files dependency ([`bc71d5e`](https://github.com/kalekundert/parametrize_from_file/commit/bc71d5ee20e70265c003d74329a8c8b5285bca64))


## v0.13.0 (2022-01-17)

### Feature

* feat: allow assertions on the direct causes of exceptions ([`d4d2be9`](https://github.com/kalekundert/parametrize_from_file/commit/d4d2be928b25048e3a4fac4edb6b5a54c0958be5))


## v0.12.0 (2022-01-17)

### Chore

* chore: treat all warnings as errors in CI ([`97f215c`](https://github.com/kalekundert/parametrize_from_file/commit/97f215c7ca1341b282d4b5d180f2639420eacbef))

### Feature

* feat: allow deferred eval/exec to be invoked by name

I think this makes the code easier to read. ([`08d0bf2`](https://github.com/kalekundert/parametrize_from_file/commit/08d0bf2869989f76a188de98c56891178c80c3cf))


## v0.11.1 (2022-01-13)

### Fix

* fix: migrate to more_itertools.zip_broadcast()

This avoids a warning in python&gt;=3.10

Fixes #13 ([`cdf37c3`](https://github.com/kalekundert/parametrize_from_file/commit/cdf37c377fc7c65b6852c35e277b82cec7c0b864))


## v0.11.0 (2022-01-12)

### Documentation

* docs: fix typos ([`38cea18`](https://github.com/kalekundert/parametrize_from_file/commit/38cea1863d62ec1202dfc94ed730e099c38e7bb8))

* docs: fix python snippet examples ([`5497205`](https://github.com/kalekundert/parametrize_from_file/commit/5497205cd718d4898659f4924fd81a139b1b2d4e))

### Feature

* feat: add empty_ok() for voluptuous schema ([`6fd446d`](https://github.com/kalekundert/parametrize_from_file/commit/6fd446dd8017f38cfff02beec6c0e1d7a90e2379))


## v0.10.0 (2022-01-04)

### Feature

* feat: get multiple variables from executed snippets ([`c43c57a`](https://github.com/kalekundert/parametrize_from_file/commit/c43c57af9045586f5ab81f9cd3c86bb523d6c60b))


## v0.9.1 (2021-12-23)

### Fix

* fix: improve debug message ([`08fa038`](https://github.com/kalekundert/parametrize_from_file/commit/08fa0382d20bbc73312f11232105fa5a1f325357))


## v0.9.0 (2021-12-23)

### Feature

* feat: try to import the voluptuous submodule ([`4d5cca4`](https://github.com/kalekundert/parametrize_from_file/commit/4d5cca4581b82526acd1174d66256281b48d9185))


## v0.8.0 (2021-12-23)

### Feature

* feat: allow exec() and eval() to be deferred

This commit also gets rid of exec_and_lookup(), which was basically just
doing one specific kind of deferral.  Fixes #8. ([`b8cf9d5`](https://github.com/kalekundert/parametrize_from_file/commit/b8cf9d5a10fa9389fb4f90980cce5cc48b30a5b0))

* feat: make namespaces immutable, add more error checks

- Make namespaces immutable, fix #10.
- Provide more flexible exception assertions, fix #9.
- Add sensible `__bool__()` implementation for error context managers,
  fix #12. ([`8e52066`](https://github.com/kalekundert/parametrize_from_file/commit/8e52066babd80bee0ca3ff2786ddb325ad16110e))

### Test

* test: make sure namespaces with unpickleable values can be copied ([`1c61ee8`](https://github.com/kalekundert/parametrize_from_file/commit/1c61ee873e8abc90b052adf309f275b58950dabd))


## v0.7.1 (2021-10-07)

### Fix

* fix: include voluptuous dependency ([`62fc60b`](https://github.com/kalekundert/parametrize_from_file/commit/62fc60ba8e1dfe0ab93a8f96b9e3b8e2dca1292d))


## v0.7.0 (2021-10-06)

### Documentation

* docs: tweak wording ([`f3be56a`](https://github.com/kalekundert/parametrize_from_file/commit/f3be56ad706b999234c6a7758f16fca3dc0a47e4))

### Feature

* feat: support eval/exec&#39;ing mocks ([`121995a`](https://github.com/kalekundert/parametrize_from_file/commit/121995a6799334ed534a26aecfa5d23331f90d61))


## v0.6.0 (2021-10-06)

### Feature

* feat: support parametrized fixtures

Fixes #6 ([`e9a95c4`](https://github.com/kalekundert/parametrize_from_file/commit/e9a95c4c324f9af7579cb0c6352f1292c7e7b9d7))

* feat: support indirect parametrization

Fixes #7 ([`34308c4`](https://github.com/kalekundert/parametrize_from_file/commit/34308c4cec6af0fe8fe74c20c07f49d7b0390e8c))

### Test

* test: add cases that break mi.zip_broadcast()

See https://github.com/more-itertools/more-itertools/issues/561 ([`980dd3b`](https://github.com/kalekundert/parametrize_from_file/commit/980dd3bff94d2ac6756494f2b2f78c6bdeaeea75))


## v0.5.1 (2021-08-29)

### Chore

* chore: merge cookiecutter ([`9eef273`](https://github.com/kalekundert/parametrize_from_file/commit/9eef273505d7202573fbbc7def8c5c647387c837))

* chore: apply cookiecutter ([`279a595`](https://github.com/kalekundert/parametrize_from_file/commit/279a595845b1adf87ae4fd24f5cec5295fdc748f))

### Fix

* fix: correctly format error messages with braces ([`7caaa31`](https://github.com/kalekundert/parametrize_from_file/commit/7caaa31da50930918efd0a4389bc45c860435027))


## v0.5.0 (2021-08-22)

### Documentation

* docs: add examples of my projects that use this package ([`f1e59f3`](https://github.com/kalekundert/parametrize_from_file/commit/f1e59f3b0e7040687b9918461a67fc6297ca6bb4))

* docs: install dependencies ([`90721fd`](https://github.com/kalekundert/parametrize_from_file/commit/90721fd11f7dacc68bb70f125aa6348bf2f5e606))

* docs: install dependencies ([`6ca7ae8`](https://github.com/kalekundert/parametrize_from_file/commit/6ca7ae89b27af50172ae85e833e42ea7b5919a27))

### Feature

* feat: allow multiple paths/keys to be specified ([`fe6696a`](https://github.com/kalekundert/parametrize_from_file/commit/fe6696a30edb878d677304f13ff38adc5fc15478))

* feat: add the load_parameters() function

I don&#39;t have a specific use for this API, but it seems like a good thing
to have.  It also forced me to refactor the code a bit to better
separate responsibilities. ([`5c8af43`](https://github.com/kalekundert/parametrize_from_file/commit/5c8af43965beca80cdd87dfcf52ed9c89e9334c1))

* feat: add the *preprocess* argument ([`219aa9f`](https://github.com/kalekundert/parametrize_from_file/commit/219aa9f37429b876171b48c4c01ebefa9af4fb4f))

### Fix

* fix: check that the schema returns a dict ([`85ecdf1`](https://github.com/kalekundert/parametrize_from_file/commit/85ecdf1d810ce58f88a28eeddba370a87962ba91))

### Unknown

* Merge branch &#39;master&#39; of github.com:kalekundert/parametrize_from_file ([`7ef4818`](https://github.com/kalekundert/parametrize_from_file/commit/7ef4818b219526a1e8086c65aa335d1998c7ce7a))


## v0.4.0 (2021-08-20)

### Documentation

* docs: slightly clarify error messages ([`7393ee0`](https://github.com/kalekundert/parametrize_from_file/commit/7393ee072ecdb8c9cb960be0d7abc8e9ecdcd212))

### Feature

* feat: add the Namespace eval/exec/error helper ([`e0c8523`](https://github.com/kalekundert/parametrize_from_file/commit/e0c85238997bd521c361463e6794e2e7ea299a0d))

### Unknown

* Merge branch &#39;master&#39; of github.com:kalekundert/parametrize_from_file ([`d9e4a06`](https://github.com/kalekundert/parametrize_from_file/commit/d9e4a064ac4e5b0ad15219cc0bf75d38b9da2e77))


## v0.3.0 (2020-12-07)

### Chore

* chore: remove stale imports ([`707ac13`](https://github.com/kalekundert/parametrize_from_file/commit/707ac13f282f02075ca9c153f650aa620b2d195f))

### Feature

* feat: accept any callable as the schema

Fixes #1 ([`2f3d1e1`](https://github.com/kalekundert/parametrize_from_file/commit/2f3d1e15129ebc70e7d5b3a2acbda3e5d7186a4a))


## v0.2.0 (2020-12-04)

### Feature

* feat: rename the &#39;key&#39; argument ([`25d7879`](https://github.com/kalekundert/parametrize_from_file/commit/25d7879160c46a1b3d63eb3cad37e184e2c89144))


## v0.1.1 (2020-12-04)

### Chore

* chore: add support for python 3.6 ([`dc8f385`](https://github.com/kalekundert/parametrize_from_file/commit/dc8f3856896805102c89314654800234a1c827a4))

* chore: install the local version of this package ([`e539e81`](https://github.com/kalekundert/parametrize_from_file/commit/e539e818547d2fd7daac515542f7d4518e00620c))

* chore: remove this package from the requirements file ([`cf80457`](https://github.com/kalekundert/parametrize_from_file/commit/cf80457e0d27211101e0013cdd34396189a626fd))

* chore: try using a requirements file to satisfy ReadTheDocs ([`fa569c8`](https://github.com/kalekundert/parametrize_from_file/commit/fa569c8c4fb8765295815e43939c80a2d066c222))

* chore: specify which version of arrow to use when building docs ([`4ca3325`](https://github.com/kalekundert/parametrize_from_file/commit/4ca3325486f7658a72fa06f792d17928b16f505e))

* chore: add dateutil as doc dependency ([`a016b2e`](https://github.com/kalekundert/parametrize_from_file/commit/a016b2e153551c035c069c14c2a06576a9f50752))

* chore: remove autoclasstoc doc dependency ([`dc0aefc`](https://github.com/kalekundert/parametrize_from_file/commit/dc0aefc23ca48d61cc4bcfbc00d27ce9e99370ee))

### Documentation

* docs: tweak some wording ([`f392eb7`](https://github.com/kalekundert/parametrize_from_file/commit/f392eb7f0854706262e54b4970961a56aaabaeed))

* docs: fix punctuation ([`6aa39db`](https://github.com/kalekundert/parametrize_from_file/commit/6aa39db9a2b654820309a7b47ebf4d1ec8aaca6a))

### Fix

* fix: don&#39;t apply the schema to &#39;id&#39; and &#39;marks&#39; ([`e18e931`](https://github.com/kalekundert/parametrize_from_file/commit/e18e931749cf83370a88ebadf4a587e07566b41e))

### Refactor

* refactor: the Params class is outside the scope of this module ([`2b5a638`](https://github.com/kalekundert/parametrize_from_file/commit/2b5a638f2383aa2be8d7aae540c1f7633108e758))

### Unknown

* Merge branch &#39;master&#39; of github.com:kalekundert/parametrize_from_file ([`8768ac2`](https://github.com/kalekundert/parametrize_from_file/commit/8768ac24b0e2283d3ec9f6d64c61b16f39f15db9))


## v0.1.0 (2020-12-03)

### Documentation

* docs: initial documentation ([`597abeb`](https://github.com/kalekundert/parametrize_from_file/commit/597abeb790823a807c60bd607e559ab2af445265))

### Feature

* feat: give more helpful schema errors ([`aac84a0`](https://github.com/kalekundert/parametrize_from_file/commit/aac84a0f16ab1392fdc51e807edfdc6b042b4cc2))


## v0.0.1 (2020-12-02)

### Chore

* chore: use &#39;toml&#39; instead of &#39;rtoml&#39;

&#39;rtoml&#39; is faster and more robust, but harder to get working in CI
environments because it requires rust to be installed.  Since this
package is meant to be used for testing, I don&#39;t want to add that
hurdle. ([`fa96633`](https://github.com/kalekundert/parametrize_from_file/commit/fa966333f3022966106793effaf41c646602ac02))

* chore: install flit when running tests ([`204d7db`](https://github.com/kalekundert/parametrize_from_file/commit/204d7db510969b4f4f91dd7c2c80f2228aa72b70))

* chore: fix whitespace error ([`cdc7fdf`](https://github.com/kalekundert/parametrize_from_file/commit/cdc7fdfb7063ea01269e4e15729a1e107181e5b9))

### Fix

* fix: use a functools.wrap() signature compatible with python&lt;=3.8 ([`2e2b60d`](https://github.com/kalekundert/parametrize_from_file/commit/2e2b60dce4083a3b98d77f1fe067b0a0baaad89b))

* fix: avoid using walrus operator ([`3775077`](https://github.com/kalekundert/parametrize_from_file/commit/37750776baaf6783edb2f279127ffdcc1dafb167))

### Unknown

* initial implementation and testing ([`61fd2aa`](https://github.com/kalekundert/parametrize_from_file/commit/61fd2aaaa32a266e3f78f39c0f41429eda28c115))

* initial commit ([`cae9460`](https://github.com/kalekundert/parametrize_from_file/commit/cae94609ffad2762b1729cc37bb89fd2157ef8b3))
