

difference($fs = 0.5000000000) {
	polygon(paths = [[0, 1, 2, 3, 0]], points = [[32.8500000000, 72.6836000000], [32.8500000000, 110.1408700000], [96.0757000000, 110.1408700000], [96.0757000000, 72.6836000000]]);
	difference($fs = 0.5000000000) {
		difference($fs = 0.5000000000) {
			difference($fs = 0.5000000000) {
				difference($fs = 0.5000000000) {
					square($fs = 0.5000000000, size = [600, 300]);
					polygon(paths = [[]], points = []);
				}
				polygon(paths = [[0, 1, 2, 3, 0]], points = [[0.0000000000, 0.0000000000], [0.0000000000, 21.3338600000], [34.8165000000, 21.3338600000], [34.8165000000, 0.0000000000]]);
			}
			polygon(paths = [[0, 1, 2, 3, 0]], points = [[0.0000000000, 21.3338000000], [0.0000000000, 72.6835700000], [66.1500000000, 72.6835700000], [66.1500000000, 21.3338000000]]);
		}
		polygon(paths = [[0, 1, 2, 3, 0]], points = [[0.0000000000, 72.6836000000], [0.0000000000, 292.0801000000], [32.8500000000, 292.0801000000], [32.8500000000, 72.6836000000]]);
	}
}