import os, re

from conan import ConanFile
from conan.tools.files import get, collect_libs, export_conandata_patches, apply_conandata_patches
from conan.tools.layout import basic_layout
from conan.errors import ConanException, ConanInvalidConfiguration


required_conan_version = ">=1.59.0"


class SkiaConan(ConanFile):
    name = "Skia"
    version = "canvaskit.0.38.0"
    license = "BSD 3-Clause"
    url = "https://github.com/conan-io/conan-center-index"
    homepage = "https://skia.org"
    topics = ("skia", "graphics", "rendering", "vector", "2d", "3d")
    description = "A 2D/3D Vector rendering engine"
    settings = "os", "compiler", "build_type", "arch"

    options = {
        "is_official_build" : [True, False],
        "is_component_build": [True, False],
        "skia_build_for_debugger": [True, False],
        "skia_canvaskit_enable_alias_font" : [True, False],
        "skia_canvaskit_enable_canvas_bindings" : [True, False],
        "skia_canvaskit_enable_debugger" : [True, False],
        "skia_canvaskit_enable_effects_deserialization" : [True, False],
        "skia_canvaskit_enable_embedded_font" : [True, False],
        "skia_canvaskit_enable_font" : [True, False],
        "skia_canvaskit_enable_matrix_helper" : [True, False],
        "skia_canvaskit_enable_pathops" : [True, False],
        "skia_canvaskit_enable_rt_shader" : [True, False],
        "skia_canvaskit_enable_skottie" : [True, False],
        "skia_canvaskit_enable_skp_serialization" : [True, False],
        "skia_canvaskit_enable_sksl_trace" : [True, False],
        "skia_canvaskit_enable_paragraph" : [True, False],
        "skia_canvaskit_include_viewer" : [True, False],
        "skia_canvaskit_profile_build" : [True, False],
        "skia_canvaskit_force_tracing" : [True, False],
        "skia_canvaskit_legacy_draw_vertices_blend_mode" : [True, False],
        "skia_canvaskit_enable_webgpu" : [True, False],
        "skia_canvaskit_enable_webgl" : [True, False],
        "skia_enable_discrete_gpu" : [True, False],
        "skia_enable_flutter_defines" : [True, False],
        "skia_enable_fontmgr_android" : [True, False],
        "skia_enable_fontmgr_custom_directory" : [True, False],
        "skia_enable_fontmgr_custom_embedded" : [True, False],
        "skia_enable_fontmgr_custom_empty" : [True, False],
        "skia_enable_fontmgr_empty" : [True, False],
        "skia_enable_fontmgr_fuchsia" : [True, False],
        "skia_enable_fontmgr_win" : [True, False],
        "skia_enable_fontmgr_win_gdi" : [True, False],
        "skia_enable_gpu" : [True, False],
        "skia_enable_pdf" : [True, False],
        "skia_enable_skottie" : [True, False],
        "skia_enable_skparagraph" : [True, False],
        "skia_enable_sksl_tracing" : [True, False],
        "skia_enable_skshaper" : [True, False],
        # "skia_enable_skunicode" : [True, False],
        "skia_enable_spirv_validation" : [True, False],
        "skia_enable_tools" : [True, False],
        "skia_enable_vulkan_debug_layers" : [True, False],
        "skia_fontmgr_factory": [None, "ANY"],
        "skia_generate_workarounds" : [True, False],
        "skia_use_angle" : [True, False],
        # "skia_use_client_icu" : [True, False],
        "skia_use_dawn" : [True, False],
        "skia_use_dng_sdk" : [True, False],
        "skia_use_egl" : [True, False],
        "skia_use_expat" : [True, False],
        "skia_use_fixed_gamma_text" : [True, False],
        "skia_use_fontconfig" : [True, False],
        "skia_use_fonthost_mac" : [True, False],
        "skia_use_freetype" : [True, False],
        "skia_use_freetype_woff2" : [True, False],
        "skia_use_harfbuzz" : [True, False],
        "skia_use_icu" : [True, False],
        "skia_use_libheif" : [True, False],
        "skia_use_libjpeg_turbo_encode" : [True, False],
        "skia_use_libjpeg_turbo_decode" : [True, False],
        # "skia_use_no_jpeg_encode" : [True, False],
        "skia_use_libpng_encode" : [True, False],
        "skia_use_libpng_decode" : [True, False],
        # "skia_use_no_png_encode" : [True, False],
        "skia_use_libwebp_encode" : [True, False],
        "skia_use_libwebp_decode" : [True, False],
        # "skia_use_no_webp_encode" : [True, False],
        "skia_use_lua" : [True, False],
        "skia_use_metal" : [True, False],
        "skia_use_piex" : [True, False],
        "skia_use_sfntly" : [True, False],
        # "skia_use_system_expat" : [True, False],
        # "skia_use_system_harfbuzz" : [True, False],
        "skia_use_system_icu" : [True, False],
        "skia_use_system_freetype2" : [True, False],
        "skia_use_system_libjpeg_turbo" : [True, False],
        "skia_use_system_libpng" : [True, False],
        "skia_use_system_libwebp" : [True, False],
        "skia_use_system_zlib" : [True, False],
        "skia_use_vulkan" : [True, False],
        "skia_use_webgl" : [True, False],
        "skia_use_webgpu" : [True, False],
        "skia_use_wuffs" : [True, False],
        "skia_use_x11" : [True, False],
        "skia_use_xps" : [True, False],
        "skia_use_zlib" : [True, False],
    }

    default_options = {
        "is_official_build" : True,
        "is_component_build":False,
        # Skia options
        "skia_build_for_debugger": False,
        "skia_canvaskit_enable_alias_font" : True,
        "skia_canvaskit_enable_canvas_bindings" : True,
        "skia_canvaskit_enable_debugger" : False,
        "skia_canvaskit_enable_effects_deserialization" : True,
        "skia_canvaskit_enable_embedded_font" : False,
        "skia_canvaskit_enable_font" : False,
        "skia_canvaskit_enable_matrix_helper" : True,
        "skia_canvaskit_enable_pathops" : True,
        "skia_canvaskit_enable_rt_shader" : True,
        "skia_canvaskit_enable_skottie" : True,
        "skia_canvaskit_enable_skp_serialization" : True,
        "skia_canvaskit_enable_sksl_trace" : True,
        "skia_canvaskit_enable_paragraph" : False,
        "skia_canvaskit_force_tracing" : False,
        "skia_canvaskit_include_viewer" : False,
        "skia_canvaskit_profile_build" : False,
        "skia_canvaskit_legacy_draw_vertices_blend_mode" : False,
        "skia_canvaskit_enable_webgpu" : False,
        "skia_canvaskit_enable_webgl" : False,
        "skia_enable_discrete_gpu" : True,
        "skia_enable_flutter_defines" : False,
        "skia_enable_fontmgr_android" : False,
        "skia_enable_fontmgr_custom_directory" : False,
        "skia_enable_fontmgr_custom_embedded" : False,
        "skia_enable_fontmgr_custom_empty" : False,
        "skia_enable_fontmgr_empty" : False,
        "skia_enable_fontmgr_fuchsia" : False,
        "skia_enable_fontmgr_win" : False,
        "skia_enable_fontmgr_win_gdi" : False,
        "skia_enable_gpu" : True,
        "skia_enable_pdf" : False,
        "skia_enable_skottie" : True,
        "skia_enable_skparagraph" : True,
        "skia_enable_sksl_tracing" : True,
        "skia_enable_skshaper" : True,
        # "skia_enable_skunicode": True,
        "skia_enable_spirv_validation" : False,
        "skia_enable_tools" : False,
        "skia_enable_vulkan_debug_layers" : False,
        "skia_fontmgr_factory": ":fontmgr_empty_factory",
        "skia_generate_workarounds" : False,
        "skia_use_angle" : False,
        # "skia_use_client_icu" : False,
        "skia_use_dawn" : False,
        "skia_use_dng_sdk" : False,
        "skia_use_egl" : False,
        "skia_use_expat" : False,
        "skia_use_fixed_gamma_text" : False,
        "skia_use_fontconfig" : False,
        "skia_use_fonthost_mac" : False,
        "skia_use_freetype" : True,
        "skia_use_freetype_woff2" : True,
        "skia_use_harfbuzz" : False,
        "skia_use_icu" : False,
        "skia_use_libheif" : False,
        "skia_use_libjpeg_turbo_encode" : True,
        "skia_use_libjpeg_turbo_decode" : True,
        # "skia_use_no_jpeg_encode" : False,
        "skia_use_libpng_encode" : True,
        "skia_use_libpng_decode" : True,
        # "skia_use_no_png_encode" : False,
        "skia_use_libwebp_encode" : True,
        "skia_use_libwebp_decode" : True,
        # "skia_use_no_webp_encode" : False,
        "skia_use_lua" : False,
        "skia_use_metal" : False,
        "skia_use_piex" : False,
        "skia_use_sfntly" : True,
        # "skia_use_system_expat" : True,
        # "skia_use_system_harfbuzz" : False,
        "skia_use_system_icu" : False,
        "skia_use_system_freetype2": False,
        "skia_use_system_libjpeg_turbo" : True,
        "skia_use_system_libpng" : False,
        "skia_use_system_libwebp" : False,
        "skia_use_system_zlib" : False,
        "skia_use_vulkan" : False,
        "skia_use_webgl" : False,
        "skia_use_webgpu" : False,
        "skia_use_wuffs" : True,
        "skia_use_x11" : False,
        "skia_use_xps" : True,
        "skia_use_zlib" : True
    }

    generators = "cmake"
    no_copy_source = True

    @property
    def _settings_build(self):
        return getattr(self, "settings_build", self.settings)

    def export_sources(self):
        export_conandata_patches(self)

    def config_options(self):
        if self.settings.os == "Windows" or self.settings.os != self._settings_build.os:
            # No system libraries on Windows
            # self.options.skia_use_system_expat = False
            # self.options.skia_use_system_harfbuzz = False
            self.options.skia_use_system_icu = False
            self.options.skia_use_system_libjpeg_turbo = False
            self.options.skia_use_system_libpng = False
            self.options.skia_use_system_libwebp = False
            self.options.skia_use_system_zlib = False

        if self.settings.os == "Emscripten":
            self.options.skia_use_dawn = self.options.skia_canvaskit_enable_webgpu
            self.options.skia_use_webgpu = self.options.skia_canvaskit_enable_webgpu
            self.options.skia_use_webgl = self.options.skia_canvaskit_enable_webgl
            self.options.skia_build_for_debugger = self.options.skia_canvaskit_enable_debugger
            self.options.skia_enable_skparagraph = self.options.skia_canvaskit_enable_paragraph

    def configure(self):
        pass

    def layout(self):
        basic_layout(self, src_folder="src")

    def requirements(self):
        pass

    def build_requirements(self):
        self.tool_requires("ninja/1.11.1@")

        if self.settings.os == "Android":
            self.tool_requires("android-ndk/r25c@")
        elif self.settings.os == "Emscripten":
            self.tool_requires("emsdk/3.1.31@")

    def validate(self):
        if self.settings.os == "Emscripten":
            for option in ["is_component_build", "skia_use_angle", "skia_use_fontconfig",
                           "skia_use_libheif", "skia_use_lua", "skia_use_piex", "skia_use_system_freetype2",
                           "skia_use_system_libjpeg_turbo", "skia_use_system_libpng", "skia_use_system_libwebp",
                           "skia_use_system_zlib", "skia_use_vulkan", "skia_enable_fontmgr_custom_directory",
                           "skia_enable_pdf"]:
                if self.options.get_safe(option, False) is True:
                    raise ConanInvalidConfiguration("option %s is not supported on Emscripten" % option)

            for option in ["skia_use_freetype", "skia_use_wuffs", "skia_use_zlib", "skia_enable_skshaper",
                           "skia_enable_skparagraph"]:
                if self.options.get_safe(option, True) is False:
                    raise ConanInvalidConfiguration("option %s is required on Emscripten" % option)

    def source(self):
        get(self, **self.conan_data["sources"][self.version], destination=self.source_folder, strip_root=True)

        # Fetch dependencies
        self.run('python3 tools/git-sync-deps')

        # Apply patches in source as source files are not being copied to the build folder
        apply_conandata_patches(self)

    def generate(self):
        pass

    def build(self):

        args = []
        extra_cflags = []

        for k, v in self.options.items():
            if k == "skia_fontmgr_factory":
                if v != "None":
                    args.append("%s=\\\"%s\\\"" % (k, v))
            else:
                args.append(("%s=%s" % (k, v)).lower())

        if self.settings.build_type == "Debug":
            args.append("is_debug=true")

        if self.settings.os == "Windows":
            if str(self._settings_build.compiler.runtime).startswith("MD"):
                if self._settings_build.build_type == "Debug":
                    extra_cflags.append("/MDd")
                else:
                    extra_cflags.append("/MD")
            else:
                if self._settings_build.build_type == "Debug":
                    extra_cflags.append("/MTd")
                else:
                    extra_cflags.append("/MT")
        elif self.settings.os == "Android":
            args.extend([
                "ndk=%s" % "\\\"%s\\\"" % self.env["ANDROID_NDK_HOME"],
                "ndk_api=%s" % self.settings.os.api_level,
            ])
        elif self.settings.os == "Emscripten":
            args.extend([
                "skia_emsdk_dir=\\\"%s\\\"" % self.env["EMSDK"],
                "target_cpu=\\\"wasm\\\""
                # target_ar, target_cc, target_cxx and target_link are automatically set up by
                # Skia's build system when using emscripten
            ])

        if str(self.settings.arch).startswith("arm"):
            if (self.settings.arch == "armv8"):
                args.append("target_cpu=\\\"arm64\\\"")
            elif (self.settings.arch == "armv8_32"):
                args.append("target_cpu=\\\"arm\\\"")
            else:
                raise ConanException("Unsupported ARM architecture: %s" % self.settings.arch)

        if extra_cflags:
            args.append("extra_cflags=[\\\"%s\\\"]" % "\\\",\\\"".join(extra_cflags))

        cmd = "bin%sgn gen %s --args=\"%s\"" % (os.sep, self.build_folder, " ".join(args))

        self.run(cmd, cwd=self.source_folder)
        if self.options.skia_canvaskit_enable_canvas_bindings:
            self.run('ninja canvaskit.js', cwd=self.build_folder)
        else:
            self.run('ninja', cwd=self.build_folder)

    def package(self):
        # copy headers
        self.copy("*.h", dst="include/skia", src=self.source_folder, keep_path=True)
        # copy binaries
        self.copy("*.dll", dst="bin", src=self.build_folder, keep_path=False)
        self.copy("*.lib", dst="lib", src=self.build_folder, keep_path=False)
        self.copy("*.so", dst="lib", src=self.build_folder, keep_path=False)
        self.copy("*.dylib", dst="lib", src=self.build_folder, keep_path=False)
        self.copy("*.a", dst="lib", src=self.build_folder, keep_path=False)

    def package_info(self):
        self.cpp_info.libs = collect_libs(self)
        self.cpp_info.includedirs = ["include", "include/skia"]
