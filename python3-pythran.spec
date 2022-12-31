# TODO: finish docs
#
# Conditional build:
%bcond_with	doc	# Sphinx documentation
%bcond_with	tests	# unit tests (missing in sdist)

Summary:	Ahead of Time compiler for numeric kernels
Summary(pl.UTF-8):	Kompilator z wyprzedzeniem dla jąder numerycznych
Name:		python3-pythran
Version:	0.12.0
Release:	1
License:	BSD
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/pythran/
Source0:	https://files.pythonhosted.org/packages/source/p/pythran/pythran-%{version}.tar.gz
# Source0-md5:	d2961ece35b4b9f44a84ef31df1b21ff
URL:		https://pypi.org/project/pythran/
BuildRequires:	python3-modules >= 1:3.2
BuildRequires:	python3-pytest-runner
BuildRequires:	python3-setuptools >= 1:12.0.5
%if %{with tests}
BuildRequires:	python3-beniget >= 0.4.0
BuildRequires:	python3-beniget < 0.5
BuildRequires:	python3-gast >= 0.5.0
BuildRequires:	python3-gast < 0.6
BuildRequires:	python3-numpy
BuildRequires:	python3-ply >= 3.4
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
%if %{with doc}
BuildRequires:	python3-guzzle_sphinx_theme
BuildRequires:	python3-nbsphinx
BuildRequires:	python3-numpy
BuildRequires:	python3-scipy
BuildRequires:	sphinx-pdg-3
%endif
Requires:	python3-modules >= 1:3.2
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Pythran is an ahead of time compiler for a subset of the Python
language, with a focus on scientific computing. It takes a Python
module annotated with a few interface description and turns it into a
native Python module with the same interface, but (hopefully) faster.

%description -l pl.UTF-8
Pythran to kompilator z wyprzedzeniem dla podzbioru języka Python,
skupiający się na obliczeniach naukowych. Przyjmuje moduł Pythona z
niewielkim opisem interfejsu i zamienia go na natywny moduł Pythona o
tym samym interfejsie, ale (miejmy nadzieję) szybszy.

%package apidocs
Summary:	API documentation for Python pythran module
Summary(pl.UTF-8):	Dokumentacja API modułu Pythona pythran
Group:		Documentation

%description apidocs
API documentation for Python pythran module.

%description apidocs -l pl.UTF-8
Dokumentacja API modułu Pythona pythran.

%prep
%setup -q -n pythran-%{version}

%build
%py3_build %{?with_tests:test}

%if %{with doc}
%{__make} -C docs html \
	SPHINXBUILD=sphinx-build-3
%endif

%install
rm -rf $RPM_BUILD_ROOT

%py3_install

%{__mv} $RPM_BUILD_ROOT%{_bindir}/pythran{,-3}
%{__mv} $RPM_BUILD_ROOT%{_bindir}/pythran-config{,-3}
ln -sf pythran-3 $RPM_BUILD_ROOT%{_bindir}/pythran
ln -sf pythran-config-3 $RPM_BUILD_ROOT%{_bindir}/pythran-config

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS Changelog LICENSE README.rst
%attr(755,root,root) %{_bindir}/pythran
%attr(755,root,root) %{_bindir}/pythran-3
%attr(755,root,root) %{_bindir}/pythran-config
%attr(755,root,root) %{_bindir}/pythran-config-3
%{py3_sitescriptdir}/omp
%{py3_sitescriptdir}/pythran
%{py3_sitescriptdir}/pythran-%{version}-py*.egg-info

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/_build/html/*
%endif
