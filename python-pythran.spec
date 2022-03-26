# TODO: finish docs
#
# Conditional build:
%bcond_with	doc	# Sphinx documentation
%bcond_with	tests	# unit tests (missing in sdist)
%bcond_without	python2 # CPython 2.x module
%bcond_without	python3 # CPython 3.x module

Summary:	Ahead of Time compiler for numeric kernels
Summary(pl.UTF-8):	Kompilator z wyprzedzeniem dla jąder numerycznych
Name:		python-pythran
# keep 0.9.5 here for python 2 support
Version:	0.9.5
Release:	1
License:	BSD
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/pythran/
Source0:	https://files.pythonhosted.org/packages/source/p/pythran/pythran-%{version}.tar.gz
# Source0-md5:	da6cbfd2d5b278e41f359db347f6620b
URL:		https://pypi.org/project/pythran/
%if %{with python2}
BuildRequires:	python-modules >= 1:2.7
BuildRequires:	python-pytest-runner
BuildRequires:	python-setuptools >= 1:12.0.5
%if %{with tests}
BuildRequires:	python-beniget >= 0.2.0
BuildRequires:	python-decorator
BuildRequires:	python-gast >= 0.3.0
BuildRequires:	python-networkx >= 2
BuildRequires:	python-numpy
BuildRequires:	python-ply >= 3.4
BuildRequires:	python-six
%endif
%endif
%if %{with python3}
BuildRequires:	python3-modules >= 1:3.2
BuildRequires:	python3-pytest-runner
BuildRequires:	python3-setuptools >= 1:12.0.5
%if %{with tests}
BuildRequires:	python3-beniget >= 0.2.0
BuildRequires:	python3-decorator
BuildRequires:	python3-gast >= 0.3.0
BuildRequires:	python3-networkx >= 2
BuildRequires:	python3-numpy
BuildRequires:	python3-ply >= 3.4
BuildRequires:	python3-six
%endif
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
Requires:	python-modules >= 1:2.7
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

%package -n python3-pythran
Summary:	Ahead of Time compiler for numeric kernels
Summary(pl.UTF-8):	Kompilator z wyprzedzeniem dla jąder numerycznych
Group:		Libraries/Python
Requires:	python3-modules >= 1:3.2

%description -n python3-pythran
Pythran is an ahead of time compiler for a subset of the Python
language, with a focus on scientific computing. It takes a Python
module annotated with a few interface description and turns it into a
native Python module with the same interface, but (hopefully) faster.

%description -n python3-pythran -l pl.UTF-8
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
%if %{with python2}
%py_build %{?with_tests:test}
%endif

%if %{with python3}
%py3_build %{?with_tests:test}
%endif

%if %{with doc}
%{__make} -C docs html \
	SPHINXBUILD=sphinx-build-3
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%py_install

%{__mv} $RPM_BUILD_ROOT%{_bindir}/pythran{,-2}
%{__mv} $RPM_BUILD_ROOT%{_bindir}/pythran-config{,-2}

%py_postclean
%endif

%if %{with python3}
%py3_install

%{__mv} $RPM_BUILD_ROOT%{_bindir}/pythran{,-3}
%{__mv} $RPM_BUILD_ROOT%{_bindir}/pythran-config{,-3}
ln -sf pythran-3 $RPM_BUILD_ROOT%{_bindir}/pythran
ln -sf pythran-config-3 $RPM_BUILD_ROOT%{_bindir}/pythran-config
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%files
%defattr(644,root,root,755)
%doc LICENSE README.rst
%attr(755,root,root) %{_bindir}/pythran-2
%attr(755,root,root) %{_bindir}/pythran-config-2
%{py_sitescriptdir}/omp
%{py_sitescriptdir}/pythran
%{py_sitescriptdir}/pythran-%{version}-py*.egg-info
%endif

%if %{with python3}
%files -n python3-pythran
%defattr(644,root,root,755)
%doc LICENSE README.rst
%attr(755,root,root) %{_bindir}/pythran
%attr(755,root,root) %{_bindir}/pythran-3
%attr(755,root,root) %{_bindir}/pythran-config
%attr(755,root,root) %{_bindir}/pythran-config-3
%{py3_sitescriptdir}/omp
%{py3_sitescriptdir}/pythran
%{py3_sitescriptdir}/pythran-%{version}-py*.egg-info
%endif

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/_build/html/*
%endif
