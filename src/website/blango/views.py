from datetime import date
from xml.etree import cElementTree

from django.shortcuts import get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic.simple import direct_to_template
from django.utils.translation import ugettext as _

from website.blango.spider import Spider, hostname_from_uri, is_absolute_link
from website.blango.paginator import QuerySetPaginator
from website.blango.models import *
from website.blango.forms import *

def get_template_name(name):
    return 'blango/%s/%s' % (settings.BLANGO_THEME, name)

def server_error(request):
    return direct_to_template(request, get_template_name('500.html'))

def page_not_found(request):
    return direct_to_template(request, get_template_name('404.html'))

def list_view(request, lang, tag_slug, year, month, page):
    entries = Entry.published.order_by('-pub_date')
    base_url = request.path

    if page:
        base_url = base_url[:-1 * len(page) - 1]

    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        entries = entries.filter(tags=tag)
    if year and month:
        entries = entries.filter(pub_date__year=int(year), pub_date__month=int(month))

    if lang:
        blango_lang = lang + '/'
        language = get_object_or_404(Language, iso639_1=lang)
        entries = entries.filter(language=language)
        dates = Entry.published.filter(language=language).dates('pub_date', 'month')
        tags = Tag.for_language(language)
    else:
        dates = Entry.published.all().dates('pub_date', 'month')
        tags = Tag.objects.all()

    languages = Language.objects.all()

    paginator = QuerySetPaginator(entries, 8, base_url=base_url, page_suffix='%d/')
    page = paginator.page_or_404(page or 1)

    return direct_to_template(request, get_template_name('list.html'), locals())

def entry_view(request, entry_slug):
    entry = get_object_or_404(Entry, slug=entry_slug)
    if entry.author != request.user:
        EntryHit.objects.create(entry=entry)

    dates = Entry.objects.filter(language=entry.language).dates('pub_date', 'month')
    tags = Tag.for_language(entry.language)

    if request.user.is_authenticated():
        comment_form = UserCommentForm()
    else:
        comment_form = CommentForm(request.META['REMOTE_ADDR'], entry.id)

    if request.method == 'POST' and entry.allow_comments:
        try:
            if request.user.is_authenticated():
                comment_form = UserCommentForm(request.POST)
                comment_form.save(entry, request)
            else:
                comment_form = CommentForm(request.META['REMOTE_ADDR'], entry.id, request.POST)
                comment_form.save(entry)
            return HttpResponseRedirect(entry.get_absolute_url())
        except ValueError:
            pass

    language = entry.language
    blango_lang = '%s/' % language.iso639_1
    return direct_to_template(request, get_template_name('entry.html'), locals())

def trackback_view(request, entry_id):
    title = request.POST.get('title')
    excerpt = request.POST.get('excerpt', '')
    url = request.POST.get('url')
    blog_name = request.POST.get('blog_name')

    if not url:
        return HttpResponse('''<?xml version="1.0" encoding="utf-8"?>
                <response>
                    <error>1</error>
                    <message>No URL specified</message>
                </response>''', mimetype='text/xml')
    if len(url) > 1024:
        return HttpResponse('''<?xml version="1.0" encoding="utf-8"?>
                <response>
                    <error>1</error>
                    <message>Entity Too Large</message>
                </response>''', mimetype='text/xml')

    if not is_absolute_link(url):
        return HttpResponse('''<?xml version="1.0" encoding="utf-8"?>
                <response>
                    <error>1</error>
                    <message>URL must match https?://.*</message>
                </response>''', mimetype='text/xml')
    
    entry = get_object_or_404(Entry, pk=entry_id)

    if not entry.allow_comments:
        return HttpResponse('''<?xml version="1.0" encoding="utf-8"?>
                <response>
                    <error>1</error>
                    <message>Trackbacks are not allowed for this entry</message>
                </response>''', mimetype='text/xml')


    try:
        Comment.objects.get(entry=entry, type__in=['T', 'P'], author_uri=url)
        return HttpResponse('''<?xml version="1.0" encoding="utf-8"?>
                <response>
                    <error>1</error>
                    <message>Trackback already registered</message>
                </response>''', mimetype='text/xml')
    except Comment.DoesNotExist:
        pass

    s = Spider(url)
    if not s.backlinks(entry.get_absolute_url()):
        return HttpResponse('''<?xml version="1.0" encoding="utf-8"?>
                <response>
                    <error>1</error>
                    <message>URL doesn't link back</message>
                </response>''', mimetype='text/xml')

    if not blog_name:
        blog_name = url.split('/')[2]

    if title:
        excerpt = '%s\n\n%s' % (title, excerpt)

    Comment.objects.create(entry=entry, author=blog_name, author_uri=url, body=excerpt, type='T')

    return HttpResponse('''<?xml version="1.0" encoding="utf-8"?>
                <response>
                    <error>0</error>
                </response>''')

