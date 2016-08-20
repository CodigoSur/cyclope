from django.core.management.base import BaseCommand, CommandError
from optparse import make_option
import mysql.connector
from cyclope.models import SiteSettings, RelatedContent
import re
from cyclope.apps.articles.models import Article
from django.contrib.sites.models import Site
from django.db import transaction
from cyclope.apps.staticpages.models import StaticPage
from django.contrib.contenttypes.models import ContentType
from cyclope.apps.custom_comments.models import CustomComment
from django.contrib.auth.models import User
from cyclope.core.collections.models import Collection, Category, Categorization
from cyclope.apps.medialibrary.models import ExternalContent, Picture, Document, RegularFile, BaseMedia, SoundTrack, MovieClip, FlashMovie
from django.conf import settings as _settings
from autoslug.settings import slugify
from operator import attrgetter
from django.db import IntegrityError
import operator

class Command(BaseCommand) :
    help = """Migrates a site in WordPress to Cyclope CMS.
    Requires the options server, database and user, passphrase is optional.
    Optional WordPress table prefix option, defaults to 'wp_'."""

    #NOTE django > 1.8 uses argparse instead of optparse module, 
    #so "You are encouraged to exclusively use **options for new commands."
    #https://docs.djangoproject.com/en/1.9/howto/custom-management-commands/
    option_list = BaseCommand.option_list + (
        make_option('--server',
            action='store',
            dest='server',
            default=None,
            help='WP-Site Host Name.'
        ),
        make_option('--user',
            action='store',
            dest='user',
            default=None,
            help='Database User.'
        ),
        make_option('--password',
            action='store',
            dest='password',
            default=None,
            help='Database Password.'
        ),
        make_option('--database',
            action='store',
            dest='db',
            default=None,
            help='Database name.'
        ),
        make_option('--table_prefix',
            action='store',
            dest='wp_prefix',
            default='wp_',
            help='Wordpress DB Table Prefix (defaults to \'wp_\').'
        ),
        make_option('--default_password',
            action='store',
            dest='wp_user_password',
            default=None,
            help='Default password for ALL users. Optional, otherwise usernames will be used.'
        ),
        make_option('--devel',
            action='store_true',
            dest='devel',
            help='Use http://localhost:8000 as site url (development)'
        ),
    )

    # class constants
    wp_prefix = 'wp_'
    wp_user_password = None
    wp_upload_path = "wp-content/uploads"
    devel_url = False
    wp_url = None

    def handle(self, *args, **options):
        """WordPress to Cyclope DataBase Migration Logic."""
        print"""
        :::::::::::wp2cyclope::::::::::::
        ::WordPress to Cyclope migrator::
        :::::::::::::::::::::::::::::::::\n\n-> hola, amigo!"""

        self.wp_prefix = options['wp_prefix']
        self.wp_user_password = options['wp_user_password']
        self.devel_url = options['devel']        

        print "-> clearing cyclope sqlite database..."
        self._clear_cyclope_db()
        
        print "-> connecting to wordpress mysql database..."
        cnx = self._mysql_connection(options['server'], options['db'], options['user'], options['password'])
        
        # SiteSettings <- wp_options
        settings = self._fetch_site_settings(cnx)
        print "-> nice to meet you, "+settings.site.name
        
        # Users <- wp_users
        #TODO send users a reset password link instead
        users_count, wp_users_count = self._fetch_users(cnx)
        print "-> migrated {}/{} users".format(users_count, wp_users_count)
        print "-> all users should reset their passwords!"
        if self.wp_user_password :
            print "   default temporary password for all users: {}.".format(self.wp_user_password)
        else:
            print "   temporary user passwords default to their username."

        print "-> starting contents migation..."
        # Articles <- wp_posts
        wp_posts_a_count, articles_count = self._fetch_articles(cnx, settings.site)
        print "-> migrated {} articles out of {} posts".format(articles_count, wp_posts_a_count)

        # StaticPages <- wp_posts
        wp_posts_p_count, pages_count = self._fetch_pages(cnx, settings.site)
        print "-> migrated {} static pages out of {} posts".format(pages_count, wp_posts_p_count)    

        # ExternalContent <- wp_links
        ex_content_count, wp_links_count = self._fetch_links(cnx)
        print "-> migrated {} external contents out of {} links".format(ex_content_count, wp_links_count)

        #we query article and page IDs to be able to resolve an ID's content type for related contents
        post_content_types = ('article', 'staticpage')
        object_type_ids = self._object_type_ids(post_content_types)

        # MediaLibrary <- wp_posts
        attachments_count, pictures_count, documents_count, files_count, sound_count, movie_count, flash_count, related_count = self._fetch_attachments(cnx, object_type_ids)
        print "-> migrated {} pictures, {} documents, {} regular files, {} sound tracks and {} movies out of {} attachments".format(pictures_count, documents_count, files_count, sound_count, (movie_count+flash_count), attachments_count)
        print "-> related {} attachments to their posts or pages as related contents".format(related_count/2)

        #with complete the ID type matrix with attachments in order to associate all types comments and categories
        attachment_content_types = ('picture', 'document', 'regularfile', 'flashmovie', 'movieclip', 'soundtrack')
        object_type_ids.update(self._object_type_ids(attachment_content_types))

        # Comments <- wp_comments
        comments_count = self._fetch_comments(cnx, settings.site, object_type_ids)
        print "-> migrated {} comments".format(comments_count)

        # Collections & Categories <- WP terms & term_taxonomies
        categorizable_content_types = ('article',) # by default in WP just posts can be categorized or tagged, feature is available to pages and media as plugins
        collection_counts, category_count, wp_term_taxonomy_count, categorizations_count = self._fetch_term_taxonomies(cnx, object_type_ids, categorizable_content_types)
        print "-> migrated {} collections and {} categories out of {} term taxonomies".format(collection_counts, category_count, wp_term_taxonomy_count)
        print "-> categorized {} articles, pages, links & attachments".format(categorizations_count)

        #close mysql connection
        cnx.close()
        # WELCOME
    ####

    def _mysql_connection(self, host, database, user, password):
        """Establish a MySQL connection to the given option params and return it."""
        config = {
            'host': host,
            'database': database,
            'user': user
        }
        if not password is None : config['password']=password
        try:
            cnx = mysql.connector.connect(**config)
            return cnx
        except mysql.connector.Error as err:
            print err
            raise
        else:
            return cnx

    def _clear_cyclope_db(self):
        #TODO clearing settings erases default layout & breaks
        #SiteSettings.objects.all().delete()
        #Site.objects.all().delete()
        Article.objects.all().delete()
        StaticPage.objects.all().delete()
        CustomComment.objects.all().delete()
        User.objects.all().delete()
        Collection.objects.all().delete()
        Category.objects.all().delete()
        ExternalContent.objects.all().delete()
        Picture.objects.all().delete()
        Document.objects.all().delete()
        RegularFile.objects.all().delete()
        SoundTrack.objects.all().delete()
        MovieClip.objects.all().delete()
        FlashMovie.objects.all().delete()
        RelatedContent.objects.all().delete()

    ########
    #QUERIES

    def _fetch_site_settings(self, mysql_cnx):
        """Execute single query to WP _options table to retrieve the given option names."""
        options = ('siteurl', 'blogname', 'blogdescription', 'home', 'default_comment_status', 'comment_moderation', 'comments_notify', 'upload_path')
        #single query
        query = "SELECT option_name, option_value FROM "+self.wp_prefix+"options WHERE option_name IN {}".format(options)
        cursor = mysql_cnx.cursor()
        cursor.execute(query)
        wp_options = dict(cursor.fetchall())
        cursor.close()
        settings = SiteSettings.objects.all()[0]
        site = settings.site
        settings.global_title = wp_options['blogname']
        settings.description = wp_options['blogdescription']
        #NOTE settings.keywords = WP doesn't use meta tags, only as a plugin
        settings.allow_comments = u'YES' if wp_options['default_comment_status']=='open' else u'NO'
        settings.moderate_comments = wp_options['comment_moderation']==1 #default False
        settings.enable_comments_notifications = wp_options['comments_notify'] in ('', 1) #default True
        settings.show_author = 'USER' # WP uses users as authors
        site.name = wp_options['blogname']
        if not self.devel_url:
            site.domain = wp_options['siteurl'].replace("http://","")
        else:
            site.domain = "localhost:8000"
        #store wordpress url anyway in order to use it to replace links to uploads
        self.wp_url = wp_options['siteurl'].replace("http://","")
        site.save()
        settings.site = site
        settings.save()
        #
        if wp_options['upload_path'] != '' : self.wp_upload_path = wp_options['upload_path']
        return settings

    def _fetch_articles(self, mysql_cnx, site):
        """Queries the given fields to WP posts table selecting only posts, not pages nor attachments nor revisions,
           It parses data as key-value pairs to instance rows as Articles and save them.
           Returns the number of created Articles and of fetched rows in a tuple."""
        fields = ('ID', 'post_title', 'post_status', 'post_date', 'post_modified', 'comment_status', 'post_content', 'post_excerpt', 'post_author')
        query = re.sub("[()']", '', "SELECT {} FROM ".format(fields))+self.wp_prefix+"posts WHERE post_type='post'"
        cursor = mysql_cnx.cursor()
        cursor.execute(query)
        #single transaction for all articles
        transaction.enter_transaction_management()
        transaction.managed(True)
        for wp_post in cursor :
            article = self._post_to_article(dict(zip(fields, wp_post)), site)
            article.save()
        transaction.commit()
        transaction.leave_transaction_management()
        counts = (cursor.rowcount, Article.objects.count())
        cursor.close()
        return counts 

    def _fetch_pages(self, mysql_cnx, site):
        """Queries to WP posts table selecting only pages, not posts nor attachments nor revisions."""
        fields = ('ID', 'post_title','post_status','post_date', 'post_modified',  'comment_status', 'post_content', 'post_excerpt', 'post_author')
        query = re.sub("[()']", '', "SELECT {} FROM ".format(fields))+self.wp_prefix+"posts WHERE post_type='page'"
        cursor = mysql_cnx.cursor()
        cursor.execute(query)
        #single transaction for all pages
        transaction.enter_transaction_management()
        transaction.managed(True)
        for wp_post in cursor :
            page = self._post_to_static_page(dict(zip(fields, wp_post)), site)
            page.save()
        transaction.commit()
        transaction.leave_transaction_management()
        counts = (cursor.rowcount, StaticPage.objects.count())
        cursor.close()
        return counts 

    def _fetch_attachments(self, mysql_cnx, object_type_ids):
        """Queries to WP posts table selecting attachments, not..."""
        fields = ('ID', 'post_mime_type', 'guid', 'post_title', 'post_status', 'post_author', 'post_date', 'post_modified', 'comment_status', 'post_content', 'post_excerpt', 'post_parent')
        query = re.sub("[()']", '', "SELECT {} FROM ".format(fields))+self.wp_prefix+"posts WHERE post_type='attachment'"
        cursor = mysql_cnx.cursor()
        cursor.execute(query)
        #single transaction for all articles
        transaction.enter_transaction_management()
        transaction.managed(True)
        for wp_post in cursor :
            post = dict(zip(fields, wp_post))
            attachment = self._post_to_attachment(post)
            attachment.save() #whatever its type
            if post['post_parent'] != 0 :
                relate_self, relate_other = self._relate_contents(attachment, post['post_parent'], object_type_ids)
                relate_self.save() #related contents
                relate_other.save()
        transaction.commit()
        transaction.leave_transaction_management()
        counts = (cursor.rowcount, Picture.objects.count(), Document.objects.count(), RegularFile.objects.count(), SoundTrack.objects.count(), MovieClip.objects.count(), FlashMovie.objects.count(), RelatedContent.objects.count())
        cursor.close()
        return counts

    def _fetch_comments(self, mysql_cnx, site, object_type_ids):
        """Populates cyclope custom comments from WP table wp_comments.
           instead of querying the related object for each comment and atomizing transactions, which could be expensive,
           we use an additional query for each content type only, and the transaction is repeated just as many times.
           we receive Site ID which is already above in the script."""
        fields = ('comment_ID', 'comment_author', 'comment_author_email', 'comment_author_url', 'comment_content', 'comment_date', 'comment_author_IP', 'comment_approved', 'comment_parent', 'user_id', 'comment_post_ID')
        counter = 0
        for content_type_id, post_ids in object_type_ids.iteritems():
            if len(post_ids) == 0 : continue
            query = re.sub("[()']", '', "SELECT {} FROM ".format(fields))+self.wp_prefix+"comments WHERE comment_approved!='spam' AND comment_post_ID IN {}".format(post_ids)
            cursor = mysql_cnx.cursor()
            cursor.execute(query)
            #single transaction per content_type
            transaction.enter_transaction_management()
            transaction.managed(True)
            for wp_comment in cursor:
                comment_hash = dict(zip(fields,wp_comment))
                comment = self._wp_comment_to_custom(comment_hash, site, content_type_id)
                comment.save()
            transaction.commit()
            transaction.leave_transaction_management()
            if cursor.rowcount > 0 : counter += cursor.rowcount
            cursor.close()
        return counter

    def _fetch_users(self, mysql_cnx):
        """Populates cyclope django-based auth users from WP table wp_users."""
        fields = ('ID', 'user_login', 'user_nicename', 'display_name', 'user_email', 'user_registered')
        query = re.sub("[()']", '', "SELECT {} FROM ".format(fields))+self.wp_prefix+"users"
        cursor = mysql_cnx.cursor()
        cursor.execute(query)
        wp_users = cursor.fetchall()
        def _hash_result(fields, user): return dict(zip(fields,user))
        users = map(_hash_result,[fields]*len(wp_users), wp_users)
        users = map(self._wp_user_to_user, users)
        User.objects.bulk_create(users)
        counts = (User.objects.count(), cursor.rowcount)
        cursor.close()
        return counts

    def _fetch_term_taxonomies(self, mysql_cnx, object_type_ids, categorizable_content_types):
        """Creates a Collection from each of the taxonomies in the term_taxonomy table. (taxonomy is a column)
           Creates a Category for each Term. The relation with its collection is inferred from the taxonomy value.
           Creates Categorizations to link objects to its Categories reading the term_relationships table.
           The type of the related object is deduced from its id, since they all come from the wp_posts table. (Except links, see detail)"""
        #Cyclope collections are WP term taxonomies
        query = "SELECT DISTINCT(taxonomy) FROM "+self.wp_prefix+"term_taxonomy"
        cursor = mysql_cnx.cursor()
        cursor.execute(query)
        for taxonomy in cursor :
            collection = self._wp_term_taxonomy_to_collection(taxonomy[0])
            collection.save()
        cursor.close()
        #collections are used for articles only (but could be used for types comming from the posts table via plugins), except link categories which are for external content
        categorizable_content_types = [ContentType.objects.get(model=content_type) for content_type in categorizable_content_types]
        for collection in Collection.objects.exclude(name__contains="link"):
            collection.content_types = categorizable_content_types
            collection.save()
        for collection in Collection.objects.filter(name__contains="link"):
            collection.content_types = [ContentType.objects.get(name='external content')]
            collection.save()
        #Cyclope categories are WP terms
        cursor = mysql_cnx.cursor()
        fields = ('t.term_id', 't.name', 'tt.taxonomy', 'tt.parent', 'tt.description')#preserve'slug'? even for articles...
        query = re.sub("[()']", '', "SELECT {} FROM ".format(fields))+self.wp_prefix+"terms t INNER JOIN "+self.wp_prefix+"term_taxonomy tt ON t.term_id = tt.term_id"
        cursor.execute(query)
        #query for collection ids only once to associate them
        collection_ids = {}
        for collection in Collection.objects.all() :
            collection_ids[collection.name]=collection.id
        #save categorties in bulk so it doesn't call custom Category save, which doesn't allow custom ids (WP referential integrity)    
        categories=[]
        for term_taxonomy in cursor:
            cat_hash = dict(zip(fields, term_taxonomy))
            categories.append(self._wp_term_to_category(cat_hash,collection_ids))
        term_taxonomy_count = cursor.rowcount     
        cursor.close()
    	#find duplicate names, since AutoSlugField doesn't properly preserve uniqueness in bulk.
        try: #duplicate query is expesive, we try not to perform it if we can
            Category.objects.bulk_create(categories)
        except IntegrityError:
            cursor = mysql_cnx.cursor()
            query = "SELECT term_id FROM "+self.wp_prefix+"terms WHERE name IN (SELECT name FROM "+self.wp_prefix+"terms GROUP BY name HAVING COUNT(name) > 1)"
            cursor.execute(query)
            result = [x[0] for x in cursor.fetchall()]
            cursor.close()
            duplicates = [cat for cat in categories if cat.id in result]
            for dup in duplicates: categories.remove(dup)
            #sort duplicate categories by name ignoring case
            duplicates.sort(key = lambda cat: operator.attrgetter('name')(cat).lower(), reverse=False)
            # categories can have the same name if they're different collections, but not the same slug
            duplicates = self._dup_categories_slugs(duplicates)
            # categories with the same collection cannot have the same name
            duplicates = self._dup_categories_collections(duplicates)
            categories += duplicates
            Category.objects.bulk_create(categories)
        #set MPTT fields using django-mptt's own method
        Category.tree.rebuild()
        #Cyclope categorizations are WP term relationships
        fields = ('tr.object_id', 'tr.term_taxonomy_id', 'tt.term_id', 'tt.taxonomy', 'tr.term_order')
        query = re.sub("[()']", '', "SELECT {} FROM ".format(fields))+self.wp_prefix+"term_taxonomy tt INNER JOIN "+self.wp_prefix+"term_relationships tr ON tr.term_taxonomy_id=tt.term_taxonomy_id"
        cursor = mysql_cnx.cursor()
        cursor.execute(query)
        categorizations = []
        for term_relationship in cursor:
            categorizations.append(self._wp_term_relationship_to_categorization(dict(zip(fields, term_relationship)), object_type_ids))
        cursor.close()
        categorizations = filter(lambda x: x is not None, categorizations) # clean None
        Categorization.objects.bulk_create(categorizations)                
        counts = (Collection.objects.count(), Category.objects.count(), term_taxonomy_count, len(categorizations))
        return counts

    def _fetch_links(self, mysql_cnx):
        """Stores WP links as Cyclope ExternalContent objects."""
        fields = ('link_id', 'link_url', 'link_description', 'link_image', 'link_name', 'link_visible', 'link_owner', 'link_updated', 'link_target')
        query = re.sub("[()']", '', "SELECT {} FROM ".format(fields))+self.wp_prefix+"links"
        cursor = mysql_cnx.cursor()
        cursor.execute(query)
        transaction.enter_transaction_management()
        transaction.managed(True)
        for wp_link in cursor :
            link = self._wp_link_to_external_content(dict(zip(fields, wp_link)))
            link.save() # slug
        transaction.commit()
        transaction.leave_transaction_management()
        counts = (ExternalContent.objects.count(), cursor.rowcount)
        cursor.close()
        return counts

    ########
    #HELPERS

    #wp terms relate to posts, which are cyclope's articles, staticpages or attachments
    #comming from the same table, their IDs shouldn't intersect
    def _object_type_ids(self, post_content_types):
        result = {}                
        for post_content_type in post_content_types:
            content_type = ContentType.objects.get(model=post_content_type)
            object_ids = tuple([object.id for object in content_type.get_all_objects_for_this_type()])
            result[content_type.id] = object_ids
        return result

    # term taxonomies relate to posts which we have created as articles, static pages and attachments
    # only the taxonomy link_category relates to links
    def _get_object_type(self, object_type_ids, object_id, taxonomy):
        if taxonomy != 'link_category':
            for item in object_type_ids.items(): 
                if object_id in item[1]:
                    return item[0]
        else:
            return ContentType.objects.get(name='external content').id # links

    def _dup_categories_slugs(self, categories):
        #use a counter to differentiate them
        counter = 2
        for idx, category in enumerate(categories):
            if idx == 0 :
                category.slug = slugify(category.name)
            else:
                if categories[idx-1].name.lower() == category.name.lower() :
                    category.slug = slugify(category.name) + '-' + str(counter)
                    counter += 1
                else:
                    counter = 2
                    category.slug = slugify(category.name)
        return categories

    def _dup_categories_collections(self, categories):
        counter = 1
        for idx, category in enumerate(categories):
            if idx != 0 :
                if categories[idx-1].name.lower() == category.name.lower() :
                    if categories[idx-1].collection == category.collection :
                        category.name = category.name + " (" + str(counter) + ")"
                else : counter = 1
        return categories

    #https://codex.wordpress.org/Determining_Plugin_and_Content_Directories
    def _parse_media_url(self, url):
        return _settings.FILEBROWSER_DIRECTORY+url.split(self.wp_upload_path)[1]

    def _parse_content_links(self, content, site):
        old_upload_path = self.wp_url + '/' + self.wp_upload_path + '/'                        # www.numerica.cl/wp-content/uploads/
        new_upload_path = site.domain +_settings.STATIC_URL +_settings.FILEBROWSER_DIRECTORY   # localhost:8000/media/uploads/
        if old_upload_path in content:
            content = content.replace(old_upload_path, new_upload_path)            
        return content

    ###################
    #OBJECT CONVERSIONS
    
    #TODO PRESERVE PERMALINKS
    def _post_to_article(self, post, site):
        """Instances an Article object from a WP post hash."""
        return Article(
            id = post['ID'],
            name = post['post_title'],
            #post_name is AutoSlug 
            text = self._parse_content_links(post['post_content'], site),
            date = post['post_date'], #redundant
            creation_date = post['post_date'],
            modification_date = post['post_modified'],
            published = post['post_status']=='publish',#private and draft are unpublished
            #in WP all posts have a status, they are saved as the option that's set(?).
            #if the user then tries to close them all, he shouldn't set them one by one.
            #whe should set them to SITE default unless comments are explicitly closed, which is the minority(?)       
            allow_comments = 'SITE' if post['comment_status']!='closed' else 'NO',
            summary = post['post_excerpt'],
            #pretitle has no equivalent in WP
            # check comments related_contents picture author source
            user_id = post['post_author'], # WP referential integrity maintained
            show_author = 'USER' #default SITE doesn't work when site sets USER
        )

    def _post_to_static_page(self, post, site):
        return StaticPage(
            id = post['ID'],
            name = post['post_title'],
            text = self._parse_content_links(post['post_content'], site),
            creation_date = post['post_date'],
            modification_date = post['post_modified'],
            published = post['post_status']=='publish',#private and draft are unpublished
            allow_comments = post['comment_status']=='open',#see article's allow_comments
            summary = post['post_excerpt'],
            #check related_contents comments
            user_id = post['post_author'], # WP referential integrity maintained
            show_author = 'USER' #default SITE doesn't work when site sets USER
        )

    def _wp_comment_to_custom(self, comment, site, content_type_id):
        comment_parent = comment['comment_parent'] if comment['comment_parent']!=0 else None
        #tree_path and last_child_id are automagically set by threadedcomments framework
        return CustomComment(
            id = comment['comment_ID'],
            object_pk = comment['comment_post_ID'],
            content_type_id = content_type_id,
            site = site,
            user_name = comment['comment_author'],
            user_email = comment['comment_author_email'],
            user_url = comment['comment_author_url'],
            comment = comment['comment_content'],
            submit_date = comment['comment_date'],
            ip_address = comment['comment_author_IP'],
            user_id = comment['user_id'] if comment['user_id']!=0 else None, # WP referential integrity maintained
            parent_id = comment_parent,
            subscribe = False #DB default
        )

    #https://docs.djangoproject.com/en/1.4/topics/auth/#fields
    def _wp_user_to_user(self, wp_user):
        user = User(
            id =  wp_user['ID'],
            username = wp_user['user_login'],
            first_name = wp_user['display_name'],
            #last_name=wp_user['user_nicename'], or parse display_name 
            #WP user_url will be lost
            email = wp_user['user_email'],
            is_staff=True,
            #user_status is a dead column in WP
            is_active=True,
            is_superuser=True,#else doesn't have any permissions
            #last_login='', we don't have this data in WP?
            date_joined = wp_user['user_registered']
        )
        password = self.wp_user_password if self.wp_user_password else user.username
        user.set_password(password)
        return user

    def _wp_term_taxonomy_to_collection(self, taxonomy):
        return Collection(
            name = taxonomy,#everything else to defaults
        )

    def _wp_term_to_category(self, term_taxonomy, collection_ids):
        return Category(
            id = term_taxonomy['t.term_id'],
            name = term_taxonomy['t.name'],
            collection_id = collection_ids[term_taxonomy['tt.taxonomy']],
            description = term_taxonomy['tt.description'],
            parent_id = term_taxonomy['tt.parent'] if term_taxonomy['tt.parent']!=0 else None,
            #bulk creation fails if these are null
            lft=0,
            rght=0,
            tree_id=0,
            level=0
        )

    def _wp_term_relationship_to_categorization(self, term_relationship, object_type_ids):
        content_type_id = self._get_object_type(object_type_ids, term_relationship['tr.object_id'], term_relationship['tt.taxonomy'])
        if content_type_id is None: return None # TODO this happens because there are categories for MENUs, develop them as Layouts
        return Categorization(
            category_id = term_relationship['tt.term_id'],
            content_type_id = content_type_id,
            object_id = term_relationship['tr.object_id'],
            order = term_relationship['tr.term_order']
        )

    def _wp_link_to_external_content(self, link):
        return ExternalContent(
            id = link['link_id'],
            content_url = link['link_url'],
            description = link['link_description'],
            new_window = link['link_target'] == '_blank',
            image = link['link_image'],          
            #base content            
            name = link['link_name'],
            published = link['link_visible'] == 'Y',
            user_id = link['link_owner'],
            modification_date = link['link_updated'],
            allow_comments = 'SITE', #if post['comment_status']!='closed' else 'NO',
            show_author = 'USER', #default SITE doesn't work when site sets
        )
        #rating, updated, rel, notes, rss will be lost

    def _post_to_attachment(self, post):
        #http://www.iana.org/assignments/media-types/media-types.xhtml#examples
        #top level media types : image, audio, video, application, multipart, text, example, message, model
        top_level_mime, mime_type = tuple(post['post_mime_type'].split('/'))
        if  top_level_mime == 'image':
            return self._wp_post_to_picture(post)
        elif  top_level_mime == 'audio':
            return self._wp_post_to_sound_track(post)
        elif  top_level_mime == 'video':              
            if mime_type == 'x-flv': 
                return self._wp_post_to_flash_movie(post)
            else:
                return self._wp_post_to_movie_clip(post)
        elif top_level_mime == 'application':
            if mime_type == 'pdf' : 
                return self._wp_post_to_document(post)
            elif mime_type == 'x-shockwave-flash' : 
                return self._wp_post_to_flash_movie(post)
            else :
                return self._wp_post_to_regular_file(post)
        elif top_level_mime == 'text':
            return self._wp_post_to_document(post)
        else: #multipart, example, message, model
            return self._wp_post_to_regular_file(post)

    def _wp_post_to_picture(self, post):
        return Picture(
            #BaseContent
            id = post['ID'],
            name = post['post_title'],
            #slug is post_name
            published = post['post_status']=='publish',
            user_id = post['post_author'],
            #related_contents
            creation_date = post['post_date'],
            modification_date = post['post_modified'],
            allow_comments = 'SITE' if post['comment_status']!='closed' else 'NO',#see _post_to_article 
            #comments
            show_author = 'USER',
            #BaseMedia                
            #author
            #source
            description = post['post_content'] or post['post_excerpt'], #if both are present excerpt will be lost, doesn't happen in Numerica
            #Picture
            image = self._parse_media_url(post['guid'])
        )

    def _wp_post_to_document(self, post):
        return Document(
            #BaseContent
            id = post['ID'],
            name = post['post_title'],
            #slug is post_name
            published = post['post_status']=='publish',
            user_id = post['post_author'],
            creation_date = post['post_date'],
            modification_date = post['post_modified'],
            allow_comments = 'SITE' if post['comment_status']!='closed' else 'NO',#see _post_to_article
            show_author = 'USER',
            #BaseMedia                
            description = post['post_content'] or post['post_excerpt'], # see Picture
            #Document
            document = self._parse_media_url(post['guid'])
            #image will be None
        )

    def _wp_post_to_regular_file(self, post):
        return RegularFile(
            #BaseContent
            id = post['ID'],
            name = post['post_title'],
            #slug is post_name
            published = post['post_status']=='publish',
            user_id = post['post_author'],
            creation_date = post['post_date'],
            modification_date = post['post_modified'],
            allow_comments = 'SITE' if post['comment_status']!='closed' else 'NO',# see _post_to_article
            show_author = 'USER',
            #BaseMedia                
            description = post['post_content'] or post['post_excerpt'], # see Picture
            #Document
            file = self._parse_media_url(post['guid'])
            #image will be None
        )

    def _wp_post_to_sound_track(self, post):
        return SoundTrack(
            #BaseContent
            id = post['ID'],
            name = post['post_title'],
            #slug is post_name
            published = post['post_status']=='publish',
            user_id = post['post_author'],
            creation_date = post['post_date'],
            modification_date = post['post_modified'],
            allow_comments = 'SITE' if post['comment_status']!='closed' else 'NO',#see _post_to_article 
            #comments
            show_author = 'USER',
            #BaseMedia                
            #author
            #source
            description = post['post_content'] or post['post_excerpt'], #if both are present excerpt will be lost, doesn't happen in Numerica
            #Picture
            audio = self._parse_media_url(post['guid'])
        )
    def _wp_post_to_movie_clip(self, post):
        return MovieClip(
            #BaseContent
            id = post['ID'],
            name = post['post_title'],
            #slug is post_name
            published = post['post_status']=='publish',
            user_id = post['post_author'],
            creation_date = post['post_date'],
            modification_date = post['post_modified'],
            allow_comments = 'SITE' if post['comment_status']!='closed' else 'NO',#see _post_to_article 
            #comments
            show_author = 'USER',
            #BaseMedia                
            #author
            #source
            description = post['post_content'] or post['post_excerpt'], #if both are present excerpt will be lost, doesn't happen in Numerica
            #Picture
            video = self._parse_media_url(post['guid'])
        )
    def _wp_post_to_flash_movie(self, post):
        return FlashMovie(
            #BaseContent
            id = post['ID'],
            name = post['post_title'],
            #slug is post_name
            published = post['post_status']=='publish',
            user_id = post['post_author'],
            creation_date = post['post_date'],
            modification_date = post['post_modified'],
            allow_comments = 'SITE' if post['comment_status']!='closed' else 'NO',#see _post_to_article 
            #comments
            show_author = 'USER',
            #BaseMedia                
            #author
            #source
            description = post['post_content'] or post['post_excerpt'], #if both are present excerpt will be lost, doesn't happen in Numerica
            #Picture
            flash = self._parse_media_url(post['guid'])
        )

    def _relate_contents(self, attachment, other_id, object_type_ids):
        one_way = RelatedContent(
            self_object = attachment,
            other_type_id = self._get_object_type(object_type_ids, other_id, ''),#article or page
            other_id = other_id
            #order null       
        )
        the_other = RelatedContent(
            other_object = attachment,
            self_type_id = self._get_object_type(object_type_ids, other_id, ''),#article or page
            self_id = other_id
            #order null       
        )
        return (one_way, the_other)

