Summary:	Tools for working with the PinePhone hardware
Name:		pinephone-tools
Version:	1.0
Release:	0.20200905.2
Url:		https://xnux.eu/devices/feature/audio-pp.html
# Tools to drive PinePhone hardware...
# Audio routing
Source0:	https://xnux.eu/devices/feature/call-audio.c
# Modem
# See https://xnux.eu/devices/feature/modem-pp.html#toc-modem-power-driver
# for documentation on the driver
Source1:	modem
# Unlock adb access to the modem
Source2:	https://xnux.eu/devices/feature/qadbkey-unlock.c
# Systemd integration for the modem...
Source3:	modem.service
Source4:	modem-wait-powered.service
# ALSA configurations
Source10:	https://raw.githubusercontent.com/dreemurrs-embedded/Pine64-Arch/master/PKGBUILDS/pine64/alsa-ucm-pinephone/HiFi.conf
Source11:	https://raw.githubusercontent.com/dreemurrs-embedded/Pine64-Arch/master/PKGBUILDS/pine64/alsa-ucm-pinephone/PinePhone.conf
Source12:	https://raw.githubusercontent.com/dreemurrs-embedded/Pine64-Arch/master/PKGBUILDS/pine64/alsa-ucm-pinephone/VoiceCall.conf
Source13:	99-dmix.conf
# NetworkManager configuration
Source20:	MobileData.nmconnection
ExclusiveArch:	aarch64
BuildRequires:	pkgconfig(alsa)
BuildRequires:	pkgconfig(libxcrypt)
License:	GPLv3+

%description
Tool to set up audio routing on the PinePhone

%prep

%build
%{__cc} %{optflags} -o pinephone-audio-setup %{S:0}
%{__cc} %{optflags} -o modem-adb-access %{S:2} -lcrypt

%install
mkdir -p %{buildroot}%{_bindir}
cp -a pinephone-audio-setup modem-adb-access %{S:1} %{buildroot}%{_bindir}/

mkdir -p %{buildroot}%{_datadir}/alsa/ucm2/PinePhone/
cp %{S:10} %{S:11} %{S:12} %{buildroot}%{_datadir}/alsa/ucm2/PinePhone/
mkdir -p %{buildroot}%{_sysconfdir}/alsa/conf.d/
cp %{S:13} %{buildroot}%{_sysconfdir}/alsa/conf.d/

mkdir -p %{buildroot}/lib/systemd/system
cp %{S:3} %{S:4} %{buildroot}/lib/systemd/system/

mkdir -p %{buildroot}%{_sysconfdir}/NetworkManager/system-connections
cp %{S:20} %{buildroot}%{_sysconfdir}/NetworkManager/system-connections/

chmod +x %{buildroot}%{_bindir}/*

%files
%{_bindir}/pinephone-audio-setup
%{_bindir}/modem
%{_bindir}/modem-adb-access
%{_datadir}/alsa/ucm2/PinePhone
/lib/systemd/system/modem.service
/lib/systemd/system/modem-wait-powered.service
%config %{_sysconfdir}/alsa/conf.d/99-dmix.conf
%config(noreplace) %{_sysconfdir}/NetworkManager/system-connections/MobileData.nmconnection
