var loadImage = function(event) {
	var image = document.getElementById('member_photo');
	image.src = URL.createObjectURL(event.target.files[0]);
};
