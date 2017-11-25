document.addEventListener("DOMContentLoaded", function(event) {

	if (window.DeviceOrientationEvent) {
  document.getElementById("notice").innerHTML = "Gaaf! De DeviceOrientationEvent API word door dit toestel ondersteund.";
  window.addEventListener('deviceorientation', function(eventData) {
  	// gamma: Tilting the device from left to right. Tilting the device to the right will result in a positive value.
    // gamma: Het kantelen van links naar rechts in graden. Naar rechts kantelen zal een positieve waarde geven.
    var tiltLR = eventData.gamma;

    // beta: Tilting the device from the front to the back. Tilting the device to the front will result in a positive value.
    // beta: Het kantelen van voor naar achteren in graden. Naar voren kantelen zal een positieve waarde geven.
    var tiltFB = eventData.beta;

    // alpha: The direction the compass of the device aims to in degrees.
    // alpha: De richting waarin de kompas van het apparaat heen wijst in graden.
    var dir = eventData.alpha

    // Call the function to use the data on the page.
    // Roep de functie op om de data op de pagina te gebruiken.
    deviceOrientationHandler(tiltLR, tiltFB, dir);
  }, false);
} else {
  document.getElementById("notice").innerHTML = "Helaas. De DeviceOrientationEvent API word niet door dit toestel ondersteund."
};

    function deviceOrientationHandler(tiltLR, tiltFB, dir) {
      document.getElementById("tiltLR").innerHTML = Math.ceil(tiltLR);
      document.getElementById("tiltFB").innerHTML = Math.ceil(tiltFB);
      document.getElementById("direction").innerHTML = Math.ceil(dir);
      
      // Rotate the disc of the compass.
      // Laat de kompas schijf draaien.
      var compassDisc = document.getElementById("compassDiscImg");
      compassDisc.style.webkitTransform = "rotate("+ dir +"deg)";
      compassDisc.style.MozTransform = "rotate("+ dir +"deg)";
      compassDisc.style.transform = "rotate("+ dir +"deg)";
    }

});