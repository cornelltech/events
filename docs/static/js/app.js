;( function( $, window, document, undefined ) {
    "use strict";

    function filterOn(val) {
        // $('.grid').isotope({ filter: val });

        if( val === '*' ) {
            $('.grid-item').show();
        }else {
            $('.grid-item').show();
            $('.grid-item:not(' + val + ')').hide();
        }

    }

    function initIsotope() {
        $('.grid').isotope({
            // options
            itemSelector: '.grid-item',
            isFitWidth: true
        });
    }

    /** Attach event listeners */

    $('.filter-btn').click(function(evt) {
        var filterValue = evt.target.getAttribute('data-filter-value');
        filterOn(filterValue);
    });


    /** Main */
    function main(){
        // initIsotope();
    } 
    main();
    


}) ( jQuery, window, document );