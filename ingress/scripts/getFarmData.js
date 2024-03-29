var getFarmData = function(){
	var element = document.createElement('script');
	element.src = 'https://cdnjs.cloudflare.com/ajax/libs/underscore.js/1.5.2/underscore-min.js';
	element.type = 'text/javascript';
	document.getElementsByTagName('head')[0].appendChild(element);

	var element = document.createElement('script');
	element.src = '	http://code.jquery.com/jquery-2.1.4.js';
	element.type = 'text/javascript';
	document.getElementsByTagName('head')[0].appendChild(element);

	var portalGuids = [
		"fff3620232dc442198bae1f592204f17.16",
		"03963442c5f0480b9fd5e3eba376bf64.16",
		"0429cafdbdd040a0a2959fed0e12c500.16",
		"9546590924d24017bfd7c6fbdc03781a.16",
		"dedd96c697444ffb823c14354416311f.16",
		"fcfe56ea96aa4b4aa8e1cf76c806db97.16",
		"76c441700b624b5f8b2dbea117cefc3b.16",
		"81ecb7bf4d6a4b73b92bd5d7892906c5.16",
		"4c5eaaae547a4e36a128d34b169aab11.16",
		"4c364b07c9044038b1bc00d49817c264.16",
		"0d4547c16b734832b21ee58903eebd01.16",
		"5ee53d25ddcd4b71a6fa4d5571ef08e6.16",
		"031db241c91344adb8dd8d9b370c6ca0.16",
		"e5b515a63f0d4991866c25f59ccfa207.11",
		"6fc0ba1e0ab04385b4de2dbfa4c31c26.16",
		"a2ae025e79a5449f8e23127358608246.16",
		"7bf1d2cf8b63459ca079619745978704.16",
		"bb65b8abb3444f7bb7e14f12283bb40b.16",
		"dde370dcaefd4c13b2be3ed2b38646a7.16",
		"af6acb9469ff4b11a68a8e0d46c4ff0c.16",
		"ef91ee113784440d932d96e7d26c7a43.16",
		"cdc807b322494ecb8976b6f7031f7a24.16",
		"92f9d017ad90443f9dcf0a2e15ae5653.16",
		"01bee9f44bcf4e91be12f1977590de65.16",
		"e0858eda49c6486d8165bf12c6685e0b.16",
		"ddf8c73a481d4114adb36a41ae8fa9f6.16",
		"60338032c0424d9fbac8c8c14a0e8559.16",
		"eb71b61bafd34f4a9fd39e3fb94f29dd.16",
		"3e54256ff0764fec88230ff24d2aaba7.16",
		"93f8446dc3c040fb96e350026ecf0184.16",
		"25573f1f49cd45129cabe128f75f397e.16",
		"51f5546945e94777a118bcdf2697f17c.12",
		"29a49d6886854084b43ef775809181dc.16",
		"f840d9470f56469d8d2aac1eb4434096.16",
		"bc11c567924345b9baa2012c96ef6697.16",
		"1e1572923490446ba1c9ed2efe3d9a11.16",
		"ba7b2d42334c41be82f39fa909ec5704.16",
		"728d3dbf39d14cd1838e66a441af9a70.11",
		"ac71613267484afb86d1e980ef84a0e2.16",
		"7b6df35ae6e24686a29b07111cf4e3f0.11",
		"4c7b1a7b028442cfac89bb6dd0c71f6c.16",
		"936a5067812c455b879aec7166e028a8.16",
		"4851c2bc07394700b8c8fa33a5b75933.16",
		"0a85f6115ebd46759ab1d3ff05740b7b.16",
		"9b8ada121c724a1585034d95903fd376.16",
		"758aa80181d1488ea4a54687d47db6df.16",
		"60139963f44d4134a053e57858d6c395.16",
		"22775e24357043519c5a9f67138b6fb6.16",
		"72e479b72b384035b54e61e2e9af7952.16"
	];

	var remainingResults = portalGuids.length;
	var results = [];

	var cb = function(response) {
		results.push(response.result);
		console.log(response.result[8]);
		--remainingResults;
		if (remainingResults === 0){
			$.ajax({
				type: "POST",
				url: "http://www.stormtide.net/ingress/uploadFarmData",
				contentType: "application/json; charset=utf-8",
				dataType: 'json',
				data: JSON.stringify(results),
				success: function(data){
					console.log('Results uploaded to www.stormtide.net.')
				}
			});
		};
	}
	for(var i = 0; i < portalGuids.length; ++i) {
		Ne(R.l().b.a, Aa, {guid: portalGuids[i]}, cb);
	}
}