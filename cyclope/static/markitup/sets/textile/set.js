// -------------------------------------------------------------------
// markItUp!
// -------------------------------------------------------------------
// Copyright (C) 2008 Jay Salvat
// http://markitup.jaysalvat.com/
// -------------------------------------------------------------------
// Textile tags example
// http://en.wikipedia.org/wiki/Textile_(markup_language)
// http://www.textism.com/
// -------------------------------------------------------------------
// Feel free to add more tags
// -------------------------------------------------------------------
mySettings = {
	previewParserPath:	'/markitup/preview/',
	onShiftEnter:		{keepDefault:false, replaceWith:'\n\n'},
	markupSet: [
		{name:'Heading 1', key:'1', openWith:'h1(!(([![Class]!]))!). ', placeHolder:'Your title here...' },
		{name:'Heading 2', key:'2', openWith:'h2(!(([![Class]!]))!). ', placeHolder:'Your title here...' },
		{name:'Heading 3', key:'3', openWith:'h3(!(([![Class]!]))!). ', placeHolder:'Your title here...' },
		{name:'Heading 4', key:'4', openWith:'h4(!(([![Class]!]))!). ', placeHolder:'Your title here...' },
		{name:'Heading 5', key:'5', openWith:'h5(!(([![Class]!]))!). ', placeHolder:'Your title here...' },
		{name:'Heading 6', key:'6', openWith:'h6(!(([![Class]!]))!). ', placeHolder:'Your title here...' },
		{name:'Paragraph', key:'P', openWith:'p(!(([![Class]!]))!). '},
		{separator:'---------------' },
		{name:'Bold', key:'B', closeWith:'*', openWith:'*'},
		{name:'Italic', key:'I', closeWith:'_', openWith:'_'},
		{name:'Stroke through', key:'S', closeWith:'-', openWith:'-'},
		{name:'Em dash', key:'D', closeWith:'--', openWith:'--'},
		{name:'Underlined', key:'U', closeWith:'+', openWith:'+'},
		{separator:'---------------' },
		{name:'Align left', openWith:'p<. '},
		{name:'Align right', openWith:'p>. '},
		{name:'Align centered', openWith:'p=. '},
		{name:'Align justified', openWith:'p<>. '},
		{separator:'---------------' },
		{name:'Bulleted list', openWith:'(!(* |!|*)!)'},
		{name:'Numeric list', openWith:'(!(# |!|#)!)'},
		{name:'Text indent', openWith:'p((. '},
		{separator:'---------------' },
		{name:'Picture', replaceWith: function(markItUp) {}},
		{name:'Link', openWith:'"', closeWith:'([![Title]!])":[![Link:!:http://]!]', placeHolder:'Your text to link here...' },
		{separator:'---------------' },
		{name:'Quotes', openWith:'bq(!(([![Class]!])!)). '},
		{name:'Code', openWith:'@', closeWith:'@'},
/**		Hack for especials links with % **/
		{name:'Especial link HTML', openWith:'<notextile><a title="[![Title]!]" href="[![Link:!:http://]!]" target="_blank">', closeWith:'</a></notextile>', placeHolder:'Your especial link here...' },
//		{separator:'---------------' },
//		{name:'Preview', call:'preview', className:'preview'}
	]
}

//TODO(NumericA) MOVE EVERYTHING BELOW TO ITS OWN SCRIPT

String.prototype.capitalize = function() {
    return this.charAt(0).toUpperCase() + this.slice(1);
}

//Content Type to HTML 5 mapping
//TODO(NumericA) source elements can specify MIME type. may be should for video codecs...
//TODO handle browsers that don't support HTML5
function generate_media_tag(url, media_type, media_desc){
    switch(media_type){
        case 'picture':
            return {replaceWith: '!(left)'+url+'('+media_desc+')!'};
        case 'soundtrack':
            audio = "<audio controls>"
                   +"<source src='"+url+"'>"
                   + media_desc
                   +"</audio>";
            return {replaceWith: '=='+audio+'=='};
        case 'movieclip':
            video = "<video controls>"
                   +"<source src='"+url+"'>"
                   + media_desc
                   +"</video>";
            return {replaceWith: '=='+video+'=='};
        case 'document': // most browsers require a plugin for this to work
            doc = "<object data='"+url+"' width='550' height='400' type='application/pdf'>"+media_desc+"</object>";
            return {replaceWith: '=='+doc+'=='};
        case 'flashmovie':
            flash = "<object data='"+url+"' width='550' height='400'>"+media_desc+"</object>";
            return {replaceWith: '=='+flash+'=='};
        default:
            throw 'Embedded Media Widget: unexistent content type!';
    }
}

/**
I added the FileBrowserHelper object so that it can store the original markitup
object that fired the event / popup, so that I can use it when trying to return
to the editor.
**/
var media_widget = null;
var FileBrowserHelper = {
    markItUp: false, // objet to store id of the textarea clicked
    insertPicture: function(markItUp) {
                $("#markItUp"+markItUp.capitalize() +" .markItUpButton20").click(function (){
                    FileBrowserHelper.markItUp = markItUp;
                    media_widget = $("#media_iframe").mediaWidget("position", this).mediaWidget("open");
                    media_widget.fb_helper = FileBrowserHelper;
                });
    },
    triggerInsert: function(url, media_type, media_desc) {
        tag_hash = generate_media_tag(url, media_type, media_desc);
        $("#"+this.markItUp).trigger('insertion', [tag_hash]);
    }
};
