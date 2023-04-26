# README


## VS2019 release

conan source . skia/m114
conan install . skia/m114 --build=missing
conan build .
conan export-pkg . skia/m114@tnz/testing


## Android

conan source .
conan install . skia/chrome.m114 --build=missing -s os=Android -s os.api_level=21 -s arch=armv8 -s compiler=clang -s compiler.version=16 -s compiler.libcxx=libc++ -s compiler.cppstd=20 -s:b os=Windows
conan build .
conan export-pkg . skia/chrome.m114@tnz/testing
