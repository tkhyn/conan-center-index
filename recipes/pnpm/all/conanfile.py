"""
pnpm recipe
"""

import os, stat

from conan import ConanFile
from conan.tools.layout import basic_layout
from conan.errors import ConanInvalidConfiguration
from conan.tools.files import download

required_conan_version = ">=1.59.0"


class PnpmConan(ConanFile):
    name = "pnpm"
    description = "pnpm binary for use as build tools"
    topics = ("pnpm", "javascript", "runtime")
    url = "https://github.com/conan-io/conan-center-index"
    homepage = "https://pnpm.io/"
    license = "MIT"
    settings = "os", "arch"
    no_copy_source = True

    @property
    def _nodejs_arch(self):
        if str(self.settings.os) == "Linux":
            if str(self.settings.arch).startswith("armv7"):
                return "armv7"
            if str(self.settings.arch).startswith("armv8") and "32" not in str(self.settings.arch):
                return "armv8"
        return str(self.settings.arch)

    def layout(self):
        basic_layout(self)

    def validate(self):
        if (not (self.version in self.conan_data["sources"]) or
            not (str(self.settings.os) in self.conan_data["sources"][self.version]) or
            not (self._nodejs_arch in self.conan_data["sources"][self.version][str(self.settings.os)] )
        ):
            raise ConanInvalidConfiguration("Binaries for this combination of architecture/version/os not available")

    def build(self):
        download(self, **self.conan_data["sources"][self.version][str(self.settings.os)][self._nodejs_arch],
            filename=self.name + (".exe" if self.settings.os == "Windows" else ""))
        if os.name == "posix":
            os.chmod(self.name, os.stat(self.name).st_mode | stat.S_IEXEC)

    def package(self):
        # Linux
        self.copy(pattern="*", dst="bin")
        # Windows
        self.copy(pattern="*.*", dst="bin")

    def package_info(self):
        self.cpp_info.includedirs = []
        self.env_info.PATH.append(os.path.join(self.package_folder, "bin"))
