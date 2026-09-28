#!/bin/sh
# Extract gem versions from Ruby source tree and compare/update ruby.spec.

UPDATE=0
if [ "$1" = "--update" ]; then
    UPDATE=1
    shift
elif [ "$1" = "--help" ] || [ "$1" = "-h" ]; then
    echo "Usage: $0 [--update]"
    echo
    echo "Without options: report gem versions that differ between the Ruby"
    echo "source tree and ruby.spec."
    echo
    echo "With --update:   patch ruby.spec to match versions found in the tree."
    exit 0
fi

DEST=$(mktemp)
trap 'rm -rf -- "$DEST"' EXIT

puts_version() {
    local name="$1"
    local version="$2"
    [ -z "$version" ] && version="UNDETERMINED"
    echo -e "%define ${name}_version\t${version}" >> "$DEST"
}

ruby_version=$(grep -P '%define\s+ruby_version' ruby.spec | grep -oP '\d\.[\d\.]+')
patchlevel=$(grep -P '%define\s+patchlevel\s+\d' ruby.spec | grep -oP '\d+')

[ -z "$ruby_version" -o -z "$patchlevel" ] && exit 1

BUILD_DIR="$(rpm --eval '%{_builddir}')/ruby-${ruby_version}.${patchlevel}-build/ruby-${ruby_version}.${patchlevel}"
#echo "BUILD_DIR ${BUILD_DIR}"
if [ ! -d "$BUILD_DIR" ]; then
    if command -v builder >/dev/null 2>&1; then
        builder -bp ruby
    else
        rpmbuild -bp ruby.spec
    fi
fi
if [ ! -d "$BUILD_DIR" ]; then
    echo "ERROR: BUILD_DIR does not exist and could not be prepared." >&2
    exit 1
fi

SPEC_DIR=$(pwd)
cd "$BUILD_DIR" || exit 1

ver=$(grep -P "\w+\.version" .bundle/gems/bigdecimal-*/.bundled.bigdecimal-*.gemspec | head -1 | grep -oP '\d+\.\d+[\d\.]*')
puts_version "bigdecimal" "$ver"

ver=$(grep -oP 'VERSION\s*=\s*["\x27]\K[\d.]+' lib/bundler/version.rb | head -1)
puts_version "bundler" "$ver"

ver=$(grep -oP 'VERSION\s*=\s*["\x27]\K[\d.]+' lib/erb/version.rb | head -1)
puts_version "erb" "$ver"

ver=$(grep IO_CONSOLE_VERSION ext/io/console/console.c | grep -oP '\d+\.\d+[\d\.]*')
puts_version "io_console" "$ver"

ver=$(grep -oP 'VERSION\s*=\s*["\x27]\K[\d.]+' .bundle/gems/irb-*/lib/irb/version.rb | head -1)
puts_version "irb" "$ver"

ver=$(grep -oP 'VERSION\s*=\s*["\x27]\K[\d.]+' ext/json/lib/json/version.rb | head -1)
puts_version "json" "$ver"

for i in etc stringio zlib; do
    iup=$(echo "$i" | tr 'a-z' 'A-Z')
    ver=$(grep "${iup}_VERSION" "ext/$i/$i.c" | grep -oP '\d+\.\d+[\d\.]*')
    puts_version "$i" "$ver"
done

ver=$(grep -P "\w+\.version\s+" ext/openssl/openssl.gemspec | head -1 | grep -oP '\d+\.\d+[\d\.]*')
puts_version "openssl" "$ver"

ver=$(grep "VERSION = " ext/psych/lib/psych/versions.rb | head -1 | grep -oP '\d+\.\d+[\d\.]*')
puts_version "psych" "$ver"

ver=$(grep -oP 'VERSION\s*=\s*["\x27]\K[\d.]+' .bundle/gems/rdoc-*/lib/rdoc/version.rb | head -1)
puts_version "rdoc" "$ver"

ver=$(grep -oP 's\.version\s*=\s*["\x27]\K[\d.]+' .bundle/specifications/readline-*.gemspec | head -1)
puts_version "readline" "$ver"

ver=$(grep "VERSION = " lib/rubygems.rb | head -1 | grep -oP '\d+\.\d+[\d\.]*')
puts_version "rubygems" "$ver"

ver=$(grep -P "\s+VERSION\s+=\s+" lib/syntax_suggest/version.rb | grep -oP '\d+\.\d+[\d\.]*')
puts_version "syntax_suggest" "$ver"

# bundled gems from .bundle/gems/
find .bundle/gems/ -maxdepth 1 -type d | grep -P '\w\-\d+' | sort | \
    perl -pe 's|\.bundle/gems/(\w.+)\-(\d+\.\d+\.\d+)|%define ${1}_version\t$2|g; s|\-|_|g' >> "$DEST"

cd "$SPEC_DIR" || exit 1

echo
echo "Determined gem versions:"
cat "$DEST"
echo

ec=0
if [ "$UPDATE" -eq 1 ]; then
    echo "Updating ruby.spec..."
    while IFS=$'\t' read -r macro version; do
        name=${macro#%define }
        name=${name%_version}
        if grep -qP "^%define\s+${name}_version\s+" ruby.spec; then
            old=$(grep -P "^%define\s+${name}_version\s+" ruby.spec | awk '{print $3}')
            if [ "$old" != "$version" ]; then
                echo "  $name: $old -> $version"
                perl -pi -e "s/^(%define\\s+${name}_version\\s+).*/\${1}${version}/" ruby.spec
            fi
        #else
            #echo "  $name: not present in ruby.spec (skipped)"
        fi
    done < "$DEST"
    echo "Done."
else
    echo "Version differences (source tree vs ruby.spec):"
    while IFS=$'\t' read -r macro version; do
        name=${macro#%define }
        name=${name%_version}
        if grep -qP "^%define\s+${name}_version\s+" ruby.spec; then
            old=$(grep -P "^%define\s+${name}_version\s+" ruby.spec | awk '{print $3}')
            if [ "$old" != "$version" ]; then
                echo "  $name: ruby.spec=$old, tree=$version"
                ec=1
            fi
        fi
    done < "$DEST"
    [ "$ec" -eq 0 ] && echo "  all match"
fi

exit "$ec"
