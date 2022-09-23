
let slideIndex = [1, 1, 1, 1, 1, 1];
//represents the class of each project
let slideId = ["Slides1", "Slides2", "Slides3", "Slides4", "Slides5", "Slides6"]


showSlides(1, 0);
showSlides(1, 1);
showSlides(1, 2);
showSlides(1, 3);
showSlides(1, 4);
showSlides(1, 5);


// Next/previous controls
function plusSlides(n, no) {
  showSlides(slideIndex[no] += n, no);
}

// Thumbnail image controls
function currentSlide(n) {
  showSlides(slideIndex = n);
}

function showSlides(n, no) {
  let i;
  let slides = document.getElementsByClassName(slideId[no]);


  if (n > slides.length) {slideIndex[no] = 1}

  if (n < 1) {slideIndex[no] = slides.length}
  
  for (i = 0; i < slides.length; i++) {
    slides[i].style.display = "none";
  }

  // console.log(slides.length, slideIndex[no]);
  slides[slideIndex[no] - 1].style.display = "block";

//   dots[slideIndex-1].className += " active";
}