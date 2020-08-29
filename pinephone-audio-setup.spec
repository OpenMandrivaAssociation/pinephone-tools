Summary:	Tool to set up audio routing on the PinePhone
Name:		pinephone-audio-setup
Version:	1.0
Release:	0.20200829.1
Url:		https://xnux.eu/devices/feature/audio-pp.html
Source0:	https://xnux.eu/devices/feature/call-audio.c
#ExclusiveArch:	aarch64
BuildRequires:	pkgconfig(alsa)
License:	GPLv3+

%description
Tool to set up audio routing on the PinePhone

%prep

%build
%{__cc} %{optflags} -o pinephone-audio-setup %{S:0}

%install
mkdir -p %{buildroot}%{_bindir}
cp pinephone-audio-setup %{buildroot}%{_bindir}/

%files
%{_bindir}/pinephone-audio-setup
