import os
from shutil import copytree

from conan import ConanFile
from conan.tools.files import get
from conan.tools.layout import basic_layout
from conan.errors import ConanInvalidConfiguration

required_conan_version = ">=1.59.0"


class NodejsConan(ConanFile):
    name = "nodejs"
    description = "nodejs binaries for use in recipes"
    topics = ("conan", "node", "nodejs")
    url = "https://github.com/conan-io/conan-center-index"
    homepage = "https://nodejs.org"
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
            not (self._nodejs_arch in self.conan_data["sources"][self.version][str(self.settings.os)] ) ):
            raise ConanInvalidConfiguration("Binaries for this combination of architecture/version/os not available")

    def build(self):
        get(self, **self.conan_data["sources"][self.version][str(self.settings.os)][self._nodejs_arch], strip_root=True)

    def package(self):
        self.copy(pattern="LICENSE", dst="licenses")

        if self.settings.os == "Windows":
            # Windows
            self.copy(pattern="node.exe", dst="bin")
            self.copy(pattern="np*.cmd", dst="bin")

            # node_modules folder is required for npm and npx
            copytree(
                os.path.join(self.build_folder, "node_modules"),
                os.path.join(self.package_folder, "bin", "node_modules"),
                dirs_exist_ok=True
            )
        else:
            # Linux. Copies node, npm, npx but not corepack
            self.copy(pattern="n*", src="bin", dst="bin", symlinks=True)

            # node_modules folder is required for npm and npx which have symlinks to it
            copytree(
                os.path.join(self.build_folder, "lib"),
                os.path.join(self.package_folder, "lib"),
                symlinks=True, dirs_exist_ok=True
            )

    def package_info(self):
        self.cpp_info.includedirs = []
        bin_dir = os.path.join(self.package_folder, "bin")
        self.output.info('Appending PATH environment variable: {}'.format(bin_dir))
        self.env_info.PATH.append(bin_dir)
