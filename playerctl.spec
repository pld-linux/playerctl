#
# Conditional build:
%bcond_without	apidocs		# API documentation
%bcond_without	static_libs	# don't build static libs

Summary:	MPRIS media player command-line controller
Name:		playerctl
Version:	2.4.1
Release:	1
License:	LGPL v3
Group:		Applications
Source0:	https://github.com/altdesktop/playerctl/archive/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	795c7f66fb865aa87a301b11f2a78940
URL:		https://github.com/altdesktop/playerctl
BuildRequires:	bash-completion-devel
BuildRequires:	glib2-devel >= 1:2.38
BuildRequires:	gobject-introspection-devel >= 1.0
%{?with_apidocs:BuildRequires:	gtk-doc}
BuildRequires:	meson >= 0.56.0
BuildRequires:	ninja
BuildRequires:	pkgconfig
BuildRequires:	rpm-build >= 4.6
BuildRequires:	rpmbuild(macros) >= 1.736
Requires:	%{name}-libs = %{version}-%{release}
Requires:	glib2 >= 1:2.38
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Playerctl is a command-line utility and library for controlling media
players that implement the MPRIS D-Bus Interface Specification.
Playerctl makes it easy to bind player actions, such as play and
pause, to media keys. You can also get metadata about the playing
track such as the artist and title for integration into statusline
generators or other command-line tools.

Playerctl also comes with a daemon that allows it to act on the
currently active media player called playerctld.

%package libs
Summary:	playerctl libraries
Group:		Libraries

%description libs
playerctl libraries.

%package devel
Summary:	Header files for playerctl
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}

%description devel
Header files for playerctl.

%package static
Summary:	playerctl static libraries
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
playerctl static libraries.

%package apidocs
Summary:	playerctl API documentation
Group:		Documentation
Requires:	%{name}-devel = %{version}-%{release}
BuildArch:	noarch

%description apidocs
playerctl API documentation.

%prep
%setup -q

%build
%meson build \
	%{!?with_static_libs:--default-library=shared} \
	-Dgtk-doc=%{__true_false apidocs}

%ninja_build -C build

%install
rm -rf $RPM_BUILD_ROOT

%ninja_install -C build

%clean
rm -rf $RPM_BUILD_ROOT

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc README.md
%attr(755,root,root) %{_bindir}/playerctl
%attr(755,root,root) %{_bindir}/playerctld
%{_datadir}/dbus-1/services/org.mpris.MediaPlayer2.playerctld.service
%{_mandir}/man1/playerctl.1*

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libplayerctl.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libplayerctl.so.2
%{_libdir}/girepository-1.0/Playerctl-2.0.typelib

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libplayerctl.so
%dir %{_includedir}/playerctl
%{_includedir}/playerctl/playerctl*.h
%{_pkgconfigdir}/playerctl.pc
%{_datadir}/gir-1.0/Playerctl-2.0.gir

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libplayerctl.a
%endif

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/playerctl
%endif
