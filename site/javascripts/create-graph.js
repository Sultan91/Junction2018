/*
 * Parse the data and create a graph with the data.
 */
function parseData(createGraph) {
	Papa.parse("../data/final.csv", {
		download: true,
		complete: function(results) {
			createGraph(results.data);
		}
	});
}

function createGraph(data) {
	var years = [];
	var silverMinted = ["humid"];

	for (var i = 1; i < data.length; i++) {
		years.push(data[i][10]);
		silverMinted.push(data[i][6]);
	}

	console.log(years);
	console.log(silverMinted);

	var chart = c3.generate({
		bindto: '#chart',
	    data: {
	        columns: [
	        	silverMinted
	        ]
	    },
	    axis: {
	        x: {
	            type: 'category',
	            categories: years,
	            tick: {
	            	multiline: false,
                	culling: {
                    	max: 15
                	}
            	}
	        }
	    },
	    zoom: {
        	enabled: true
    	},
	    legend: {
	        position: 'right'
	    }
	});
}

parseData(createGraph);