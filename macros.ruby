%ruby_archdir    %(ruby -r rbconfig -e 'print Config::CONFIG["archdir"]')
%ruby_rubylibdir %(ruby -r rbconfig -e 'print Config::CONFIG["rubylibdir"]')

%rdoc  rdoc --inline-source --op rdoc --title '%{name}-%{version}'
%ri	rdoc --ri --op ri 
