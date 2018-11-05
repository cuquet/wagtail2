/* Creates the copy buttons in the header of each stream field */
$(function () {
	$('div.PanelTabs.stream-field').each(function () {
        loadCopyButtons($(this).children('div.panel-heading'));
	});

    $('.nav-tabs a').on('shown.bs.tab', function(){
        if ($(this).parents('div.PanelTabs').hasClass('stream-field')){
            var panel = $(this).parents('div.panel-heading');
            $(panel).children('.translation-field-copy-wrapper').empty().html('&nbsp;(Copy content from)');
            loadCopyButtons(panel);
        }
    });

	$('.translation-field-copy').click(function(event){
		event.preventDefault();
		var lang = $(this).attr('data-lang-code');
		var currentLang = $(this).attr('current-lang-code');
		requestCopyField(lang, currentLang);
	});
});

function loadCopyButtons(panel){
    var arrayFieldId = [],
        currentFieldId = '';
    panel.find('ul.nav-tabs li').each(function(){
        if ($(this).hasClass('active')){
            currentFieldId = $(this).data('fieldname');
        }else{
            arrayFieldId.push($(this).data('fieldname'));
        }
    });
    var $thisButtonGroup = $(panel).children('.translation-field-copy-wrapper');
    $thisButtonGroup.html('&nbsp;(Copy content from)');
    $.each(arrayFieldId, function( index, value ) {
        $thisButtonGroup.append('<li class="button button-small button-secondary translation-field-copy" current-lang-code="'+ currentFieldId +'" data-lang-code="'+ value +'">'+ value.substr(value.indexOf("_") + 1)+'</li>');
    });
}

function requestCopyField(originID, targetID) {
	var serializedForm = $("#page-edit-form").serializeArray();
	var serializedOriginField = $.grep(serializedForm, function(obj){return obj.name.indexOf(originID) >= 0;});
	var jsonString = JSON.stringify(serializedOriginField);

	$.ajax({
		url: 'copy_translation_content',
		type: 'POST',
		dataType: 'json',
		data: {'origin_field_name': originID, 'target_field_name': targetID, 'serializedOriginField': jsonString},
	})
	.done(function(data) {
		var wrapperDiv = $("#"+targetID+"-count").parents('.input')[0];
		$(wrapperDiv).html(data);
	})
	.fail(function(error) {
		console.log("wagtail-modeltranslation error: %s", error.responseText);
	})

}
