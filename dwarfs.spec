%global debug_package %{nil}
Name:           dwarfs
Version:        0.10.2
Release:        0%{?dist}
Summary:        A fast high compression read-only file system

BuildRequires: sed
ExcludeArch: s390x

%define so_ver %(echo %{version} | sed 's/\\./_/g;')

License:        GPL-3.0
URL:            https://github.com/mhx/%{name}
Source0:        https://github.com/mhx/%{name}/releases/download/v%{version}/dwarfs-%{version}.tar.xz

%define libboost() ( boost-devel or libboost_%{1}-devel )

BuildRequires: gcc
BuildRequires: gcc-c++
BuildRequires: clang
BuildRequires: git
BuildRequires: ccache
BuildRequires: (ninja or ninja-build)
BuildRequires: cmake
BuildRequires: make
BuildRequires: bison
BuildRequires: flex
BuildRequires: parallel-hashmap-devel
#BuildRequires: ruby3.2-rubygem-ronn
BuildRequires: fuse3
BuildRequires: pkg-config
BuildRequires: binutils-devel
BuildRequires: pkgconfig(libarchive)
BuildRequires: cmake(benchmark)
BuildRequires: boost-devel
BuildRequires: %{libboost chrono}
BuildRequires: %{libboost context}
BuildRequires: %{libboost filesystem}
#BuildRequires: %{libboost process}
BuildRequires: %{libboost iostreams}
BuildRequires: %{libboost program_options}
BuildRequires: %{libboost python3}
BuildRequires: %{libboost regex}
BuildRequires: %{libboost system}
BuildRequires: %{libboost thread}
BuildRequires: pkgconfig(libbrotlicommon)
BuildRequires: pkgconfig(libevent)
BuildRequires: pkgconfig(jemalloc)
BuildRequires: cmake(double-conversion)
BuildRequires: (cmake(lz4) or pkgconfig(liblz4))
#BuildRequires: lzlib-devel
BuildRequires: pkgconfig(liblzma)
BuildRequires: pkgconfig(libmagic)
BuildRequires: pkgconfig(openssl)
BuildRequires: pkgconfig(libunwind)
BuildRequires: pkgconfig(libdwarf)
BuildRequires: pkgconfig(libelf)
BuildRequires: cmake(fmt)
BuildRequires: pkgconfig(fuse3)
BuildRequires: cmake(nlohmann_json)
BuildRequires: cmake(utf8cpp)
BuildRequires: cmake(range-v3)
BuildRequires: pkgconfig(libxxhash)
BuildRequires: cmake(date)
BuildRequires: gtest
BuildRequires: gmock
BuildRequires: thrift
BuildRequires: folly-devel
BuildRequires: glog-devel
BuildRequires: glog
BuildRequires: pkgconfig(thrift)

%description
DwarFS is a read-only file system with a focus on achieving very high compression ratios in particular for very redundant data.

%{?!_cmakedir:%define _cmakedir %{_libdir}/cmake}

%package -n libdwarfs%{?suse_version:so_ver}
Summary: DwarFS dynamic library

%description -n libdwarfs%{?suse_version:so_ver}
%{summary}.

%package -n libdwarfs-doc
BuildArch: noarch
Summary: DwarFS documentations

%description -n libdwarfs-doc
%{summary}.

%package -n libdwarfs-devel
Summary: DwarFS development files
Requires: libdwarfs%{?suse_version:so_ver} = %{version}

%description -n libdwarfs-devel
%{summary}.

%files -n libdwarfs%{?suse_version:so_ver}
%{_libdir}/*.so.*

%{?!run_ldconfig:%define run_ldconfig %{_sbindir}/ldconfig}

%post -n libdwarfs%{?suse_version:so_ver}
%run_ldconfig

%postun -n libdwarfs%{?suse_version:so_ver}
%run_ldconfig

%files -n libdwarfs-doc
%{_mandir}/*/*
%doc README.md

%files -n libdwarfs-devel
%{_includedir}/dwarfs/*.h
%{_includedir}/dwarfs/*/*.h
%{_cmakedir}/dwarfs/*.cmake
%{_libdir}/*.so
%dir %{_includedir}/dwarfs
%dir %{_includedir}/dwarfs/reader
%dir %{_includedir}/dwarfs/utility
%dir %{_includedir}/dwarfs/writer
%dir %{_cmakedir}/dwarfs

%prep
%setup -q
#rm -Rfv folly ||:
#rm -Rfv fbthrift ||:

%build
%cmake -DWITH_TESTS=OFF -DPREFER_SYSTEM_GTEST=OFF -DPREFER_SYSTEM_FMT=ON -DCMAKE_EXE_LINKER_FLAGS="-lboost_system -lboost_filesystem" 
# -lboost_process"
%cmake_build

%check
#ctest

%install
%cmake_install
mkdir -pv %{buildroot}/%{_bindir}
mv %{buildroot}/%{_usr}/sbin/%{name} %{buildroot}/%{_bindir}/%{name}
rm -rf %{buildroot}/%{_sbindir}
find %{buildroot} -type f -executable -exec strip --strip-all '{}' +

%files
%license LICENSE
%{_bindir}/*%{name}*


%changelog
- fmt is included in the source directory instead of being cloned from github
- added the missing dependencies
- reduced redundancy and project size
