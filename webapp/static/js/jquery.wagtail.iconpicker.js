var $icomoonPrefix = '',
    $fontelloPrefix = '',
    $icomoon_json_icons = [],
    $icomoon_json_search = [],
    $fontello_json_icons = [];

function loadJSON(filePath, origin='icomoon') {
    // *Load json file;
    // var json = loadTextFileAjaxSync(filePath, "application/json");
    // if (json==false){return false;}
    // *Parse json
    // var response = JSON.parse(json);
    // *Get the class prefix
    // Get the JSON file
    $.ajax({
        url: filePath,
        type: 'GET',
        dataType: 'json'
    })
    .done(function(response) {
        if (origin==='icomoon'){
            var classPrefix = response.preferences.fontPref.prefix,
                icomoon_json_icons = [],
                icomoon_json_search = [];

            // For each icon
            $.each(response.icons, function(i, v) {
                // Set the source
                icomoon_json_icons.push( classPrefix + v.properties.name );

                // Create and set the search source
                if ( v.icon && v.icon.tags && v.icon.tags.length ) {
                    icomoon_json_search.push( v.properties.name + ' ' + v.icon.tags.join(' ') );
                } else {
                    icomoon_json_search.push( v.properties.name );
                }
            });
            $classPrefix = classPrefix;
            $icomoon_json_icons = icomoon_json_icons;
            $icomoon_json_search = icomoon_json_search;
        }
        if (origin==='fontello'){
            var fontello_json_icons = [];
            // Push the fonts into the array
            $.each(response.glyphs, function(i, v) {
                fontello_json_icons.push( response.css_prefix_text + v.css );
            });
            $fontello_json_icons = fontello_json_icons;
        }
        return true;
    })
    .fail(function() {
        return false;
    });
}

function loadTextFileAjaxSync(filePath, mimeType)
{
  var xmlhttp=new XMLHttpRequest();
  xmlhttp.open("GET",filePath,false);
  if (mimeType != null) {
    if (xmlhttp.overrideMimeType) {
      xmlhttp.overrideMimeType(mimeType);
    }
  }
  xmlhttp.send();
  if (xmlhttp.status==200)
  {
    return xmlhttp.responseText;
  }
  else {
    // TODO Throw exception
    return false;
  }
}

jQuery.fn.extend({
  fontpickerup: function() {
    return this.each(function() {
        $(this).fontIconPicker({
            source: $icomoon_json_icons,
            searchSource: $icomoon_json_search,
            theme: 'fip-grey',
            emptyIcon: true,
            hasSearch: true,
        });
    });
  }
});
