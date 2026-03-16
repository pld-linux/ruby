#!/bin/sh
# Extract gem versions used in rpm.spec

DEST=$(mktemp)
trap 'rm -rf -- "$DEST"' EXIT

puts_version() {
    local name="$1"
    local version="$2"
    [ -z "$version" ] && version="UNDETERMINED"
    echo -e "%define ${name}_ver\t${version}" >> $DEST
}

ruby_version=$(grep -P '%define\s+ruby_version' ruby.spec | grep -oP '\d\.[\d\.]+')
patchlevel=$(grep -P '%define\s+patchlevel\s+\d' ruby.spec | grep -oP '\d+')

[ -z "$ruby_version" -o -z "$patchlevel" ] && exit 1

BUILD_DIR="$(rpm --eval '%{_builddir}')/ruby-${ruby_version}.${patchlevel}"
[ ! -d $BUILD_DIR ] && builder -bp ruby

SPEC_DIR=$(pwd)
cd $BUILD_DIR || exit 1


ver=$(grep -P "\w+\.version" ext/bigdecimal/bigdecimal.gemspec | head -1 | grep -oP '\d+\.\d+[\d\.]*')
puts_version "bigdecimal" $ver

ver=$(grep "VERSION = " lib/bundler/version.rb | grep -oP '\d+\.\d+[\d\.]*')
puts_version "bundler" $ver

ver=$(grep "VERSION = " lib/erb/version.rb | grep -oP '\d+\.\d+[\d\.]*')
puts_version "erb" $ver

ver=$(grep "_VERSION = " ext/io/console/io-console.gemspec | grep -oP '\d+\.\d+[\d\.]*')
puts_version "io_console" $ver

ver=$(grep -P "\s+VERSION = " lib/irb/version.rb | grep -oP '\d+\.\d+[\d\.]*')
puts_version "irb" $ver

ver=$(cat ./ext/json/VERSION | grep -oP '\d+\.\d+[\d\.]*')
puts_version "json" $ver

for i in etc stringio zlib; do
    iup=$(echo $i | tr '[a-z]' '[A-Z]')
    ver=$(grep "${iup}_VERSION" ext/$i/$i.c | grep -oP '\d+\.\d+[\d\.]*')
    puts_version $i $ver
done

ver=$(grep -P "\w+\.version\s+" ext/openssl/openssl.gemspec | head -1 | grep -oP '\d+\.\d+[\d\.]*')
puts_version "openssl" $ver

ver=$(grep "VERSION = " ext/psych/lib/psych/versions.rb | head -1 | grep -oP '\d+\.\d+[\d\.]*')
puts_version "psych" $ver

ver=$(grep -P "\s+VERSION\s+= " lib/racc/info.rb | grep -oP '\d+\.\d+[\d\.]*')
puts_version "racc" $ver

ver=$(grep -P "\s+VERSION = " lib/rdoc/version.rb | grep -oP '\d+\.\d+[\d\.]*')
puts_version "rdoc" $ver

ver=$(grep -P "\w+\.version\s+" ext/readline/readline*.gemspec | head -1 | grep -oP '\d+\.\d+[\d\.]*')
puts_version "readline" $ver

ver=$(grep "VERSION = " lib/rubygems.rb | head -1 | grep -oP '\d+\.\d+[\d\.]*')
puts_version "rubygems" $ver

echo "# bundled" >> $DEST
find .bundle/gems/ -maxdepth 1 -type d | grep -P '\w\-\d+' | sort | perl -pe  's|\.bundle/gems/(\w.+)\-(\d+\.\d+\.\d+)|%define ${1}_ver\t$2|g; s|\-|_|g' >> $DEST

echo "Determined gem versions:"
cat $DEST

cd $SPEC_DIR || exit 1

echo "Checking version macros usage:"
# determine _ver macros usage
ec=0
for i in $(grep -P '^%define\s+\w+_ver\s+\d[\.\d]+$' ruby.spec | awk '{print $2}' | sort -u); do
    grep -q "%{$i}" ruby.spec
    if [ $? -eq 0 ]; then
        grep -qP "%define\s+${i}\s+\d" $DEST
        if [ $? -ne 0 ]; then
            echo "$i: MISSING DEFINITION"
            ec=1
        fi
    fi
done
[ "$ec" -eq 0 ] && echo " all OK"

rm -f $DEST
exit $ec
