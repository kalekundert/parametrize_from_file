# Changelog

<!--next-version-placeholder-->

## v0.14.0 (2022-04-18)
### Feature
* Allow loaders to be overridden locally ([`466fa31`](https://github.com/kalekundert/parametrize_from_file/commit/466fa31075427da63cb2f16529dbebde6c285d18))
* Allow preprocess() to get additional contextual information ([`a482725`](https://github.com/kalekundert/parametrize_from_file/commit/a4827256b1157a464c7c543a528cc3a826e5494a))

### Documentation
* Use sentence-case for page titles ([`0f30c42`](https://github.com/kalekundert/parametrize_from_file/commit/0f30c421da9b6915864070c3b2cf6970e88cadf4))
* Use python 3.7 to build the docs ([`6bd272c`](https://github.com/kalekundert/parametrize_from_file/commit/6bd272cf5afd2eafa014581b730db369afc65983))

## v0.13.1 (2022-04-08)
### Fix
* Improve error messages ([`c1eaa78`](https://github.com/kalekundert/parametrize_from_file/commit/c1eaa78d7307ef09f97c069f621ff81ed428f847))

### Documentation
* Add a tutorial on temporary files ([`09aa784`](https://github.com/kalekundert/parametrize_from_file/commit/09aa78405334f5ea7b44be121462ac0e50f37d26))
* Fix pytest cross-references ([`33580bb`](https://github.com/kalekundert/parametrize_from_file/commit/33580bbb8982073f90007f4cd0f47528c7df6ea0))
* Tweak wording ([`f791460`](https://github.com/kalekundert/parametrize_from_file/commit/f7914601cba64e256efdc5b1c73f5bbd53933fff))

## v0.13.0 (2022-01-17)
### Feature
* Allow assertions on the direct causes of exceptions ([`d4d2be9`](https://github.com/kalekundert/parametrize_from_file/commit/d4d2be928b25048e3a4fac4edb6b5a54c0958be5))

## v0.12.0 (2022-01-17)
### Feature
* Allow deferred eval/exec to be invoked by name ([`08d0bf2`](https://github.com/kalekundert/parametrize_from_file/commit/08d0bf2869989f76a188de98c56891178c80c3cf))

## v0.11.1 (2022-01-13)
### Fix
* Migrate to more_itertools.zip_broadcast() ([`cdf37c3`](https://github.com/kalekundert/parametrize_from_file/commit/cdf37c377fc7c65b6852c35e277b82cec7c0b864))

## v0.11.0 (2022-01-12)
### Feature
* Add empty_ok() for voluptuous schema ([`6fd446d`](https://github.com/kalekundert/parametrize_from_file/commit/6fd446dd8017f38cfff02beec6c0e1d7a90e2379))

### Documentation
* Fix typos ([`38cea18`](https://github.com/kalekundert/parametrize_from_file/commit/38cea1863d62ec1202dfc94ed730e099c38e7bb8))
* Fix python snippet examples ([`5497205`](https://github.com/kalekundert/parametrize_from_file/commit/5497205cd718d4898659f4924fd81a139b1b2d4e))

## v0.10.0 (2022-01-04)
### Feature
* Get multiple variables from executed snippets ([`c43c57a`](https://github.com/kalekundert/parametrize_from_file/commit/c43c57af9045586f5ab81f9cd3c86bb523d6c60b))

## v0.9.1 (2021-12-23)
### Fix
* Improve debug message ([`08fa038`](https://github.com/kalekundert/parametrize_from_file/commit/08fa0382d20bbc73312f11232105fa5a1f325357))

## v0.9.0 (2021-12-23)
### Feature
* Try to import the voluptuous submodule ([`4d5cca4`](https://github.com/kalekundert/parametrize_from_file/commit/4d5cca4581b82526acd1174d66256281b48d9185))

## v0.8.0 (2021-12-23)
### Feature
* Allow exec() and eval() to be deferred ([`b8cf9d5`](https://github.com/kalekundert/parametrize_from_file/commit/b8cf9d5a10fa9389fb4f90980cce5cc48b30a5b0))
* Make namespaces immutable, add more error checks ([`8e52066`](https://github.com/kalekundert/parametrize_from_file/commit/8e52066babd80bee0ca3ff2786ddb325ad16110e))

## v0.7.1 (2021-10-07)
### Fix
* Include voluptuous dependency ([`62fc60b`](https://github.com/kalekundert/parametrize_from_file/commit/62fc60ba8e1dfe0ab93a8f96b9e3b8e2dca1292d))

## v0.7.0 (2021-10-06)
### Feature
* Support eval/exec'ing mocks ([`121995a`](https://github.com/kalekundert/parametrize_from_file/commit/121995a6799334ed534a26aecfa5d23331f90d61))

### Documentation
* Tweak wording ([`f3be56a`](https://github.com/kalekundert/parametrize_from_file/commit/f3be56ad706b999234c6a7758f16fca3dc0a47e4))

## v0.6.0 (2021-10-06)
### Feature
* Support parametrized fixtures ([`e9a95c4`](https://github.com/kalekundert/parametrize_from_file/commit/e9a95c4c324f9af7579cb0c6352f1292c7e7b9d7))
* Support indirect parametrization ([`34308c4`](https://github.com/kalekundert/parametrize_from_file/commit/34308c4cec6af0fe8fe74c20c07f49d7b0390e8c))

## v0.5.1 (2021-08-29)
### Fix
* Correctly format error messages with braces ([`7caaa31`](https://github.com/kalekundert/parametrize_from_file/commit/7caaa31da50930918efd0a4389bc45c860435027))

## v0.5.0 (2021-08-22)
### Feature
* Allow multiple paths/keys to be specified ([`fe6696a`](https://github.com/kalekundert/parametrize_from_file/commit/fe6696a30edb878d677304f13ff38adc5fc15478))
* Add the load_parameters() function ([`5c8af43`](https://github.com/kalekundert/parametrize_from_file/commit/5c8af43965beca80cdd87dfcf52ed9c89e9334c1))
* Add the *preprocess* argument ([`219aa9f`](https://github.com/kalekundert/parametrize_from_file/commit/219aa9f37429b876171b48c4c01ebefa9af4fb4f))

### Fix
* Check that the schema returns a dict ([`85ecdf1`](https://github.com/kalekundert/parametrize_from_file/commit/85ecdf1d810ce58f88a28eeddba370a87962ba91))

### Documentation
* Add examples of my projects that use this package ([`f1e59f3`](https://github.com/kalekundert/parametrize_from_file/commit/f1e59f3b0e7040687b9918461a67fc6297ca6bb4))
* Install dependencies ([`90721fd`](https://github.com/kalekundert/parametrize_from_file/commit/90721fd11f7dacc68bb70f125aa6348bf2f5e606))
* Install dependencies ([`6ca7ae8`](https://github.com/kalekundert/parametrize_from_file/commit/6ca7ae89b27af50172ae85e833e42ea7b5919a27))

## v0.4.0 (2021-08-20)
### Feature
* Add the Namespace eval/exec/error helper ([`e0c8523`](https://github.com/kalekundert/parametrize_from_file/commit/e0c85238997bd521c361463e6794e2e7ea299a0d))

### Documentation
* Slightly clarify error messages ([`7393ee0`](https://github.com/kalekundert/parametrize_from_file/commit/7393ee072ecdb8c9cb960be0d7abc8e9ecdcd212))

## v0.3.0 (2020-12-07)
### Feature
* Accept any callable as the schema ([`2f3d1e1`](https://github.com/kalekundert/parametrize_from_file/commit/2f3d1e15129ebc70e7d5b3a2acbda3e5d7186a4a))

## v0.2.0 (2020-12-04)
### Feature
* Rename the 'key' argument ([`25d7879`](https://github.com/kalekundert/parametrize_from_file/commit/25d7879160c46a1b3d63eb3cad37e184e2c89144))

## v0.1.1 (2020-12-04)
### Fix
* Don't apply the schema to 'id' and 'marks' ([`e18e931`](https://github.com/kalekundert/parametrize_from_file/commit/e18e931749cf83370a88ebadf4a587e07566b41e))

### Documentation
* Tweak some wording ([`f392eb7`](https://github.com/kalekundert/parametrize_from_file/commit/f392eb7f0854706262e54b4970961a56aaabaeed))
* Fix punctuation ([`6aa39db`](https://github.com/kalekundert/parametrize_from_file/commit/6aa39db9a2b654820309a7b47ebf4d1ec8aaca6a))

## v0.1.0 (2020-12-03)
### Feature
* Give more helpful schema errors ([`aac84a0`](https://github.com/kalekundert/parametrize_from_file/commit/aac84a0f16ab1392fdc51e807edfdc6b042b4cc2))

### Documentation
* Initial documentation ([`597abeb`](https://github.com/kalekundert/parametrize_from_file/commit/597abeb790823a807c60bd607e559ab2af445265))

## v0.0.1 (2020-12-02)
### Fix
* Use a functools.wrap() signature compatible with python<=3.8 ([`2e2b60d`](https://github.com/kalekundert/parametrize_from_file/commit/2e2b60dce4083a3b98d77f1fe067b0a0baaad89b))
* Avoid using walrus operator ([`3775077`](https://github.com/kalekundert/parametrize_from_file/commit/37750776baaf6783edb2f279127ffdcc1dafb167))
