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


## Emscripten WASM

conan source .
conan install . skia/canvaskit.0.38.0 --build=missing -s os=Emscripten -s arch=wasm -s compiler=clang -s compiler.version=17 -s compiler.libcxx=libc++ -s compiler.cppstd=20 -s:b os=Windows
conan build .
conan export-pkg . skia/canvaskit.0.38.0@ksytek/testing

The build step fails on:

```
FAILED: obj/src/ports/typeface_freetype.SkFontHost_FreeType.o
D:\dev\.env\.conan\data\emsdk\3.1.31\_\_\package\89721c0f92d5036aff276518054ee3d87ea2ef5f\bin/upstream/emscripten/em++.bat -MD -MF obj/src/ports/typeface_freetype.SkFontHost_FreeType.o.d -DNDEBUG -DSK_ENABLE_SKSL -DSK_ENABLE_PRECOMPILE -DSKNX_NO_SIMD -DSK_DISABLE_A
AA -DSK_FORCE_8_BYTE_ALIGNMENT -DSK_DISABLE_TRACING -DSK_DISABLE_LEGACY_SHADERCONTEXT -DSK_ASSUME_WEBGL=1 -DSK_USE_WEBGL -DSK_GAMMA_APPLY_TO_A8 -DSKIA_IMPLEMENTATION=1 "-DSK_FREETYPE_MINIMUM_RUNTIME_VERSION=(((FREETYPE_MAJOR) << 24) | ((FREETYPE_MINOR) << 16) | ((F
REETYPE_PATCH) << 8))" -DFT_CONFIG_MODULES_H=<freetype-no-type1/freetype/config/ftmodule.h> -DFT_CONFIG_OPTIONS_H=<freetype-no-type1/freetype/config/ftoption.h> -DFT_CONFIG_OPTION_USE_ZLIB -DFT_CONFIG_OPTION_USE_BROTLI -DFT_CONFIG_OPTION_SVG -I../src -Wno-attribute
s -ffp-contract=off -fstrict-aliasing -fPIC -fvisibility=hidden --sysroot=D:\dev\.env\.conan\data\emsdk\3.1.31\_\_\package\89721c0f92d5036aff276518054ee3d87ea2ef5f\bin/upstream/emscripten/cache/sysroot -O3 -isystem D:/dev/libs/conan/conan-center-index/recipes/skia/
all/src/third_party/freetype2/include -isystem D:/dev/libs/conan/conan-center-index/recipes/skia/all/src/third_party/freetype2/include/freetype-no-type1 -isystem D:/dev/libs/conan/conan-center-index/recipes/skia/all/src/third_party/externals/freetype/include -std=c++17 -fvisibility-inlines-hidden -fno-exceptions -fno-rtti -c ../src/src/ports/SkFontHost_FreeType.cpp -o obj/src/ports/typeface_freetype.SkFontHost_FreeType.o
The system cannot find the path specified.
```

Removing the `FT_CONFIG_OPTIONS` and `FT_CONFIG_MODULES` definitions fixes it (or comment the
following lines in `third_party/freetype2/BUILD.gn`) but it may have unintended consequences:

```
      public_defines += [
        "FT_CONFIG_MODULES_H=<freetype-no-type1/freetype/config/ftmodule.h>",
        "FT_CONFIG_OPTIONS_H=<freetype-no-type1/freetype/config/ftoption.h>",
      ]
```
