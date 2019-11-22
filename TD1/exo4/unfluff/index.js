/*
 * This module allows to extract text contained in HTML files using unfluff.
 *
 * Antoine Orgerit - François Gréau - Lisa Fougeron
 * La Rochelle Université - 2019-2020
 */

var extractor = require('unfluff');
var fs = require('fs');

var source_files_path = '../../resources/html/';
var dest_files_path = '../../resources/unfluff/'
var files = fs.readdirSync(source_files_path);

files.forEach(function(file) {
	fs.readFile(source_files_path + file, function(err, content) {
		if (err) {
			console.log(err);
		} else {
			data = extractor(content)
			content_to_write = ' ';
			if (data.text != '') {
				content_to_write = data.text
			}
			fs.appendFile(dest_files_path + file, content_to_write, function(
					err) {
				if (err) {
					console.log(err);
				}
			});
		}
	});
});