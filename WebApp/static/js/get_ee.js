<script type="text/javascript">
		$('#form-prds').on('submit', function loadProducts(e) {
			e.preventDefault();
			console.log("form submitted!");
			update_map();
			function update_map() {
				console.log("create post is working!") // sanity check
				$.ajax({
					url: "{% url 'get-image-collection' %}", // the endpoint
					type: "POST", // http method
					data: {
						platforms: $('#id_platforms').val(),
						sensors: $('#id_sensors').val(),
						products: $('#id_products').val(),
						start_date: $('#id_start_date').val(),
						end_date: $('#id_end_date').val(),
						reducer: $('#id_reducer').val()
					},

					// handle a successful response
					success: function data_loaded(json) {

						console.log(json); // log the returned json to the console
						console.log("success"); // another sanity check
						var gee_layer = new L.tileLayer(json.url, { attribution: '&copy; <a href="https://www.earthengine.google.com/copyright">Google Earth Engine</a>'})
						function get_gee_layer(){
							gee_layer.addTo(map);
							var baseMaps = {
								"OpenStreetMap": openstreetmap,
							};
							var overlaymaps = {
								lyr:gee_layer,
							};
							L.control.layers(baseMaps, overlaymaps).addTo(map);
							gee_layer.on('tileload', function () {
								console.log("Loading the requested data......");
								document.getElementById('overlay').style.display = 'block';
							});
							gee_layer.on('load', function () {
								console.log("Data loaded.");
								document.getElementById('overlay').style.display = 'none';
							});
							return gee_layer;
						};
						get_gee_layer();
					},
					// handle a non-successful response
					error: function (xhr, errmsg, err) {
						// add the error to the dom
						alert("There was an error loading the requested data")
					}
				});
			}
		});
		var map = L.map('map-div', {
			center: [0.3556, 37.5833],
			zoom: 6,
		});
		var openstreetmap = L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
			attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
		}).addTo(map);
		//let overlaymaps = loadProducts().update_layer_control();
		L.marker([0.3556, 37.5833]).addTo(map)
			.bindPopup('Approximately the center of Kenya');
	</script>