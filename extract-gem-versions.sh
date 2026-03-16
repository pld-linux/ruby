#!/bin/sh
# Extract gem versions from unpacked Ruby source for use in ruby.spec.
# Run from the package directory (where ruby.spec lives).
# Requires: builder -bp ruby to have been run first (or will run it).

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

BUILD_DIR="$(rpm --eval '%{_builddir}')/ruby-${ruby_version}.${patchlevel}-build/ruby-${ruby_version}.${patchlevel}"
if [ ! -d "$BUILD_DIR" ]; then
    # try without -build suffix (older rpm-build-macros)
    BUILD_DIR="$(rpm --eval '%{_builddir}')/ruby-${ruby_version}.${patchlevel}"
fi
[ ! -d "$BUILD_DIR" ] && builder -bp ruby

SPEC_DIR=$(pwd)
cd $BUILD_DIR || exit 1

echo "# Default gems (from ext/ and lib/)" >> $DEST

ver=$(grep "VERSION = " lib/bundler/version.rb | grep -oP '\d+\.\d+[\d\.]*')
puts_version "bundler" $ver

ver=$(grep "VERSION = " lib/erb/version.rb | grep -oP '\d+\.\d+[\d\.]*')
puts_version "erb" $ver

ver=$(grep 'IO_CONSOLE_VERSION' ext/io/console/console.c | grep -oP '\d+\.\d+[\d\.]*')
puts_version "io_console" $ver

ver=$(grep "VERSION = " ext/json/lib/json/version.rb | grep -oP '\d+\.\d+[\d\.]*')
puts_version "json" $ver

for i in stringio zlib; do
    iup=$(echo $i | tr '[a-z]' '[A-Z]')
    ver=$(grep "${iup}_VERSION" ext/$i/$i.c | grep -oP '\d+\.\d+[\d\.]*')
    puts_version $i $ver
done

ver=$(grep -oP 'spec\.version\s*=\s*"\K[^"]+' ext/openssl/openssl.gemspec 2>/dev/null)
puts_version "openssl" $ver

ver=$(grep "VERSION = " ext/psych/lib/psych/versions.rb | head -1 | grep -oP '\d+\.\d+[\d\.]*')
puts_version "psych" $ver

ver=$(grep "VERSION = " lib/rubygems.rb | head -1 | grep -oP '\d+\.\d+[\d\.]*')
puts_version "rubygems" $ver

ver=$(grep -oP 'VERSION\s*=\s*."\K[^"]+' lib/did_you_mean/version.rb 2>/dev/null)
puts_version "did_you_mean" $ver

echo "" >> $DEST
echo "# Bundled gems (from .bundle/gems/)" >> $DEST
find .bundle/gems/ -maxdepth 1 -type d | grep -P '\w\-\d+' | sort | perl -pe  's|\.bundle/gems/(\w.+)\-(\d+\.\d+\.\d+)|%define ${1}_ver\t$2|g; s|\-|_|g' >> $DEST

echo "" >> $DEST
echo "# Bundler vendored sub-versions" >> $DEST
ver=$(grep 'VERSION = ' lib/bundler/vendor/connection_pool/lib/connection_pool/version.rb 2>/dev/null | grep -oP '\d+\.\d+[\d\.]*')
puts_version "bundler_connection_pool" $ver
ver=$(grep 'VERSION = ' lib/bundler/vendor/fileutils/lib/fileutils.rb 2>/dev/null | grep -oP '\d+\.\d+[\d\.]*')
puts_version "bundler_fileutils" $ver
ver=$(grep 'VERSION = ' lib/bundler/vendor/pub_grub/lib/pub_grub/version.rb 2>/dev/null | grep -oP '\d+\.\d+[\d\.]*')
puts_version "bundler_pub_grub" $ver
ver=$(grep 'VERSION = ' lib/bundler/vendor/net-http-persistent/lib/net/http/persistent.rb 2>/dev/null | grep -oP '\d+\.\d+[\d\.]*')
puts_version "bundler_net_http_persistent" $ver
ver=$(grep 'VERSION = ' lib/bundler/vendor/thor/lib/thor/version.rb 2>/dev/null | grep -oP '\d+\.\d+[\d\.]*')
puts_version "bundler_thor" $ver
ver=$(grep 'VERSION = ' lib/bundler/vendor/tsort/lib/tsort.rb 2>/dev/null | grep -oP '\d+\.\d+[\d\.]*')
puts_version "bundler_tsort" $ver
ver=$(grep 'VERSION = ' lib/bundler/vendor/uri/lib/uri/version.rb 2>/dev/null | grep -oP '\d+\.\d+[\d\.]*')
puts_version "bundler_uri" $ver

echo ""
echo "Determined gem versions:"
cat $DEST

cd $SPEC_DIR || exit 1

echo ""
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
