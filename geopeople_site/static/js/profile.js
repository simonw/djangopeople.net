window.onload = function() {    
    function ShrinkControl() {}
    ShrinkControl.prototype = new GControl();
    ShrinkControl.prototype.initialize = function(gmap) {
        var shrinkButton = document.createElement('div');
        shrinkButton.innerHTML = 'Shrink map';
        this.setButtonStyle_(shrinkButton);
        google.maps.Event.addDomListener(shrinkButton, "click", function() {
            $('#gmap').css({'cursor': 'pointer'}).attr(
                'title', 'Activate larger map'
            );
            hideNearbyPeople(gmap);
            gmap.removeControl(largeMapControl);
            gmap.removeControl(mapTypeControl);
            gmap.removeControl(shrinkControl);
            // Back to original center:
            var point = new google.maps.LatLng(
                person_latitude, person_longitude
            );
            var marker = new google.maps.Marker(point, getMarkerOpts());
            gmap.addOverlay(marker);

            $('#gmap').animate({
                height: '7em',
                opacity: 0.6
            }, 500, 'swing', function() {
                gmap.checkResize();
                gmap.setCenter(point, 12);
                gmap.disableDragging();
                $('#gmap').click(onMapClicked);
            });
        });
        gmap.getContainer().appendChild(shrinkButton);
        return shrinkButton;
    }
    ShrinkControl.prototype.getDefaultPosition = function() {
        return new GControlPosition(G_ANCHOR_BOTTOM_LEFT, new GSize(70, 7));
    }

    // Sets the proper CSS for the given button element.
    ShrinkControl.prototype.setButtonStyle_ = function(button) {
        button.style.color = "black";
        button.style.backgroundColor = "white";
        button.style.font = "12px Arial";
        button.style.border = "1px solid black";
        button.style.padding = "2px";
        button.style.marginBottom = "3px";
        button.style.textAlign = "center";
        button.style.width = "6em";
        button.style.cursor = "pointer";
    }
    
    var largeMapControl = new google.maps.LargeMapControl();
    var mapTypeControl = new google.maps.MapTypeControl()
    var shrinkControl = new ShrinkControl();
    
    window.gmap = new google.maps.Map2(document.getElementById('gmap'));
    
    /* Map enlarges and becomes active when you click on it */
    $('#gmap').css({'cursor': 'pointer', 'opacity': 0.6}).attr(
        'title', 'Activate larger map'
    );
    gmap.disableDragging();
    function onMapClicked() {
        $('#gmap').css({'cursor': ''}).attr('title', '');
        $('#gmap').animate({
            height: '25em',
            opacity: 1.0
        }, 500, 'swing', function() {
            gmap.checkResize();
            gmap.enableDragging();
            // Need to recreate LargeMapControl to work around a bug
            largeMapControl = new google.maps.LargeMapControl();
            gmap.addControl(largeMapControl);
            gmap.addControl(mapTypeControl);
            gmap.addControl(shrinkControl);
            showNearbyPeople(gmap);
            // Unbind event so user can actually interact with map
            $('#gmap').unbind('click', onMapClicked);
        });
    }
    $('#gmap').click(onMapClicked);
    
    var point = new google.maps.LatLng(
        person_latitude, person_longitude
    );
    gmap.setCenter(point, 12);
    var marker = new google.maps.Marker(point, getMarkerOpts());
    gmap.addOverlay(marker);
}

jQuery(function($) {
    $('#editSkills').hide();
    $('ul.tags li.edit a').toggle(
        function() {
            $('#editSkills').show();
            return false;
        },
        function() {
            $('#editSkills').hide();
            return false;
        }
    );
    
    if ($('#uploadNewPhoto').length && $('div.header img.main').length) {
        var href = $('a#uploadNewPhoto').attr('href');
        $('#uploadNewPhoto').remove();
        var upload = $('<a href="' + href + '">(replace)</a>').appendTo(
            document.body
        );
        var img = $('div.header img.main');
        upload.css({
            'font-size': '10px',
            'text-decoration': 'none',
            'color': 'white',
            'padding': '0px 2px 0px 2px',
            'background-color': 'black',
            'position': 'absolute',
            'top': img.offset().top + img.height() - upload.height() - 1,
            'left': img.offset().left + 4,
            'visibility': 'hidden'
        });
        img.mouseover(function() {
            upload.css('visibility', 'visible');
        });
        upload.mouseover(function() {
            upload.css('visibility', 'visible');
        });
        img.mouseout(function() {
            upload.css('visibility', 'hidden');
        });
    }
    /*    
    // Hide changeloc link too
    if ($('a.changeloc').length) {
        $('a.changeloc').css('visibility', 'hidden');
        $('a.changeloc').parent().mouseover(function() {
            $('a.changeloc').css('visibility', 'visible');
        });
        $('a.changeloc').parent().mouseout(function() {
            $('a.changeloc').css('visibility', 'hidden');
        });
        $('a.changeloc').mouseover(function() {
            $('a.changeloc').css('visibility', 'visible');
        });
    }
    
    // And tags edit
    if ($('ul.tags li.edit').length) {
        var a = $('ul.tags li.edit a').css('text-decoration', 'none');
        a.css('visibility', 'hidden');
        a.parent().parent().mouseover(function() {
            a.css('visibility', 'visible');
        });
        a.parent().parent().mouseout(function() {
            a.css('visibility', 'hidden');
        });
        a.mouseover(function() {
            a.css('visibility', 'visible');
        });
    }
    
    // And the edit links in the h2s
    $('h2 a.edit').each(function() {
        var $this = $(this);
        $this.css('visibility', 'hidden');
        $this.parent().mouseover(function() {
            $this.css('visibility', 'visible');
        });
        $this.parent().mouseout(function() {
            $this.css('visibility', 'hidden');
        });
        $this.mouseover(function() {
            $this.css('visibility', 'visible');
        });
    });
    
    // And the edit bio link
    if ($('div.bio a.edit').length) {
        $div = $('div.bio');
        $a = $('div.bio a.edit');
        $a.css('visibility', 'hidden');
        $div.mouseover(function() {
            $a.css('visibility', 'visible');
        });
        $div.mouseout(function() {
            $a.css('visibility', 'hidden');
        });
        $a.mouseover(function() {
            $a.css('visibility', 'visible');
        });
    }
    */    
});
