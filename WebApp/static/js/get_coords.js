var Map = L.map("Map");

var tile_layer_openstreetmap = L.tileLayer(
	"https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
        {"attribution": "Data by \u0026copy; \u003ca href=\"http://openstreetmap.org\"\u003eOpenStreetMap\u003c/a\u003e, under \u003ca href=\"http://www.openstreetmap.org/copyright\"\u003eODbL\u003c/a\u003e.", "detectRetina": false, "maxNativeZoom": 30, "maxZoom": 30, "minZoom": 0, "noWrap": false, "opacity": 1, "subdomains": "abc", "tms": false}
).addTo(Map);
        
    
var tile_layer_google_maps = L.tileLayer(
	"https://mt1.google.com/vt/lyrs=m\u0026x={x}\u0026y={y}\u0026z={z}",{
        "attribution": "Google", 
        "detectRetina": false, 
        "maxNativeZoom": 22, 
        "maxZoom": 22, 
        "minZoom": 0, 
        "noWrap": false, 
        "opacity": 1, 
        "subdomains": "abc", 
        "tms": false}
).addTo(Map);

var tile_layer_google_satellite = L.tileLayer(
	"https://mt1.google.com/vt/lyrs=y\u0026x={x}\u0026y={y}\u0026z={z}",{
        "attribution": "Google", 
        "detectRetina": false, 
        "maxNativeZoom": 22, 
        "maxZoom": 22, 
        "minZoom": 0, 
        "noWrap": false, 
        "opacity": 1, 
        "subdomains": "abc", 
        "tms": false}
).addTo(Map);

L.Control.geocoder({"collapsed": true, "defaultMarkGeocode": true, "position": "topleft"}).on('markgeocode', function(e) {
                Map.setView(e.geocode.center, 11);
            }).addTo(Map);        
    
Map.fitBounds(
	[[-24, -55], [-24, -55]],
        {"maxZoom": 6}
);

var layer_control = {
	base_layers : {
		"openstreetmap" : tile_layer_openstreetmap,
        },
        overlays :  {
        	"Google Maps" : tile_layer_google_maps,
                "Google Satellite" : tile_layer_google_satellite,
        },
};

L.control.layers(
	layer_control.base_layers,
        layer_control.overlays,
        {"autoZIndex": true, "collapsed": true, "position": "topright"}
).addTo(Map);
            
var options = {
	position: "topleft",
        draw: {},
        edit: {},
}
            
// FeatureGroup is to store editable layers.
var drawnItems = new L.featureGroup().addTo(Map);
options.edit.featureGroup = drawnItems;
var draw_control = new L.Control.Draw(options).addTo(Map);
Map.on(L.Draw.Event.CREATED, function(e) {
                		var layer = e.layer,
                    		    type = e.layerType;
                		var coords = JSON.stringify(layer.toGeoJSON());
                		layer.on('click', function() {
                    				alert(coords);
                    				console.log(coords);
                		});
                		drawnItems.addLayer(layer);
});
Map.on('draw:created', function(e) {
	drawnItems.addLayer(e.layer);
});      
 
document.getElementById('get_coords').onclick = function(e) {
		var data = drawnItems.toGeoJSON();
        	var data_geojson = JSON.stringify(data, undefined, 2);
        	document.getElementById('info').textContent = data_geojson;   
            }