def xmlrpc_view(request):
    return XmlRpcDispatcher(request).dispatch()

class XmlRpcDispatcher(object):
    @staticmethod
    def fault(code, msg):
        return HttpResponse('''<?xml version="1.0"?>
        <methodResponse>
            <fault>
                <value>
                    <struct>
                        <member>
                            <name>faultCode</name>
                            <value><int>%d</int></value>
                        </member>
                        <member>
                            <name>faultString</name>
                            <value><string>%s</string></value>
                        </member>
                    </struct>
                </value>
            </fault>
        </methodResponse>''' % (code, msg), mimetype='text/xml')
    @staticmethod
    def pingback_reply(msg):
        return HttpResponse('''<?xml version="1.0"?>
        <methodResponse>
            <params>
                <param>
                    <value>
                        <string>%s</string>
                    </value>
                </param>
            </params>
        </methodResponse>''' % msg, mimetype='text/xml')
    def __init__(self, request):
        self.request = request

    def dispatch(self):
        if not self.request.raw_post_data:
            return HttpResponse('')

        self.tree = cElementTree.fromstring(self.request.raw_post_data.strip())
        method_name = self.tree.find('methodName').text
        method = getattr(self, method_name.replace('.', '_'), None)
        if method:
            self.params = []
            for v in self.tree.findall('params/param/value'):
                try:
                    child = v.getchildren()[0]
                except KeyError:
                    self.params.append(v.text) #string
                if child.tag == 'string':
                    self.params.append(child.text)
                if child.tag in ('int', 'i4'):
                    self.params.append(int(child.text))
                if child.tag == 'boolean':
                    self.params.append(child.text == '1')
                if child.tag == 'double':
                    self.params.append(float(chold.text))
                # Missing types, but for now, only strings are needed
            return method()
        else:
            return XmlRpcDispatcher.fault(1, 'Invalid method')

    def pingback_ping(self):
        source = self.params[0]
        target = self.params[1]
        slug = target.split('/')[-2]
        try:
            entry = Entry.objects.get(slug=slug)
            if not entry.allow_comments:
                raise Entry.DoesNotExist
        except Entry.DoesNotExist:
            return XmlRpcDispatcher.fault(33, 'The specified URI cannot be used as target')

        try:
            Comment.objects.get(entry=entry, type__in=['P', 'T'], author_uri=source)
            return XmlRpcDispatcher.fault(48, 'The pingback has already been registered')
        except Comment.DoesNotExist:
            pass

        s = Spider(source)
        if not s.backlinks(target):
            if s.code == 200:
                return XmlRpcDispatcher.fault(17, 'The source URI does not contain a link to the target URI')

            return XmlRpcDispatcher.fault(16, 'The source URI does not exist')

        Comment.objects.create(entry=entry, type='P',
                author=hostname_from_uri(source, http=False),
                author_uri=source, body='')

        return XmlRpcDispatcher.pingback_reply('Pingback stored')

