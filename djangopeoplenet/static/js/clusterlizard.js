
//if (typeof(GObject) == "undefined") {
//	GObject = google.maps.Object;
//	GSize = google.maps.Size;
//	GPoint = google.maps.Point;
//	GIcon = google.maps.Icon;
//	GLatLng = google.maps.LatLng;
//	GOverlay = google.maps.Overlay;
//	G_MAP_MARKER_PANE = google.maps.MAP_MARKER_PANE;
//}

window.ClusterLizard = {

	clusterIcon: function (size, w, h) {
		var icon = new GIcon();
		icon.image = "/static/img/marker_" + size + ".png"
		icon.shadowImage = "/static/img/marker_" + size + "_shadow.png"
		icon.iconSize = new GSize(w, h);
		icon.shadowSize = icon.iconSize;
		icon.iconAnchor = new GPoint(w/2, h/2);
		icon.infoWindowAnchor = icon.iconAnchor;
		return icon;
	},

	addCluster: function(map, latlng, number) {
		if (number > 1000) {
			icon = ClusterLizard.icon_large;
		} else if (number > 300) {
			icon = ClusterLizard.icon_med;
		} else if (number > 10) {
			icon = ClusterLizard.icon_small;
		} else {
			icon = ClusterLizard.icon_tiny;
		}
		var marker = new ClusterLizard.ClusterMarker(latlng, icon, number);
		map.addOverlay(marker);
		return marker;
	},
	
	ClusterMarker: function (latlng, icon, number) {
		this.latlng = latlng;
		this.icon = icon;
		this.number = number;
		this.fontSize = 10;
	},
	
}

/////////// Implementing ClusterMarker ////////////

ClusterLizard.ClusterMarker.prototype = new GOverlay();

// Makes DOM elements
ClusterLizard.ClusterMarker.prototype.initialize = function (map) {
	var div = document.createElement("div");
	var img = document.createElement("img");
	img.src = this.icon.image;
	img.style.position = "absolute";
	img.style.top = "0px";
	img.style.left = "0px";
	div.appendChild(img);
	div.style.position = "absolute";
	var label = document.createElement("div");
	label.innerHTML = "" + this.number;
	label.style.fontSize = this.fontSize + "px";
	label.style.fontWeight = "bold";
	label.style.color = "#fff";
	label.style.position = "absolute";
	label.style.textAlign = "center";
	label.style.width = "100%";
	label.style.top = ((this.icon.iconSize.height-this.fontSize)/2)-1 + "px";
	div.appendChild(label);
	div.style.width = this.icon.iconSize.width + "px";
	div.style.height = this.icon.iconSize.height + "px";
	// Add to the map pane
	map.getPane(G_MAP_MARKER_PANE).appendChild(div);
	this.div = div;
	this.img = img;
	this.label = label;
	this.map = map;
}

// Removes DOM elements
ClusterLizard.ClusterMarker.prototype.remove = function () {
	this.div.parentNode.removeChild(this.div);
}

// Cloning
ClusterLizard.ClusterMarker.prototype.copy = function () {
	return new ClusterLizard.ClusterMarker(this.latlng, this.icon);
}

// Drawing
ClusterLizard.ClusterMarker.prototype.redraw = function(force) {

  // We only need to redraw if the coordinate system has changed
  if (!force) return;

  // Calculate the DIV coordinates of two opposite corners of our bounds to
  // get the size and position of our rectangle
  var coords = this.map.fromLatLngToDivPixel(this.latlng);

  // Now position our DIV based on the DIV coordinates of our bounds
  this.div.style.top = coords.y - (this.icon.iconSize.height/2) + "px";
  this.div.style.left = coords.x - (this.icon.iconSize.width/2) + "px";
  
}

// Binds the click action on the marker to going somewhere.
ClusterLizard.ClusterMarker.prototype.bindClick = function(url) {
	this.div.style.cursor = "pointer";
	this.div.onclick = function () {
		window.location.href = url;
	}
}

	
ClusterLizard.icon_large = ClusterLizard.clusterIcon(4, 48, 48);
ClusterLizard.icon_med = ClusterLizard.clusterIcon(3, 39, 39);
ClusterLizard.icon_small = ClusterLizard.clusterIcon(2, 28, 28);
ClusterLizard.icon_tiny = ClusterLizard.clusterIcon(1, 17, 17);