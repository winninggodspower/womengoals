window.addEventListener('load', function(){
    const carouselSetting =  {
        slidesToShow: 1,
        slidesToScroll: 1,
        draggable: true,
        
        dots: '.dots',
        arrows: {
            prev: '.glider-prev',
            next: '.glider-next'
        }
    }

    new Glider(document.querySelector('.glider'), carouselSetting)



  })