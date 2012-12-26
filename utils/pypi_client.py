#!/usr/bin/env python

import xmlrpclib
import os.path
import pprint
import sys

pp = pprint.PrettyPrinter()
download = True
filter_serie = '2.6'
verbose = True

exclude_packages = [
    'tryton',
    'neso',
    'proteus',
    ]
known_authors = [
    'b2ck',
    'zikzakmedia',
    'openlabs',
    'nfg',
    ]

def get_tryton_packages_from_pypi(serie):
    # http://wiki.python.org/moin/PyPiXmlRpc
    client = xmlrpclib.ServerProxy('http://pypi.python.org/pypi')

    all_tryton_packages = client.browse(["Framework :: Tryton"])
    major_versions = list(set(".".join(p[1].split('.')[0:2]) for p in all_tryton_packages))
    major_versions.sort()

    if verbose:
        print "[INFO] All Tryton Packages: (%d)" % len(all_tryton_packages)
    packages_by_serie = {}
    for p_name, p_version in all_tryton_packages:
        if p_name in exclude_packages:
            continue
        serie = ".".join(p_version.split('.')[0:2])
        package_in_serie = packages_by_serie.setdefault(serie, {})

        release_info = client.release_data(p_name, p_version)
        download_url = release_info['download_url']
        author = release_info['author']
        author_slug = get_author_slug_from_package_info(p_name, p_version,
                author, download_url)
        if not author_slug:
            continue
        package_author = package_in_serie.setdefault(author_slug, [])
        package_author.append((p_name, p_version, author, download_url,
                author_slug))
    with open('packages.txt', 'w') as packages_file:
        packages_file.write(str(packages_by_serie))
    if serie:
        return packages_by_serie[serie]
    return packages_by_serie

def get_author_slug_from_package_info(name, version, author, download_url):
    download_url_parts = download_url.split('/')
    prefix = name.split('_')[0]
    if ('downloads.tryton.org' in download_url_parts and
            prefix == 'trytond'):
        return 'core'
    elif 'downloads.tryton.org' in download_url_parts:
        print >> sys.stderr, "[WARN] Packages %s of %s in version %s seems " \
                "to have an invalid Download URL: %s" % (name, author, version,
                        download_url)
    if 'ftp.gnu.org' in download_url_parts and 'health' in download_url_parts:
        return 'gnuhealth'
    if 'downloads.openlabs.co.in' in download_url_parts:
        return 'openlabs'
    if 'bitbucket.org' in download_url_parts:
        return download_url_parts[3]
    if author == 'Virtual Things':
        return 'virtual_things'
    author_slug = author.split(' ')[0].lower()
    if author_slug in known_authors:
        return author_slug
    print >> sys.stderr, "[ERROR] Unknown combination of prefix '%s' and " \
            "download URL '%s' for package %s (%s, %s)" % (prefix,
                    download_url, name, author, version)
    return False

def get_tryton_packages_from_file():
    if not os.path.exists('packages.txt'):
        print >> sys.stderr, "[ERROR] packages.txt file doesn't exists!"
        sys.exit(1)
    packages_file = open('packages.txt', 'r')
    packages_txt = packages_file.read()
    packages_file.close()
    packages_dict = eval(packages_txt)
    for key in exclude_packages:
        if key in packages_dict:
            del packages_dict[key]
    return packages_dict

def get_mr_developer_line_from_package_info(name, version, author,
        download_url):
    download_url_parts = download_url.split('/')
    if 'bitbucket.org' in download_url_parts:
        return "%s = hg %s" % (name, download_url)
    elif 'hg.tryton.org' in download_url_parts:
        if download_url.endswith(name):
            return "%s = hg %s" % (name, download_url)
        else:
            return "%s = hg %smodules/%s" % (name, download_url, name)
    elif 'downloads.tryton.org' in download_url.split('/'):
        vcs_url = 'http://hg.tryton.org/%s/modules/%s' % (
                ".".join(version.split('.')[0:2]), name)
        print >> sys.stderr, "[WARN] Download URL (%s) of package %s of %s " \
                "in version %s is not a VCS. We assume it is '%s'" \
                % (download_url, name, author, version, vcs_url)
        return 'hg ' + vcs_url
    print >> sys.stderr, "[ERROR] The package %s in version %s has an " \
            "unknown download URL: %s" % (name, version, download_url)
    return False

def print_packages_by_serie(packages_by_serie):
    for serie in packages_by_serie:
        print serie
        print "==="
        print_packages_by_prefix(packages_by_serie[serie])
        print ""
    return

def print_packages_by_prefix(package_in_serie):
    for prefix in package_in_serie:
        print "- %s:" % prefix
        lines = []
        for p_info in packages[prefix]:
            line = get_mr_developer_line_from_package_info(p_info[0],
                    p_info[1], p_info[2], p_info[3])
            if line:
                lines.append(line)
        lines.sort()
        for line in lines:
            print line
    return

if download:
    packages = get_tryton_packages_from_pypi(filter_serie)
else:
    packages = get_tryton_packages_from_file()

if filter_serie:
    print "[INFO] Packages of serie %s" % filter_serie
    print_packages_by_prefix(packages)
else:
    print "[INFO] All packages:"
    print_packages_by_serie(packages)

#print "Show all data of a module:"
#pp.pprint(client.release_data('trytond_party', '2.6.0'))

