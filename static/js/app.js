;( function( $, window, document, undefined ) {
    "use strict";

    function filterOn(val) {
        if( val === '*' ) {
            $('.grid-item').show();
        }else {
            $('.grid-item').show();
            $('.grid-item:not(' + val + ')').hide();
        }

    }

    function initSelect() {
        $('select').select2({
            placeholder: 'Filter by tag',
        });
        $('select').on("select2:select", function (e) { 
            var tag = e.target.value;
            filterOn('.' + tag);
        });
        $('select').on("select2:unselect", function (e) { 
            var tag = e.target.value;

        });

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
        initSelect();
    } 
    main();

}) ( jQuery, window, document );