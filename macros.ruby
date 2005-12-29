%define ruby_archdir    %(ruby -r rbconfig -e 'print Config::CONFIG["archdir"]')
%define ruby_rubylibdir %(ruby -r rbconfig -e 'print Config::CONFIG["rubylibdir"]')
%define ruby_ridir	%(ruby -r rbconfig -e 'include Config; print File.join(CONFIG["datadir"], "ri", CONFIG["ruby_version"], "system")')
%define ruby_version	%(ruby -r rbconfig -e 'print Config::CONFIG["ruby_version"]')
%define rdoc	rdoc --inline-source --op rdoc --title '%{name}-%{version}'
%define build_ri 		rdoc --ri --op ri
%define ruby_ver_requires_eq   Requires:   ruby(ver) = %{ruby_ver}
%define ruby_mod_ver_requires_eq   Requires:   ruby-modules(ver) = %{ruby_ver}
